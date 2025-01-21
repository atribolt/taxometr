import logging
import json
import flask
import taxometr.server.errors as err
from taxometr.database import (
  TaskDB,
  ActionDB,
  TimeRangeDB
)
from taxometr.server.routes import logger_required
from pydantic import BaseModel, Field, AfterValidator
from typing_extensions import Annotated
from typing import Optional, TypeAlias, Iterable
from dataclasses import dataclass, asdict, Field as DataClassField
from datetime import datetime, timezone as tz, timedelta
from enum import Enum
from itertools import groupby


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
  State = 'state'
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


class FilterSchema(BaseModel):
  class TimeRangeFilter(BaseModel):
    since: TimeWithTimezone = Field(default_factory=time_start_current_day_utc)
    until: TimeWithTimezone = Field(default_factory=time_start_tomorrow_day_utc)

  time_range: Optional[TimeRangeFilter] = TimeRangeFilter()


@dataclass
class ReportRecord:
  @dataclass
  class TimeRange:
    begin: str
    end: str | None = None

  task_id: int = 0
  task_name: str = ''
  action_id: int = 0
  action_name: str = ''
  time_seconds: int = 0
  state: str = 'pause'
  action_time_ranges: list[TimeRange] | None = None


@logger_required
def get_timing_report(logger: logging.Logger):
  filters_object = json.loads(flask.request.args.get('filter', '{}'))
  filters = FilterSchema.model_validate(filters_object)

  logging.debug('filters: %s', filters)

  query = TimeRangeDB.select().where(
    (TimeRangeDB.end_utc >= filters.time_range.since) &
    (TimeRangeDB.begin_utc <= filters.time_range.until)
  )

  result: list[dict] = []

  for action, times in groupby(query, key=lambda x: x.action):
    logger.debug('action: %s', action)
    action: ActionDB
    times: Iterable[TimeRangeDB]

    record = ReportRecord()
    record.task_id = action.task.id
    record.task_name = action.task.title
    record.action_id = action.id
    record.action_name = action.description
    record.action_time_ranges = []

    for time in times:
      begin_time_utc = time.begin()
      end_time_utc = time.end()

      if end_time_utc is None:
        record.state = 'active'
        end_time_utc = datetime.now(tz=tz.utc)

      if begin_time_utc < filters.time_range.since:
        begin_time_utc = filters.time_range.since

      if end_time_utc > filters.time_range.until:
        end_time_utc = filters.time_range.until

      record.time_seconds += (end_time_utc - begin_time_utc).total_seconds()
      record.action_time_ranges.append(
        ReportRecord.TimeRange(
          begin=time.begin_utc.isoformat(),
          end=time.end_utc.isoformat() if time.end_utc else None
        )
      )

    result.append(asdict(record))

  return result
