from datetime import datetime, timedelta


class Converter:
  _converters: list['BaseConverter'] = []

  @staticmethod
  def convert(dt: datetime) -> datetime:
    """Apply converters to datetime"""
    for converter in Converter._converters:
      dt = converter.apply(dt)
    return dt

  @staticmethod
  def add_converter(converter: 'BaseConverter'):
    Converter._converters.append(converter)


class BaseConverter:
  def apply(self, dt: datetime) -> datetime:
    """Convert datetime"""


class SecondsReounding(BaseConverter):
  """Округление микросекунд до секунд, и секунд до минут вверх"""

  def apply(self, dt: datetime) -> datetime:
    dt += timedelta(minutes=1)
    return dt.replace(second=0, microsecond=0)


class MinuteDecimalRounding(BaseConverter):
  """Округление минут до десяток"""
  def __init__(self, threshold: int):
    """
    :param threshold: Threshold minutes for round up or down
    """
    if 0 >= threshold >= 10:
      raise ValueError('Valid values [1-9]')

    self.threshold = threshold

  def apply(self, dt: datetime) -> datetime:
    minutes = dt.minute
    n = minutes % 10
    if n < self.threshold:
      minutes -= n
    else:
      minutes += (10 - n)

    return dt.replace(minute=minutes)
