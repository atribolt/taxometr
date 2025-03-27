from peewee import SqliteDatabase
from taxometr.database import TaskDao, TaskLabelLinkDao, LabelDao, TimingsDao, TABLES


db = SqliteDatabase('database.db')
db.bind(TABLES)


def test_get_active_task():
	assert TimingsDao.get_active_task().title == 'task 3'


def test_select_by_labels():
	list0 = TaskDao.search_by_labels(('test 1', 'test 3'))
	assert len(list0) == 3

	list1 = TaskDao.search_by_labels(('test 1', 'test 2'))
	assert len(list1) == 2

def test_start_stop_task():
	active_task = TimingsDao.get_active_task()
	assert active_task.title == 'task 3'

	stopped_task = TimingsDao.stop_active_task()
	assert active_task == stopped_task

	TimingsDao.start_task(stopped_task)
	started_task = TimingsDao.get_active_task()
	assert stopped_task == started_task
