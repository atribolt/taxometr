from peewee import Model, BigAutoField, ForeignKeyField, TimestampField
from playhouse.shortcuts import ThreadSafeDatabaseMetadata
from taxometr.dao.database import ActionDB
from datetime import timezone as tz


class TimeRangeDB(Model):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'times'

  id = BigAutoField()
  action = ForeignKeyField(ActionDB)
  begin_utc = TimestampField(utc=True, resolution=1)
  end_utc = TimestampField(null=True, resolution=1)

  def begin(self):
    return self.begin_utc.replace(tzinfo=tz.utc)

  def end(self):
    return self.end_utc.replace(tzinfo=tz.utc) if self.end_utc else None
