import click
from functools import partial
from taxometr.cli.commands import Date
from datetime import datetime, timedelta, timezone as tz
from taxometr.cli.printing import Table, echo
from taxometr.dao.factory import DaoFactory
from taxometr.dao import Action, Task


TIME_GROUP = click.Choice(['today', 'month', 'all'], case_sensitive=False)


@click.group()
def action_group():
  """Actions managing"""


@action_group.command('list')
@click.option('-a', '--all', 'show_all', is_flag=True, default=False, help='Show all actions')
@click.option('-s', '--since', type=Date, help='Show actions after')
@click.option('-u', '--until', type=Date, help='Show actions before')
@click.option('-t', '--time', type=TIME_GROUP, default='today', help='Sum time for the period')
def action_list(show_all, since, until, time):
  """Show action list (default show today actions)"""

  action_dao = DaoFactory().get_action_dao()

  if show_all:
    since = until = None
  elif since is None:
    since = datetime.now(tz.utc).replace(hour=0, minute=0, second=0, microsecond=0)

  if time == 'all':
    time_since = None
  elif time == 'month':
    time_since = datetime.now(tz.utc).replace(month=1, hour=0, minute=0, second=0, microsecond=0)
  else:
    time_since = datetime.now(tz.utc).replace(hour=0, minute=0, second=0, microsecond=0)

  active_action = action_dao.get_active_action() or Action()

  table = Table('id', 'task', 'action', 'total time', 'active')
  for action in action_dao.get_actions_by_time(since, until):
    times = action_dao.get_action_timings(action, time_since)

    today_time = sum(map(lambda x: x.total_time, times), timedelta())

    row = [
      action.id,
      action.task.title,
      action.description,
      '%s (%.2f)' % (today_time, today_time.total_seconds() / 60 / 60),
      action.id == active_action.id
    ]
    table.add_row(row)

  echo(str(table))


@action_group.command('show')
@click.option('-s', '--show-ranges', type=TIME_GROUP, help='Show time range for the period', default='all')
@click.argument('action-id')
def action_show(show_ranges, action_id):
  """Show info about an action"""

  action_dao = DaoFactory().get_action_dao()

  today = datetime.now(tz.utc).replace(hour=0, minute=0, second=0, microsecond=0)
  month = datetime.now(tz.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

  today_filter = partial(filter, lambda x: x.begin >= today)
  month_filter = partial(filter, lambda x: x.begin >= month)

  action = action_dao.get_action(action_id)
  timings = list(action_dao.get_action_timings(action))

  all_time = sum(map(lambda x: x.total_time, timings), timedelta())
  today_time = sum(map(lambda x: x.total_time, today_filter(timings)), timedelta())
  month_time = sum(map(lambda x: x.total_time, month_filter(timings)), timedelta())

  echo('Id: {}', action.id)
  echo('Task:')
  echo('  Id: {}', action.task.id)
  echo('  Title: {}', action.task.title)
  echo('Description: {}', action.description)
  echo('All time: {} ({:.2f})', all_time, all_time.total_seconds() / 60 / 60)
  echo('This month time: {} ({:.2f})', month_time, month_time.total_seconds() / 60 / 60)
  echo('Today time: {} ({:.2f})', today_time, today_time.total_seconds() / 60 / 60)

  if show_ranges == 'month':
    filter_ranges = month_filter
  elif show_ranges == 'today':
    filter_ranges = today_filter
  else:
    filter_ranges = lambda x: x

  echo('Time ranges:')
  date_fmt = '%Y-%m-%d %H:%M:%S %Z'
  for time in filter_ranges(timings):
    echo('  | {} | {:.2f}h | {} - {} ',
        time.total_time, time.total_time.seconds / 60 / 60,
        time.begin.strftime(date_fmt), time.end.strftime(date_fmt) if time.end else '...')


@action_group.command('new')
@click.option('-s', '--start', is_flag=True, default=False, help='Запустить эту задачу')
@click.option('-t', '--task', 'task_id', type=int, help='ID задачи')
@click.argument('name')
def action_new(start, task_id, name):
  """Create new action"""

  action_dao = DaoFactory().get_action_dao()

  action = Action()
  action.task = Task()
  action.task.id = task_id
  action.description = name

  action = action_dao.new(action)
  if start:
    action_dao.stop_all_actions()
    action_dao.start_action(action.id)

  echo('{}: ({}) {}', action.id, action.task.title, action.description)


@action_group.command('start')
@click.argument('action-id', type=int)
def action_start(action_id):
  """Start action"""
  action_dao = DaoFactory().get_action_dao()
  action_dao.stop_all_actions()
  action_dao.start_action(action_id)


@action_group.command('stop')
def action_stop():
  DaoFactory().get_action_dao().stop_all_actions()
