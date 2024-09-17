import click
from taxometr.dao import Task
from taxometr.cli.printing import echo, Table
from taxometr.dao.factory import DaoFactory


@click.group()
def task_group():
  """Task group managing"""


@task_group.command('new')
@click.argument('task-name', type=str)
def task_new(task_name):
  """Create new task"""
  task = Task()
  task.title = task_name
  task = DaoFactory().get_task_dao().new(task)
  echo('{}: {}', task.id, task.title)


@task_group.command('list')
def task_list():
  """Show task list"""

  table = Table('id', 'title')
  for t in DaoFactory().get_task_dao().get_tasks():
    table.add_row([t.id, t.title])
  echo(str(table))
