import flask
from taxometr.database import ActionDB, TimeRangeDB
from typing import Iterable
from dataclasses import dataclass, asdict
from datetime import datetime, timezone as tz
from itertools import groupby
from taxometr.server.routes import JsonQueryField
from taxometr.server.schemas import ReportTimingsFilterSchema


@dataclass
class TimeRange:
  since: str = None
  until: str = None


@dataclass
class ActionTimeRange:
  begin: str
  end: str | None = None


@dataclass
class ActionInfo:
  task_id: int = 0
  task_name: str = ''
  action_id: int = 0
  action_name: str = ''
  time_seconds: int = 0
  action_time_ranges: list[ActionTimeRange] | None = None


@dataclass
class Report:
  time_range: TimeRange = None
  total_seconds: int = 0
  actions: list[ActionInfo] = None


report_handler = flask.Blueprint('reports', __name__, url_prefix='/report')


@report_handler.get('/timings')
@JsonQueryField('filter', ReportTimingsFilterSchema)
def get_timing_report(filters: ReportTimingsFilterSchema):
  logger = flask.current_app.logger

  query = TimeRangeDB.select().where(
    ((TimeRangeDB.end_utc >= filters.time_range.since) | TimeRangeDB.end_utc.is_null()) &
    (TimeRangeDB.begin_utc <= filters.time_range.until)
  )

  report = Report(
    TimeRange(
      since=filters.time_range.since.isoformat(),
      until=filters.time_range.until.isoformat()
    )
  )

  report.actions = []

  for action, times in groupby(query, key=lambda x: x.action):
    logger.debug('action: %s', action)
    action: ActionDB
    times: Iterable[TimeRangeDB]

    action_info = ActionInfo()
    action_info.task_id = action.task.id
    action_info.task_name = action.task.title
    action_info.action_id = action.id
    action_info.action_name = action.description
    action_info.action_time_ranges = []

    for time in times:
      begin_time_utc = time.begin()
      end_time_utc = time.end(datetime.now(tz=tz.utc))

      if begin_time_utc < filters.time_range.since:
        begin_time_utc = filters.time_range.since

      if end_time_utc > filters.time_range.until:
        end_time_utc = filters.time_range.until

      action_info.time_seconds += (end_time_utc - begin_time_utc).total_seconds()
      action_info.action_time_ranges.append(
        ActionTimeRange(
          begin=time.begin_utc.replace(tzinfo=tz.utc).isoformat(),
          end=time.end_utc.replace(tzinfo=tz.utc).isoformat() if time.end_utc else None
        )
      )

    report.total_seconds += action_info.time_seconds
    report.actions.append(action_info)

  return asdict(report)
