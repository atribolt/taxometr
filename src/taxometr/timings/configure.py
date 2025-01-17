import logging
from pydantic import BaseModel, Field


class RoundMinutesConfig(BaseModel):
  enabled: bool = True
  threshold: int = Field(default=5, ge=1, le=9)


class RoundingConfig(BaseModel):
  roundSeconds: bool = True
  roundMinutes: RoundMinutesConfig = RoundMinutesConfig()


def load(config: RoundingConfig):
  log = logging.getLogger('rounding.configure')

  from taxometr.timings import Converter, SecondsReounding, MinuteDecimalRounding
  if config.roundSeconds:
    log.debug('append second rounging')
    Converter.add_converter(SecondsReounding())

  if config.roundMinutes.enabled:
    log.debug('append minute rounding with threshold "%i minutes"', config.roundMinutes.threshold)
    Converter.add_converter(MinuteDecimalRounding(config.roundMinutes.threshold))

  log.debug('completed')
