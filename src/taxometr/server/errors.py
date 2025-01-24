import json
from functools import partial
from flask import Response


class Error(Response):
  def __init__(self, message, code, *args, **kwargs):
    super().__init__(
      response=json.dumps({
        'code': code,
        'message': message
      }),
      content_type='application/json',
      *args, **kwargs
    )


InvalidIdentifier = partial(Error, code=1001, status=400)
InvalidActionName = partial(Error, code=1002, status=400)
InvalidDatetimeValue = partial(Error, code=1003, status=400)
InvalidQueryItem = partial(Error, core=1004, status=400)

NoActiveActions = partial(Error, code=2000, status=404)
