import os
import sys
import json
import logging
from pathlib import Path
from taxometr.database.configure import (
  DatabaseConfig, load as database_configure
)
from taxometr.timings.configure import (
  RoundingConfig, load as rounding_configure
)


CONFIG_SECTIONS = {
  'data': (DatabaseConfig, database_configure),
  'rounding': (RoundingConfig, rounding_configure)
}


def load_from_json(data: dict):
  log = logging.getLogger('configure')

  for section, (validator, configurator) in CONFIG_SECTIONS.items():
    log.debug('check config object "%s"', section)

    model = None

    if section not in data:
      log.warning('section "%s" not present in config, load as default', section)
      model = validator()
    else:
      log.debug('loading config object "%s"', section)
      model = validator.model_validate(data[section])

    if callable(configurator):
      configurator(model)

  if os.environ.get('TAXOMETR_DEBUG_LOGGING'):
    from taxometr.log import init_debug_logging
    init_debug_logging()

  log.info('config loaded')


def load_from_file(config: Path = None):
  log = logging.getLogger('configure')
  if config is None:
    return load()

  log.info('load config from %s', config)

  with config.open('r') as file:
    data = json.load(file)

  load_from_json(data)


def load():
  log = logging.getLogger('configure')

  config_paths: list[Path] = [
    Path('./taxometr.json')
  ]

  if sys.platform == 'linux':
    config_paths += [
      Path('~/.config/taxometr/taxometr.json').expanduser(),
      Path('/etc/taxometr.json')
    ]
  elif sys.platform == 'nt':
    config_paths += [
      Path('~/AppData/Local/taxometr/taxometr.json').expanduser(),
    ]

  for config in config_paths:
    log.debug('test config %s', config)
    if config.exists():
      log.debug('load config %s', config)
      load_from_file(config)
      return
  else:
    load_from_json({})
