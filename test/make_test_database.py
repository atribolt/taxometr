import sys
from taxometr.database import LabelDao, TaskDao, TimingsDao, TaskLabelLinkDao, TABLES
from peewee import SqliteDatabase
from datetime import datetime, timezone, timedelta


DATABASE = 'database.db'


SCHEMA = [
  {
    'title': 'task 1',
    'labels': ['test 1'],
    'start': datetime.now(tz=timezone.utc),
    'finish': datetime.now(tz=timezone.utc) + timedelta(days=1)
  },
  {
    'title': 'task 2',
    'labels': ['test 1', 'test 2'],
    'start': datetime.now(tz=timezone.utc),
    'finish': datetime.now(tz=timezone.utc) + timedelta(days=1)
  },
  {
    'title': 'task 3',
    'labels': ['test 3'], 
    'start': datetime.now(tz=timezone.utc),
    'finish': datetime.now(tz=timezone.utc) + timedelta(days=1)
  }
]


def main():
  database = SqliteDatabase(DATABASE)
  database.bind(TABLES)

  [x.create_table() for x in TABLES]

  for t in SCHEMA:
    task = TaskDao.create(title=t['title'])
    
    for l in t['labels']:
      label, _ = LabelDao.get_or_create(name=l)
      TaskLabelLinkDao.create(task=task, label=label)
    
    TimingsDao.create(
      task=task,
      start=t['start'],
      finish=t['finish']
    )

  return 0


if __name__ == '__main__':
  sys.exit(main())
