from typing import Type
from taxometr.dao import BaseTaskDAO, BaseActionDAO


class DaoFactory:
  ActionDAO: Type[BaseActionDAO] = None
  TaskDAO: Type[BaseTaskDAO] = None

  def get_action_dao(self):
    return self.ActionDAO()

  def get_task_dao(self):
    return self.TaskDAO()
