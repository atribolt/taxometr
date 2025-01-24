import logging
import flask
import taxometr.server.errors as err
from taxometr.database import TaskDB
from taxometr.server.routes import JsonRequest
from pydantic import BaseModel, Field
from taxometr.common.validations import PrintableString


class TaskParamsSchema(BaseModel):
  title: PrintableString = Field(max_length=1000)


task_handler = flask.Blueprint('tasks', __name__, url_prefix='/task')


@task_handler.get('/')
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


@task_handler.put('/')
@JsonRequest(TaskParamsSchema)
def new_task(task_params: TaskParamsSchema):
  logger = flask.current_app.logger
  task = TaskDB.new(task_params.title)
  logger.info('task created: %i - %s', task.id, task.title)
  return {
    'id': task.id,
    'title': task.title
  }, 201


@task_handler.post('/<int:task_id>')
@JsonRequest(TaskParamsSchema)
def update_task(task_params: TaskParamsSchema, task_id: int):
  task = TaskDB()
  task.id = task_id
  task.title = task_params.title
  TaskDB.update_task(task)
  return {
    'id': task.id,
    'title': task.title
  }


@logger_required
def delete_task(logger: logging.Logger, task_id: int):
  if not task_id or task_id < 0:
    logger.error('invalid task ID "%i"', task_id)
    return err.InvalidIdentifier('Required valid task identifier')

  task = TaskDB.get_task(task_id)
  TaskDB.delete_task(task)

  logger.info('%s deleted', task)


def new_task_action(logger: logging.Logger, task_id: int):
  if not task_id or task_id < 0:
    logger.error('invalid task ID "%i"', task_id)
    return err.InvalidIdentifier('Action required valid task identifier')

  params: dict = flask.request.json
  action_name = params.get('name', None)

  if action_name is None:
    logger.error('action name is not present')
    return err.InvalidActionName('action name required')
  elif not isinstance(action_name, str) or not action_name or not action_name.isprintable():
    logger.error('action name invalid: %s', action_name)
    return err.InvalidActionName('action name should be valid printable string')

  action = ActionDB()
  action.task = TaskDB.get_task(task_id)
  action.description = action_name

  action = ActionDB.new(action)
  logger.info('action created: %s', action)
  return {
    'id': action.id,
    'taskId': action.task.id,
    'name': action.description
  }