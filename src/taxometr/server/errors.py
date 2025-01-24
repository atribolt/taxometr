from functools import partial
from flask import Response


class Error(Response):
  def __init__(self, message, code, *args, **kwargs):
    super().__init__(
      response={
        'code': code,
        'message': message
      },
      *args, **kwargs
    )



InvalidIdentifier = partial(Error, code=1001, status=400)
InvalidActionName = partial(Error, code=1002, status=400)
InvalidDatetimeValue = partial(Error, code=1003, status=400)

InvalidBody = partial(Error, code=1000, status=400)
