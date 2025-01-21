import os
from flask import Flask, request_started, request, request_finished, g
from taxometr.server.routes import task, actions, reports


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
  server = Flask('taxometr',
                 static_url_path='/',
                 static_folder='public')

  log = server.logger

  if config := os.environ.get('TAXOMETR_CONFIG'):
    log.debug('TAXOMETR_CONFIG is present: %s', config)
    if os.path.exists(config):
      log.debug('load config: %s', config)

      import taxometr.configure as cfg
      from pathlib import Path

      cfg.load_from_file(Path(config))
    else:
      log.warning('config %s is not exists', config)
  if 'TAXOMETR_DEBUG' in os.environ:
    from taxometr.log import init_debug_logging
    init_debug_logging()

  request_started.connect(put_trace_hash, server)
  request_started.connect(bind_database, server)
  request_finished.connect(close_database, server)

  server.get('/task')(task.get_task_list)
  server.put('/task')(task.new_task)
  server.post('/task/<int:task_id>')(task.update_task)
  server.delete('/task/<int:task_id>')(task.delete_task)

  server.put('/task/<int:task_id>/action')(actions.new_task_action)
  server.get('/task/<int:task_id>/action')(actions.get_task_actions)
  server.delete('/action/<int:action_id>')(actions.delete_action)
  server.post('/action/<int:action_id>')(actions.update_action)
  server.get('/timings/report')(reports.get_timing_report)

  return server
