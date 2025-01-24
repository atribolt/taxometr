import flask
import taxometr.server.errors as err
from taxometr.database import ActionDB, TimeRangeDB
from functools import wraps
from taxometr.server.routes import JsonRequest
from taxometr.server.schemas import ActionParamsSchema


actions_handler = flask.Blueprint('actions', __name__, url_prefix='/action')


def action_required(func):
  @wraps(func)
  def wrapper(action_id: int, *args, **kwargs):
    logger = flask.current_app.logger
    if not action_id or action_id < 0:
      logger.error('invalid action ID "%i"', action_id)
      return err.InvalidIdentifier('Required valid action identifier')
    action = ActionDB.get_action(action_id)
    return func(action, *args, **kwargs)
  return wrapper


@actions_handler.delete('/<int:action_id>')
@action_required
def delete_action(action: ActionDB):
  ActionDB.delete_action(action)
  flask.current_app.logger.info('%s deleted', action)


@actions_handler.post('/<int:action_id>')
@action_required
@JsonRequest(ActionParamsSchema)
def update_action(action_params: ActionParamsSchema, action: ActionDB):
  if action_params.name != action.description:
    oldname = action.description
    action.description = action_params.name
    ActionDB.update_action(action)
    flask.current_app.logger.info('action name changed: %s -> %s', oldname, action.description)

  return {
    'id': action.id,
    'taskId': action.task.id,
    'name': action.description
  }


@actions_handler.post('/<int:action_id>/start')
@action_required
def start_action(action: ActionDB):
  log = flask.current_app.logger

  was_active, stopped_action = TimeRangeDB.stop_active_action()
  if was_active:
    log.info('stopped action: %s', stopped_action.description)

  TimeRangeDB.start_action(action)
  log.info('action started: %s', action.description)
  return flask.Response(status=200)


@actions_handler.post('/stop')
def stop_action():
  was_active, stopped_action = TimeRangeDB.stop_active_action()
  if was_active:
    flask.current_app.logger.info('stopped action: %s', stopped_action.description)
    return {
      'id': stopped_action.id,
      'name': stopped_action.description
    }
  return err.NoActiveActions('No active actions')
