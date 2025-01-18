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


InvalidTitle = partial(Error, code=1000, status=400)
InvalidIdentifier = partial(Response, code=1001, status=400)
