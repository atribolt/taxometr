import copy
import logging
import flask
import taxometr.server.errors as err
from taxometr.database import TaskDB, ActionDB
from taxometr.server.routes import logger_required


actions_handler = flask.Blueprint('actions', __name__, url_prefix='/action')


# @actions_handler.put('/<int:task_id>')



@logger_required
def get_task_actions(logger: logging.Logger, task_id: int):
  if not task_id or task_id < 0:
    logger.error('invalid task ID "%i"', task_id)
    return err.InvalidIdentifier('Action required valid task identifier')

  task = TaskDB.get_task(task_id)

  filters = flask.request.args.get('filter', {})
  action_name = filters.get('name', None)

  if action_name is not None:
    if not isinstance(action_name, str) or not action_name.isprintable():
      logger.error('action name in filter invalid: %s', action_name)
      return err.InvalidActionName('action name should be valid string')

  return [
    {
      'id': action.id,
      'taskId': action.task.id,
      'name': action.description
    }
    for action in ActionDB.get_actions_by_task(task, action_name)
  ]


@logger_required
def delete_action(logger: logging.Logger, action_id: int):
  if not action_id or action_id < 0:
    logger.error('invalid action ID "%i"', action_id)
    return err.InvalidIdentifier('Action required valid identifier')

  action = ActionDB.get_action(action_id)
  ActionDB.delete_action(action)

  logger.info('%s deleted', action)


@logger_required
def update_action(logger: logging.Logger, action_id: int):
  if not action_id or action_id < 0:
    logger.error('invalid action ID "%i"', action_id)
    return err.InvalidIdentifier('Action required valid identifier')

  action = ActionDB.get_action(action_id)

  params: dict = flask.request.json
  action_name = params.get('name')

  if action.description != action_name:
    update = copy.copy(action)
    update.description = action_name

    ActionDB.update_action(update)
    logger.info('updated: %s -> %s', action, update)

  return {
    'id': action.id,
    'taskId': action.task.id,
    'name': action.description
  }

