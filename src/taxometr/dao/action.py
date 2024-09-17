from typing import Iterable, Optional
from datetime import datetime, timezone
from taxometr.dao import Task


class TimeRange:
  id: int
  begin: datetime
  end: datetime

  @property
  def total_time(self):
    end = self.end or datetime.now(timezone.utc).replace(microsecond=0)
    return end - self.begin


class Action:
  id: int = None
  task: Task = None
  description: str = None


class BaseActionDAO:
  def new(self, properties: Action) -> Action:
    raise NotImplementedError()

  def get_action(self, action_id: int) -> Action:
    raise NotImplementedError()

  def get_actions(self, action_ids: Optional[Iterable[int]] = None) -> Iterable[Action]:
    raise NotImplementedError()

  def get_actions_by_time(self, since: Optional[datetime], until: Optional[datetime]) -> Iterable[Action]:
    raise NotImplementedError()

  def get_active_action(self) -> Action | None:
    raise NotImplementedError()

  def get_actions_by_task(self, task: Task) -> Iterable[Action]:
    raise NotImplementedError()

  def stop_all_actions(self):
    raise NotImplementedError()

  def start_action(self, action_id: int) -> bool:
    raise NotImplementedError()

  def get_action_timings(self, action: Action, since: datetime = None, until: datetime = None) -> Iterable[TimeRange]:
    raise NotImplementedError()
