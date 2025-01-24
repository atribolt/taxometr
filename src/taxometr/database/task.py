from typing import Iterable
from peewee import Model, BigAutoField, TextField
from playhouse.shortcuts import ThreadSafeDatabaseMetadata


class TaskDB(Model):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'task'

  id = BigAutoField()
  title = TextField()

  def __str__(self):
    return 'Task({}, {})'.format(self.id, self.title)

  @staticmethod
  def new(task_title: str) -> 'TaskDB':
    result, created = TaskDB.get_or_create(
      title=task_title
    )
    if not created:
      raise ValueError('task same properties is exists')
    return result

  @staticmethod
  def get_task(task_id: int) -> 'TaskDB':
    result = TaskDB.get_or_none(task_id)
    if result is None:
      raise RuntimeError('task with id #{} is not exists'.format(task_id))
    return result

  @staticmethod
  def get_tasks(task_title: str = None,
                offset: int = 0,
                count: int = 0) -> Iterable['TaskDB']:
    query = TaskDB.select()

    if task_title:
      query = query.where(TaskDB.title.contains(task_title))

    if offset:
      query = query.offset(offset)

    if count:
      query = query.limit(count)

    return query

  @staticmethod
  def update_task(task: 'TaskDB'):
    if task.id is None or task.id < 0 or not task.title:
      raise ValueError('task id or task title is empty')

    instance: TaskDB = TaskDB.get_or_none(task.id)
    if instance is None:
      raise ValueError('task with id #{} is not exists'.format(task.id))

    if task.title != instance.title:
      instance.title = task.title
      instance.save()

  @staticmethod
  def delete_task(task: 'TaskDB'):
    if task.id is None or task.id < 0:
      raise ValueError('task id invalid')

    instance: TaskDB = TaskDB.get_or_none(task.id)
    if instance is None:
      raise ValueError('task with id #{} is not exists'.format(task.id))

    instance.delete_instance(recursive=True)
