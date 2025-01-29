import flask
from taxometr.server.routes import actions, task, reports


v1 = flask.Blueprint('v1', __name__, url_prefix='/v1')
v1.register_blueprint(task.task_handler)
v1.register_blueprint(actions.actions_handler)
v1.register_blueprint(reports.report_handler)


@v1.get('/echo')
def echo():
  return flask.Response(status=200)
