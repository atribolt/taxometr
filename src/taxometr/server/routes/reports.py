import flask
from taxometr.database import ActionDB, TimeRangeDB
from typing import Iterable
from dataclasses import dataclass, asdict
from datetime import datetime, timezone as tz
from itertools import groupby
from taxometr.server.routes import JsonQueryField
from taxometr.server.schemas import ReportTimingsFilterSchema


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


report_handler = flask.Blueprint('reports', __name__, '/report')


@report_handler.get('/timings')
@JsonQueryField('filter', ReportTimingsFilterSchema)
def get_timing_report(filters: ReportTimingsFilterSchema):
  logger = flask.current_app.logger

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
