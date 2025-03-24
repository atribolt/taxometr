from .task import TaskDao, TaskLabelLinkDao, LabelDao
from .timings import TimingsDao


TABLES = [
  TaskDao,
  TaskLabelLinkDao,
  LabelDao,
  TimingsDao
]