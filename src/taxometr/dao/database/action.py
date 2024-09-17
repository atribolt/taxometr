from datetime import datetime, timezone as tz
from typing import Iterable, Optional
from peewee import Model, BigAutoField, ForeignKeyField, TextField
from playhouse.shortcuts import ThreadSafeDatabaseMetadata

from taxometr.dao.action import TimeRange
from taxometr.dao.database import TaskDB
from taxometr.dao import BaseActionDAO, Action, Task


class ActionDB(Model, BaseActionDAO):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'action'

  id = BigAutoField()
  task = ForeignKeyField(TaskDB)
  description = TextField()

  def new(self, action: Action) -> Action:
    result, created = ActionDB.get_or_create(
      task=action.task.id,
      description=action.description
    )

    if not created:
      raise ValueError('action same properties is exists')

    action.id = result.id
    action.task.title = result.task.title
    return action

  def get_action(self, action_id: int) -> Action:
    result = ActionDB.select().join(TaskDB).where(ActionDB.id == action_id).get()
    return dbrow_to_action(result)

  def get_actions_by_task(self, task: Task) -> Iterable[Action]:
    query = ActionDB.select().join(TaskDB).where(ActionDB.task == task.id)
    return map(dbrow_to_action, query)

  def get_actions(self, action_ids: Optional[Iterable[int]] = None) -> Iterable[Action]:
    query = ActionDB.select().join(TaskDB)
    if action_ids:
      query = query.where(ActionDB.id.in_(action_ids))
    return map(dbrow_to_action, query)

  def get_actions_by_time(self, since: Optional[datetime], until: Optional[datetime]) -> Iterable[Action]:
    from taxometr.dao.database import TimeRangeDB

    query = ActionDB.select().join(TaskDB).switch(ActionDB).join(TimeRangeDB)
    if since:
      query = query.where(TimeRangeDB.begin_utc >= since)
    if until:
      query = query.where(TimeRangeDB.end_utc < until)
    query = query.group_by(ActionDB.id)
    return map(dbrow_to_action, query)

  def get_active_action(self) -> Action | None:
    from taxometr.dao.database import TimeRangeDB

    query = ActionDB.select().join(TaskDB).switch(ActionDB).join(TimeRangeDB).where(TimeRangeDB.end_utc.is_null())
    result = query.get_or_none()
    if result is None:
      return result
    return dbrow_to_action(result)

  def stop_all_actions(self):
    from taxometr.dao.database import TimeRangeDB
    TimeRangeDB.update(end_utc=datetime.now(tz.utc)).where(TimeRangeDB.end_utc.is_null()).execute()

  def start_action(self, action_id: int) -> bool:
    from taxometr.dao.database import TimeRangeDB
    _, created = TimeRangeDB.get_or_create(action_id=action_id, end_utc=None)
    return created

  def get_action_timings(self, action: Action, since: datetime = None, until: datetime = None) -> Iterable[TimeRange]:
    from taxometr.dao.database import TimeRangeDB
    query = TimeRangeDB.select().where(TimeRangeDB.action == action.id)
    if since:
      query = query.where(TimeRangeDB.begin_utc >= since)
    if until:
      query = query.where(TimeRangeDB.end_utc < until)
    return map(dbrow_to_time_range, query)


def dbrow_to_time_range(time_range_row):
  time_range = TimeRange()
  time_range.id = time_range_row.id
  time_range.begin = time_range_row.begin()
  time_range.end = time_range_row.end()
  return time_range


def dbrow_to_action(result: ActionDB):
  action = Action()
  action.id = result.id
  action.task = Task()
  action.task.id = result.id
  action.task.title = result.task.title
  action.description = result.description
  return action
