import click
from taxometr.cli import context, CliConfig, printing, commands


@click.group()
@click.option('-v', '--verbose', count=True,
              default=False, help='Enable verbose output (-v, -vv, -vvv)')
@click.option('-C', '--colored', is_flag=True, default=False, help='Enable colored output')
@click.option('-u', '--url', 'url', type=str, help='URL to taxometr server', default=None)
@context
def cli(ctx: CliConfig, verbose, colored, url: str | None):
  """CLI for taxometr"""
  printing.init(verbose, colored)

  if url is None or not url:
    url = 'http://localhost'
    printing.debug('server url set as default: %s', url)

  ctx.taxometr_server = url
  # TODO add check to alive server


cli.add_command(commands.task_group, 'task')
cli.add_command(commands.action_group, 'action')
cli.add_command(commands.report_group, 'report')


if __name__ == '__main__':
  cli()
