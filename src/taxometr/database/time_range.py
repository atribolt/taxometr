import time
from peewee import Model, BigAutoField, ForeignKeyField, TimestampField
from playhouse.shortcuts import ThreadSafeDatabaseMetadata
from taxometr.database.action import ActionDB
from datetime import timezone as tz, timedelta, datetime


def to_local_time(tm):
  offset = timedelta(seconds=-time.timezone)
  tzname = time.tzname[0] if time.tzname else None
  local_zone = tz(offset, tzname)
  return (tm + offset).replace(tzinfo=local_zone)


class TimeRangeDB(Model):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'times'

  id = BigAutoField()
  action = ForeignKeyField(ActionDB)
  begin_utc = TimestampField(utc=True, resolution=1)
  end_utc = TimestampField(null=True, resolution=1)

  def begin(self) -> datetime:
    return to_local_time(self.begin_utc)

  def end(self, default=None) -> datetime | None:
    assert isinstance(default, datetime), 'arg "default" should be "datetime.datetime" instance'
    return to_local_time(self.end_utc) if self.end_utc else default

  def total_time(self) -> timedelta:
    end = self.end_utc or datetime.now()
    return end - self.begin()

  @staticmethod
  def get_active_action():
    last_time: list[TimeRangeDB] = list(TimeRangeDB.select().order_by(TimeRangeDB.id.desc()).limit(1))
    if last_time:
      return last_time[0].action
    return None

  @staticmethod
  def stop_active_action():
    last_time: list[TimeRangeDB] = list(
      TimeRangeDB.select().order_by(TimeRangeDB.id.desc()).where(TimeRangeDB.end_utc.is_null()).limit(1)
    )
    if last_time:
      time_range = last_time[0]
      time_range.end_utc = datetime.now(tz=tz.utc)
      time_range.save()
      return True, time_range.action
    return False, None

  @staticmethod
  def start_action(action: ActionDB):
    TimeRangeDB.get_or_create(action_id=action.id, end_utc=None)
