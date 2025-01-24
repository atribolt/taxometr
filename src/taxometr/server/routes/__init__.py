from pydantic import BaseModel
from typing import Type
import functools
import flask


class JsonRequest:
  def __init__(self, schema: Type[BaseModel]):
    self.schema = schema

  def __call__(self, func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      json_body = flask.request.json
      obj = self.schema.model_validate(json_body)
      return func(obj, *args, **kwargs)
    return wrapper


class JsonQueryField:
  def __init__(self, field: str, schema: Type[BaseModel], required: bool = False):
    self.field = field
    self.schema = schema
    self.required = required

  def __call__(self, func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      json_body = flask.request.args.get(self.field, None)
      if self.required and json_body is None:
        raise

      obj = self.schema.model_validate(json_body)
      return func(obj, *args, **kwargs)

    return wrapper