from peewee import Database
from pydantic import BaseModel, AnyUrl


ConnectionUrl: str
DatabaseType: Database
GlobalConnection: Database


class DatabaseConfig(BaseModel):
  type: str = 'sqlite'
  url: AnyUrl = './taxometr.db'


def create_tables():
  from taxometr.dao.database import TABLES

  db: Database = DatabaseType(ConnectionUrl)
  with db.bind_ctx(TABLES):
    for table in TABLES:
      if not table.table_exists():
        table.create_table()


def load(config: DatabaseConfig):
  global DatabaseType, ConnectionUrl, GlobalConnection

  from peewee import SqliteDatabase, PostgresqlDatabase
  types = {
    'sqlite': SqliteDatabase,
    'postgre': PostgresqlDatabase
  }

  if config.type not in types:
    raise ValueError('invalid database type %s, allow %s' % (config.type, types.keys()))

  DatabaseType = types[config.type]
  ConnectionUrl = config.url

  create_tables()

  from taxometr.dao.database import TABLES
  GlobalConnection = DatabaseType(ConnectionUrl)
  GlobalConnection.bind(TABLES)
