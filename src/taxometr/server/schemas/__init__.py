from pydantic import BaseModel, Field, AfterValidator
from taxometr.common.validations import PrintableString
from datetime import datetime, timezone as tz, timedelta
from typing_extensions import Annotated, TypeAlias, Optional
from enum import Enum


class TaskParamsSchema(BaseModel):
  title: PrintableString = Field(max_length=1000)


class ActionParamsSchema(BaseModel):
  name: PrintableString = Field(max_length=1000)


class ActionFilterSchema(BaseModel):
  name: PrintableString = Field(default=None, max_length=1000)


def add_timezone(value: datetime):
  if value.tzinfo is None:
    return value.replace(tzinfo=tz.utc)
  return value


def time_start_current_day_utc():
  return datetime.now(tz=tz.utc).replace(hour=0, minute=0, second=0, microsecond=0)


def time_start_tomorrow_day_utc():
  return time_start_current_day_utc() + timedelta(days=1)


TimeWithTimezone: TypeAlias = Annotated[datetime, AfterValidator(add_timezone)]


class Column(str, Enum):
  TaskId = 'task_id'
  TaskName = 'task_name'
  ActionId = 'action_id'
  ActionName = 'action_name'
  Time = 'time'
  ActionTimeRanges = 'action_time_ranges'
  TimeHours = 'time_hours'


class SortingColumns(str, Enum):
  TaskId = 'task_id'
  TaskName = 'task_name'
  ActionId = 'action_id'
  ActionName = 'action_name'
  Time = 'time'
  TimeHours = 'time_hours'


class SortOrder(str, Enum):
  ask = 'ask'
  desk = 'desk'


class ReportTimingsFilterSchema(BaseModel):
  class TimeRangeFilter(BaseModel):
    since: TimeWithTimezone = Field(default_factory=time_start_current_day_utc)
    until: TimeWithTimezone = Field(default_factory=time_start_tomorrow_day_utc)

  time_range: Optional[TimeRangeFilter] = TimeRangeFilter()

