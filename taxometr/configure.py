import sys
import json
import logging
from pathlib import Path
from taxometr.dao.configure import (
  DaoConfigure, load as dao_configure
)


CONFIG_SECTIONS = {
  'data': (DaoConfigure, dao_configure)
}


def load_from_json(data: dict):
  log = logging.getLogger('configure')

  for section, (validator, confugrator) in CONFIG_SECTIONS.items():
    log.debug('load %s', section)
    if section not in data:
      log.warning('section "%s" not present in config, use default', section)
      confugrator(validator())
    else:
      confugrator(validator.model_validate(data[section]))


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

  config_paths = [
    './taxometr.json'
  ]

  if sys.platform == 'linux':
    config_paths += [
      '~/.config/taxometr/taxometr.json',
      '/etc/taxometr.json'
    ]
  elif sys.platform == 'nt':
    config_paths += [
      '~/AppData/Local/taxometr/taxometr.json',
    ]

  for config in map(Path, config_paths):
    log.debug('test config %s', config)
    if config.exists():
      load_from_file(config)
      return
  else:
    load_from_json({})
