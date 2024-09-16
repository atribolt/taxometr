from typing import Iterable


class Task:
  id: int
  title: str


class BaseTaskDAO:
  def new(self, properties: Task) -> Task:
    raise NotImplementedError()

  def get_task(self, task_id: int) -> Task:
    raise NotImplementedError()

  def get_tasks(self, task_ids: Iterable[int] = None) -> Iterable[Task]:
    raise NotImplementedError()
