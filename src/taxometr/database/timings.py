from peewee import (
  Model,
  BigAutoField,
  DateTimeField,
  ForeignKeyField
)
from playhouse.shortcuts import ThreadSafeDatabaseMetadata
from taxometr.database.task import TaskDao


class TimeingsDao(Model):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'timings'

  id = BigAutoField(primary_key=True, null=False)
  task = ForeignKeyField(TaskDao)
  start = DateTimeField(null=False)
  finish = DateTimeField(null=True)
