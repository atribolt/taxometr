from datetime import datetime
from taxometr.timings import BaseConverter


class Converter:
  _converters: list[BaseConverter] = []

  @staticmethod
  def convert(dt: datetime) -> datetime:
    """Apply converters to datetime"""
    for converter in Converter._converters:
      dt = converter.apply(dt)
    return dt

  @staticmethod
  def add_converter(converter: BaseConverter):
    Converter._converters.append(converter)
