import click
from pathlib import Path
from click import DateTime
from . import printing
from urllib.parse import urljoin
import requests as req


class CliConfig:
  taxometr_server: str = None


ReadableFile = click.Path(exists=True, readable=True, dir_okay=False, path_type=Path)
Date = DateTime(formats=['%Y-%m-%d', '%H:%M:%S', '%Y-%m-%d %H:%M:%S'])


context = click.make_pass_decorator(CliConfig, True)





@click.group()
@click.option('-v', '--verbose', count=True,
              default=False, help='Enable verbose output (-v, -vv, -vvv)')
@click.option('-C', '--colored', is_flag=True, default=False, help='Enable colored output')
@click.option('-u', '--url', 'url', type=str, help='URL to taxometr server',
              default='http://localhost', show_default=True)
@context
def cli(ctx: CliConfig, verbose, colored, url: str | None):
  """CLI for taxometr"""
  printing.init(verbose, colored)

  ctx.taxometr_server = url

  reply = req.get(urljoin(ctx.taxometr_server, '/v1/echo'))
