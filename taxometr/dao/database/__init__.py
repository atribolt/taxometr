from .task import TaskDB
from .action import ActionDB
from .time_range import TimeRangeDB


TABLES = [
  TaskDB,
  ActionDB,
  TimeRangeDB
]


def get_connection():
  from .configure import DatabaseType, ConnectionArgs, ConnectionKwargs
  return DatabaseType(*ConnectionArgs, **ConnectionKwargs)
