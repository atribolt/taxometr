from flask import Flask, request_started, request, request_finished, g
from taxometr.server.routes import task
from pathlib import Path


def put_trace_hash(*_, **__):
  from taxometr.context import set_trace_hash, generate_trace_hash

  trace_hash = request.headers.get('Trace-Hash', None)
  if not trace_hash:
    trace_hash = generate_trace_hash()

  set_trace_hash(trace_hash)


def bind_database(sender, **__):
  from taxometr.database import get_connection, TABLES
  db = get_connection()
  db.bind(TABLES)
  g.db = db
  sender.logger.debug('database connection is opened: %x', id(db))


def close_database(sender, **__):
  try:
    db = g.pop('db')
    if db:
      db.close()
  except Exception as exc:
    sender.logger.warning('any exception while close database', exc_info=exc)
  else:
    sender.logger.debug('database connection closed: %x', id(db))


def create_app():
  server = Flask('AcquiringService',
                 static_url_path='/',
                 static_folder='public')

  request_started.connect(put_trace_hash, server)
  request_started.connect(bind_database, server)
  request_finished.connect(close_database, server)

  server.get('/task')(task.get_task_list)
  server.put('/task')(task.new_task)
  server.post('/task/<task_id>')(task.update_task)
  server.delete('/task/<task_id>')(task.delete_task)

  return server
