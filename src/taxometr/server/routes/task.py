import logging
import flask
import taxometr.server.errors as err
from taxometr.database import TaskDB, Task
from taxometr.server.routes import logger_required


def get_task_list():
  filters = flask.request.args.get('filter', {})

  title = filters.get('title', None)
  offset = flask.request.args.get('offset', 0)
  count = flask.request.args.get('count', 1000)

  return [
    {
      'id': task.id,
      'title': task.title
    }
    for task in TaskDB.get_tasks(
      task_title=title,
      offset=offset,
      count=count
    )
  ]


@logger_required
def new_task(logger: logging.Logger):
  props: dict = flask.request.json

  task = Task()
  task.title = props.get('title', '')

  if not task.title:
    return err.InvalidTitle('Title is required')
  elif not task.title.isprintable():
    return err.InvalidTitle('Title should be printable text')

  logger.debug('try create new task: %s', task.title)
  task = TaskDB.new(task)

  logger.debug('task created: %i - %s', task.id, task.title)
  return task.id, 201


@logger_required
def update_task(logger: logging.Logger, task_id: int):
  if task_id < 0:
    logger.error('invalid identifier: %i', task_id)
    return err.InvalidIdentifier("task id can't be less then zero")

  params: dict = flask.request.json

  task = Task()
  task.id = task_id
  task.title = params.get('title')

  TaskDB.update_task(task)
  return {
    task.id,
    task.title
  }


@logger_required
def delete_task(logger: logging.Logger, task_id: int):
  if not task_id or task_id < 0:
    logger.error('invalid task ID "%i"', task_id)
    return err.InvalidIdentifier('Required valid task identifier')

  task = TaskDB.get_task(task_id)
  TaskDB.delete_task(task)

  logger.info('%s deleted', task)
