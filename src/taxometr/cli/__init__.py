import click
from pathlib import Path


class CliConfig:
  ssl_cert = Path('~/.config/taxometr/server.crt').expanduser()

  if ssl_cert.exists():
    taxometr_server = 'https://localhost:8273'
  else:
    taxometr_server = 'https://localhost:8270'


ReadableFile = click.Path(exists=True, readable=True, dir_okay=False, path_type=Path)
