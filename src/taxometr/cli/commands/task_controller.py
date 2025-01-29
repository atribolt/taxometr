import click
import requests as req
from urllib.parse import urljoin
from taxometr.cli.printing import echo, Table
from taxometr.cli import context, CliConfig
from pydantic import BaseModel, NonNegativeInt
from taxometr.common.validations import PrintableString


class TaskModel(BaseModel):
  id: NonNegativeInt
  title: PrintableString


@click.group()
def task_group():
  """Task group managing"""


@task_group.command('new')
@click.argument('task-name', type=str)
@context
def task_new(ctx: CliConfig, task_name):
  """Create new task"""
  url = urljoin(ctx.taxometr_server, '/task')

  reply = req.put(url, json={
    'title': task_name
  })

  if reply.status_code != 201:
    click.get_current_context().fail("Task wasn't created: %s")

  echo('{}: {}', task.id, task.title)


@task_group.command('list')
def task_list():
  """Show task list"""

  table = Table('id', 'title')
  for t in DaoFactory().get_task_dao().get_tasks():
    table.add_row([t.id, t.title])
  echo(str(table))
