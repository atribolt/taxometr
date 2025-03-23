from peewee import (
  Model,
  AutoField,
  BigAutoField,
  CharField,
  ForeignKeyField
)
from playhouse.shortcuts import ThreadSafeDatabaseMetadata


class LabelDao(Model):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'label'

  id = BigAutoField(primary_key=True, null=False)
  name = CharField(max_length=255, unique=True)


class TaskDao(Model):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'task'

  id = AutoField(primary_key=True, null=False)
  title = CharField(max_length=255, null=False, unique=True)


class TaskLabelLinkDao(Model):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'task_label_link'

  task = ForeignKeyField(TaskDao, primary_key=True)
  label = ForeignKeyField(LabelDao, primary_key=True)
