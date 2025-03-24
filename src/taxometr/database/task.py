from peewee import (
  Model,
  AutoField,
  BigAutoField,
  CharField,
  ForeignKeyField,
  CompositeKey
)
from typing import Iterable
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

  @staticmethod
  def search_by_labels(labels: Iterable[str | LabelDao]) -> Iterable['TaskDao']:
    return (
      TaskDao.select()
        .join(TaskLabelLinkDao)
        .join(LabelDao)
      .where(LabelDao.name.in_(labels))
      .group_by(TaskDao)
    )


class TaskLabelLinkDao(Model):
  class Meta(ThreadSafeDatabaseMetadata):
    table_name = 'task_label_link'
    primary_key = CompositeKey('task', 'label')

  task = ForeignKeyField(TaskDao)
  label = ForeignKeyField(LabelDao)
