from pydantic import BaseModel
from taxometr.dao.factory import DaoFactory


class DaoConfigure(BaseModel):
  backend: str = 'database'
  properties: dict = {}


def load_database_backend(config: DaoConfigure):
  from taxometr.dao.database import TaskDB, ActionDB, TimeRangeDB, configure
  configure.load(configure.DatabaseConfig.model_validate(config.properties))

  DaoFactory.ActionDAO = ActionDB
  DaoFactory.TaskDAO = TaskDB
  DaoFactory.TimeRangeDAO = TimeRangeDB


BACKENDS = {
  'database': load_database_backend
}


def load(config: DaoConfigure):
  if config.backend not in BACKENDS:
    raise ValueError('invalid dao backend {}, expected {}'.format(
      config.backend, list(BACKENDS)
    ))

  BACKENDS[config.backend](config)
