from peewee import (
  Model,
  BigAutoField,
  DateTimeField,
  ForeignKeyField
)
from playhouse.shortcuts import ThreadSafeDatabaseMetadata
from taxometr.database.task import TaskDao
from typing import Optional


class TimingsDao(Model):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'timings'

  id = BigAutoField(primary_key=True, null=False)
  task = ForeignKeyField(TaskDao)
  start = DateTimeField(null=False)
  finish = DateTimeField(null=True)

  @staticmethod
  def get_active_task() -> Optional[TaskDao]:
    timing = TimingsDao.select(TimingsDao.task, TimingsDao.finish).order_by(TimingsDao.id.desc()).get_or_none()
    if timing is not None and timing.finish is None:
      return timing.task
