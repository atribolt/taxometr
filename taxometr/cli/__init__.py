import click
import taxometr.configure as config
import taxometr.cli.printing as printing
from taxometr.cli.commands import (
  task_group,
  action_group
)


ReadableFile = click.Path(exists=True, readable=True, dir_okay=False)
Date = click.DateTime(formats=['%Y-%m-%d', '%H:%M:%S', '%Y-%m-%d %H:%M:%S'])


@click.group()
@click.option('-v', '--verbose', count=True,
              default=False, help='Enable verbose output (-v, -vv, -vvv)')
@click.option('-c', '--colored', is_flag=True, default=False, help='Enable colored output')
def cli(verbose, colored):
  """CLI for taxometr"""
  printing.init(verbose, colored)
  config.load()


cli.add_command(task_group, 'task')
cli.add_command(action_group, 'action')
