import click
from pathlib import Path
import taxometr.configure as config
import taxometr.cli.printing as printing
from taxometr.cli.commands import (
  task_group,
  action_group
)
from taxometr.dao.database import get_connection, TABLES


ReadableFile = click.Path(exists=True, readable=True, dir_okay=False, path_type=Path)
Date = click.DateTime(formats=['%Y-%m-%d', '%H:%M:%S', '%Y-%m-%d %H:%M:%S'])


class Context:
  database = None


context = click.make_pass_decorator(Context, True)


@click.group()
@click.option('-v', '--verbose', count=True,
              default=False, help='Enable verbose output (-v, -vv, -vvv)')
@click.option('-C', '--colored', is_flag=True, default=False, help='Enable colored output')
@click.option('-c', '--config', 'config_file', type=ReadableFile, help='Config file')
@context
def cli(ctx, verbose, colored, config_file):
  """CLI for taxometr"""
  printing.init(verbose, colored)
  config.load_from_file(config_file)

  ctx.database = get_connection()
  ctx.database.bind(TABLES)


cli.add_command(task_group, 'task')
cli.add_command(action_group, 'action')
