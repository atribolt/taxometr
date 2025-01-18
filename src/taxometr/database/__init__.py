from .task import Task, TaskDB
from .action import Action, ActionDB
from .time_range import TimeRange, TimeRangeDB


TABLES = [
  TaskDB,
  ActionDB,
  TimeRangeDB
]


def get_connection():
  from .configure import DatabaseType, ConnectionArgs, ConnectionKwargs
  return DatabaseType(*ConnectionArgs, **ConnectionKwargs)
