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

  def end(self) -> datetime | None:
    return to_local_time(self.end_utc) if self.end_utc else None

  def total_time(self) -> timedelta:
    end = self.end_utc or datetime.now()
    return end - self.begin()
