from typing import Iterable
from peewee import Model, BigAutoField, TextField
from taxometr.dao import BaseTaskDAO, Task
from playhouse.shortcuts import ThreadSafeDatabaseMetadata


class TaskDB(Model, BaseTaskDAO):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'task'

  id = BigAutoField()
  title = TextField()

  def new(self, task: Task) -> Task:
    result, created = TaskDB.get_or_create(
      title=task.title
    )

    if not created:
      raise ValueError('task same properties is exists')

    task.id = result.id
    return task

  def get_task(self, task_id: int) -> Task:
    result = TaskDB.get_or_none(task_id)
    if result is None:
      raise ValueError('task with id #{} is not exists'.format(task_id))
    return tdb_to_task(TaskDB.get())

  def get_tasks(self, task_ids: Iterable[int] = None) -> Iterable[Task]:
    query = TaskDB.select()
    if task_ids:
      query.where(TaskDB.id.in_(task_ids))
    return map(tdb_to_task, query)


def tdb_to_task(result: TaskDB):
  task = Task()
  task.id = result.id
  task.title = result.title
  return task
