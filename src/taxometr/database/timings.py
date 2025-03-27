import logging
from peewee import (
  Model,
  BigAutoField,
  DateTimeField,
  ForeignKeyField
)
from playhouse.shortcuts import ThreadSafeDatabaseMetadata
from taxometr.database.task import TaskDao
from typing import Optional
from datetime import datetime, timezone


def current_time_utc():
  return datetime.now(tz=timezone.utc)


def logger():
  return logging.getLogger('dao.timings')


class TimingsDao(Model):
  """The accessor to database 'timings' table"""

  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'timings'

  id = BigAutoField(primary_key=True, null=False)
  task = ForeignKeyField(TaskDao)
  start = DateTimeField(null=False, default=current_time_utc)
  finish = DateTimeField(null=True)

  @staticmethod
  def get_active_task() -> Optional[TaskDao]:
    """Search and return current active task"""

    timing = TimingsDao.select(TimingsDao.task, TimingsDao.finish).order_by(TimingsDao.id.desc()).get_or_none()
    if timing is not None and timing.finish is None:
      return timing.task

  @staticmethod
  def stop_active_task() -> Optional[TaskDao]:
    """Finish active task and return it if it exists"""

    log = logger()

    task = TimingsDao.get_active_task()
    if task is not None:
      TimingsDao.update(finish=datetime.now(tz=timezone.utc)).where(TimingsDao.finish.is_null())
      log.info('%r stopped', task)
      return task

  @staticmethod
  def start_task(task: TaskDao, stop_other: bool = True):
    log = logger()

    active_task = TimingsDao.get_active_task()
    if active_task is not None:
      if active_task == task:
        log.debug('%r already is active', task)
        return
      elif stop_other:
        log.debug('%r active now, stop it', active_task)
        TimingsDao.stop_active_task()
      else:
        log.error('%r active and "stop_other" is "False"')
        raise RuntimeError("New task can't be start while other is active")
    else:
      tm = TimingsDao.create(task=task)
      log.info('%r started: %r', task, tm)
