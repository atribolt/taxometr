from typing import Iterable
from peewee import Model, BigAutoField, TextField
from playhouse.shortcuts import ThreadSafeDatabaseMetadata


class Task:
  id: int
  title: str


class TaskDB(Model):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'task'

  id = BigAutoField()
  title = TextField()

  @staticmethod
  def new(task: Task) -> Task:
    result, created = TaskDB.get_or_create(
      title=task.title
    )

    if not created:
      raise ValueError('task same properties is exists')

    task.id = result.id
    return task

  @staticmethod
  def get_task(task_id: int) -> Task:
    result = TaskDB.get_or_none(task_id)
    if result is None:
      raise ValueError('task with id #{} is not exists'.format(task_id))
    return tdb_to_task(TaskDB.get())

  @staticmethod
  def get_tasks(task_title: str = None,
                offset: int = 0,
                count: int = 0) -> Iterable[Task]:
    query = TaskDB.select()

    if task_title:
      query = query.where(TaskDB.title.contains(task_title))

    if offset:
      query = query.offset(offset)

    if count:
      query = query.limit(count)

    return map(tdb_to_task, query)

  @staticmethod
  def update_task(task: Task):
    if task.id is None or task.id < 0 or not task.title:
      raise ValueError('task id or task title is empty')

    instance: TaskDB = TaskDB.get_or_none(task.id)
    if instance is None:
      raise ValueError('task with id #{} is not exists'.format(task.id))

    instance.title = task.title
    instance.save()

  @staticmethod
  def delete_task(task_id: int):
    if task_id is None or task_id < 0:
      raise ValueError('task id or task title is empty')

    instance: TaskDB = TaskDB.get_or_none(task_id)
    if instance is None:
      raise ValueError('task with id #{} is not exists'.format(task_id))

    instance.delete_instance(recursive=True)


def tdb_to_task(result: TaskDB):
  task = Task()
  task.id = result.id
  task.title = result.title
  return task
