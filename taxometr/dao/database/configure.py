from peewee import Database
from pydantic import BaseModel


ConnectionArgs: list
ConnectionKwargs: dict

DatabaseType: Database
GlobalConnection: Database


class DatabaseConfig(BaseModel):
  type: str = 'sqlite'
  dbname: str = './taxometr.db'
  host: str = 'sqlite'
  port: int = 5432
  user: str = 'postgres'
  password: str = 'postgres'


def create_tables():
  from taxometr.dao.database import TABLES

  db: Database = DatabaseType(*ConnectionArgs, **ConnectionKwargs)
  with db.bind_ctx(TABLES):
    for table in TABLES:
      if not table.table_exists():
        table.create_table()


def load(config: DatabaseConfig):
  global GlobalConnection

  types = {
    'sqlite': load_sqlite,
    'postgre': load_postgres
  }

  if config.type not in types:
    raise ValueError('invalid database type %s, allow %s' % (config.type, types.keys()))

  types[config.type](config)
  create_tables()

  from taxometr.dao.database import TABLES
  GlobalConnection = DatabaseType(ConnectionArgs)
  GlobalConnection.bind(TABLES)


def load_sqlite(config: DatabaseConfig):
  global DatabaseType, ConnectionArgs, ConnectionKwargs
  from peewee import SqliteDatabase

  DatabaseType = SqliteDatabase
  ConnectionArgs = [str(config.dbname)]
  ConnectionKwargs = {}


def load_postgres(config: DatabaseConfig):
  global DatabaseType, ConnectionArgs, ConnectionKwargs
  from peewee import PostgresqlDatabase

  DatabaseType = PostgresqlDatabase
  ConnectionArgs = [str(config.dbname)]
  ConnectionKwargs = dict(
    user=config.user,
    password=config.password,
    host=config.host,
    port=config.port,
    dbname=config.dbname
  )
