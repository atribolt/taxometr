import click
import taxometr.cli as tcli


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


if __name__ == '__main__':
  cli()
