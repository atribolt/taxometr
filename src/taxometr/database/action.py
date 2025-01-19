from datetime import datetime, timezone as tz
from typing import Iterable, Optional
from peewee import Model, BigAutoField, ForeignKeyField, TextField
from playhouse.shortcuts import ThreadSafeDatabaseMetadata
from taxometr.database.task import Task, TaskDB


class Action:
  id: int = None
  task: Task = None
  description: str = None

  def __str__(self):
    return 'Action({}, {}, {})'.format(self.id, self.task, self.description)


class ActionDB(Model):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'action'

  id = BigAutoField()
  task = ForeignKeyField(TaskDB)
  description = TextField()

  @staticmethod
  def new(action: Action) -> Action:
    result, created = ActionDB.get_or_create(
      task=action.task.id,
      description=action.description
    )

    if not created:
      raise ValueError('action same properties is exists')

    action.id = result.id
    action.task.title = result.task.title
    return action

  @staticmethod
  def get_action(action_id: int) -> Action:
    result = ActionDB.select().join(TaskDB).where(ActionDB.id == action_id).get()
    return dbrow_to_action(result)

  @staticmethod
  def get_actions_by_task(task: Task, name_template: str | None = None) -> Iterable[Action]:
    query = ActionDB.select().join(TaskDB).where(ActionDB.task == task.id)
    if name_template is not None:
      query = query.where(ActionDB.description.contains(str(name_template)))

    return map(dbrow_to_action, query)

  @staticmethod
  def delete_action(action: Action):
    if action.id is None or action.id < 0:
      raise ValueError('action id invalid')

    instance: ActionDB = ActionDB.get_or_none(action.id)
    if instance is None:
      raise ValueError('action with id #{} is not exists'.format(action.id))

    instance.delete_instance(recursive=True)

  @staticmethod
  def update_action(action: Action):
    if action.id is None or action.id < 0:
      raise ValueError('action id invalid')

    instance: ActionDB = ActionDB.get_or_none(action.id)
    if instance is None:
      raise ValueError('action with id #{} is not exists'.format(action.id))

    instance.description = action.description
    instance.save()
    return dbrow_to_action(instance)

  def get_actions(self, action_ids: Optional[Iterable[int]] = None) -> Iterable[Action]:
    query = ActionDB.select().join(TaskDB)
    if action_ids:
      query = query.where(ActionDB.id.in_(action_ids))
    return map(dbrow_to_action, query)

  def get_actions_by_time(self, since: Optional[datetime], until: Optional[datetime]) -> Iterable[Action]:
    from taxometr.database import TimeRangeDB

    query = ActionDB.select().join(TaskDB).switch(ActionDB).join(TimeRangeDB)
    if since:
      query = query.where(TimeRangeDB.begin_utc >= since)
    if until:
      query = query.where(TimeRangeDB.end_utc < until)
    query = query.group_by(ActionDB.id)
    return map(dbrow_to_action, query)

  def get_active_action(self) -> Action | None:
    from taxometr.database import TimeRangeDB

    query = ActionDB.select().join(TaskDB).switch(ActionDB).join(TimeRangeDB).where(TimeRangeDB.end_utc.is_null())
    result = query.get_or_none()
    if result is None:
      return result
    return dbrow_to_action(result)

  def stop_all_actions(self):
    from taxometr.database import TimeRangeDB
    TimeRangeDB.update(end_utc=datetime.now(tz.utc)).where(TimeRangeDB.end_utc.is_null()).execute()

  def start_action(self, action_id: int) -> bool:
    from taxometr.database import TimeRangeDB
    _, created = TimeRangeDB.get_or_create(action_id=action_id, end_utc=None)
    return created


def dbrow_to_action(result: ActionDB):
  action = Action()
  action.id = result.id
  action.task = Task()
  action.task.id = result.id
  action.task.title = result.task.title
  action.description = result.description
  return action
