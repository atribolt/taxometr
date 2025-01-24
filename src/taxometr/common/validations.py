from pydantic import ValidationError, AfterValidator
from typing import TypeAlias
from typing_extensions import Annotated


def _is_printable_string(value):
  if not isinstance(value, str):
    raise ValidationError('expected string not %s' % type(value), value)
  elif not value.isprintable():
    raise ValidationError('expected printable text', value)

  return value


PrintableString: TypeAlias = Annotated[str, AfterValidator(_is_printable_string)]
