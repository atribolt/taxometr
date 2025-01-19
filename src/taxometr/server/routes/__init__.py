import flask
import logging
from functools import wraps


def logger_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    logger = getattr(flask.app, 'logger', logging.getLogger(func.__name__))
    return func(logger, *args, **kwargs)

  return wrapper
