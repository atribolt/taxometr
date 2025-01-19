import time
from peewee import Model, BigAutoField, ForeignKeyField, TimestampField
from playhouse.shortcuts import ThreadSafeDatabaseMetadata
from taxometr.database.action import ActionDB
from datetime import timezone as tz, timedelta, datetime


class TimeRange:
  id: int
  begin: datetime
  end: datetime

  @property
  def total_time(self):
    end = self.end or datetime.now(tz.utc).replace(microsecond=0)
    return end - self.begin


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

  def begin(self):
    return to_local_time(self.begin_utc)

  def end(self):
    return to_local_time(self.end_utc) if self.end_utc else None



def dbrow_to_time_range(time_range_row):
  time_range = TimeRange()
  time_range.id = time_range_row.id
  time_range.begin = time_range_row.begin()
  time_range.end = time_range_row.end()
  return time_range