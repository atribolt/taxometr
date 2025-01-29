import click
from pathlib import Path
from click import DateTime


class CliConfig:
  taxometr_server: str = None


ReadableFile = click.Path(exists=True, readable=True, dir_okay=False, path_type=Path)
Date = DateTime(formats=['%Y-%m-%d', '%H:%M:%S', '%Y-%m-%d %H:%M:%S'])


context = click.make_pass_decorator(CliConfig, True)


class Error(click.UsageError):
  
