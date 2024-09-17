import logging
import click
from typing import Iterable
from functools import partial


DEBUG_STYLE = partial(click.style, fg='bright_black')
WARNING_STYLE = partial(click.style, fg='yellow')
ERROR_STYLE = partial(click.style, fg='red')


def debug(fmt, *args, **kwargs):
  click.echo(DEBUG_STYLE(fmt.format(*args, **kwargs)))


def warning(fmt, *args, **kwargs):
  click.echo(WARNING_STYLE(fmt.format(*args, **kwargs)))


def error(fmt, *args, **kwargs):
  click.echo(ERROR_STYLE(fmt.format(*args, **kwargs)))


def echo(fmt, *args, **kwargs):
  click.echo(fmt.format(*args, **kwargs))


class Colored(logging.Formatter):
  def __init__(self, *argv, **kwargs):
    super().__init__(*argv, **kwargs)

  def formatMessage(self, record: logging.LogRecord) -> str:
    msg = super().formatMessage(record)

    match record.levelno:
      case logging.DEBUG:
        return DEBUG_STYLE(msg)
      case logging.WARNING:
        return WARNING_STYLE(msg)
      case logging.ERROR:
        return ERROR_STYLE(msg)

    return msg


def init(verbose, colored):
  global debug, DEBUG_STYLE, WARNING_STYLE, ERROR_STYLE

  if not verbose:
    debug = lambda *_, **__: None

  if not colored:
    DEBUG_STYLE = WARNING_STYLE = ERROR_STYLE = lambda msg: msg

  if verbose > 0:
    import logging.config as lc

    lc.dictConfig({
      'version': 1,
      'formatters': {
        'colored': {
          '()': 'taxometr.cli.printing.Colored',
          'format': '%(levelname)s : (%(name)s) : %(message)s'
        }
      },
      'filters': {},
      'handlers': {
        'console': {
          'class': 'logging.StreamHandler',
          'filters': [],
          'formatter': 'colored',
          'stream': 'ext://sys.stdout'
        }
      },
      'root': {
        'level': logging.DEBUG if verbose >= 2 else logging.INFO,
        'handlers': ['console']
      },
      'disable_existing_loggers': verbose < 3
    })
  else:
    logging.basicConfig(level=logging.CRITICAL)


class Table:
  import tabulate

  def __init__(self, *headers):
    self.headers: list[str] = []
    self.table: list[Iterable[str]] = []

    self.set_headers(headers)

  def set_headers(self, *headers):
    self.headers = list(*headers)

  def add_row(self, row: list):
    self.table.append(row)

  def __str__(self):
    table = self.table or [[]]
    return self.tabulate.tabulate(table, headers=self.headers, tablefmt='simple_grid', maxcolwidths=100)
