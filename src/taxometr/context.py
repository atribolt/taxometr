import uuid
from contextvars import ContextVar


TRACE_HASH = ContextVar('TRACE_HASH', default='')


def generate_trace_hash():
  return uuid.uuid4().hex


def update_trace_hash():
  set_trace_hash(generate_trace_hash())


def set_trace_hash(trace_hash: str):
  TRACE_HASH.set(trace_hash)


def clear_trace_hash():
  set_trace_hash('')


def get_trace_hash():
  return TRACE_HASH.get()


__all__ = [
  'set_trace_hash',
  'get_trace_hash',
  'generate_trace_hash',
  'update_trace_hash'
]
