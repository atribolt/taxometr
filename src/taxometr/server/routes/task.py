import flask
import taxometr.server.errors as err
from taxometr.database import TaskDB, ActionDB
from taxometr.server.routes import JsonRequest, JsonQueryField
from taxometr.server.schemas import TaskParamsSchema, ActionParamsSchema, ActionFilterSchema
from functools import wraps


task_handler = flask.Blueprint('tasks', __name__, url_prefix='/task')


def task_required(func):
  @wraps(func)
  def wrapper(task_id: int, *args, **kwargs):
    logger = flask.current_app.logger
    if not task_id or task_id < 0:
      logger.error('invalid task ID "%i"', task_id)
      return err.InvalidIdentifier('Required valid task identifier')
    task = TaskDB.get_task(task_id)
    return func(task, *args, **kwargs)
  return wrapper


@task_handler.get('')
def get_task_list() -> list:
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


@task_handler.put('')
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
@task_required
@JsonRequest(TaskParamsSchema)
def update_task(task_params: TaskParamsSchema, task: TaskDB):
  if task_params.title != task.title:
    old_title = task.title
    task.title = task_params.title
    TaskDB.update_task(task)
    flask.current_app.logger.info('task title update "%s" -> "%s"', old_title, task.title)

  return {
    'id': task.id,
    'title': task.title
  }


@task_handler.delete('/<int:task_id>')
@task_required
def delete_task(task: TaskDB):
  logger = flask.current_app.logger
  TaskDB.delete_task(task)
  logger.info('%s deleted', task)


@task_handler.put('/<int:task_id>/action')
@task_required
@JsonRequest(ActionParamsSchema)
def new_task_action(action_params: ActionParamsSchema, task: TaskDB):
  logger = flask.current_app.logger

  action = ActionDB()
  action.task = task
  action.description = action_params.name

  action = ActionDB.new(action)
  logger.info('action created: %s', action)
  return {
    'id': action.id,
    'taskId': action.task.id,
    'name': action.description
  }


@task_handler.get('/<int:task_id>/action')
@task_required
@JsonQueryField('filter', ActionFilterSchema)
def get_task_actions(filters: ActionFilterSchema, task: TaskDB):
  return [
    {
      'id': action.id,
      'taskId': action.task.id,
      'name': action.description
    }
    for action in ActionDB.get_actions_by_task(task, filters.name)
  ]
