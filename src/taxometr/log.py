import sys
import logging
import taxometr.context as context


def init_debug_logging():
  import logging.config as logconfig

  logconfig.dictConfig({
      'version': 1,
      'formatters': {
        'file': {
          'format': '%(asctime)s [%(levelname)s] {%(name)s} |hash=%(trace_hash)s| %(message)s'
        }
      },
      'filters': {
        'hashfilter': {
          '()': 'taxometr.logger.HashFilter'
        }
      },
      'handlers': {
        'console': {
          'class': 'logging.StreamHandler',
          'filters': ['hashfilter'],
          'formatter': 'file',
          'stream': 'ext://sys.stdout'
        }
      },
      'root': {
        'level': 'DEBUG',
        'handlers': ['console']
      },
      'disable_existing_loggers': False
    })


class HashFilter(logging.Filter):
  def filter(self, record: logging.LogRecord) -> bool:
    record.trace_hash = context.get_trace_hash()
    return True


def _exception_formatter(*argv, **kwargs):
  """
  * exc_type: Exception type.
  * exc_value: Exception value, can be None.
  * exc_traceback: Exception traceback, can be None.
  * err_msg: Error message, can be None.
  * object: Object causing the exception, can be None.
  """

  if argv:
    if len(argv) == 1:
      exc = argv[0]
      exc_type, exc, tb = exc.exc_type, exc.exc_value, exc.exc_traceback
    else:
      exc_type, exc, tb = argv
    logging.getLogger('excepthook').exception('Exception', exc_info=(exc_type, exc, tb))

  elif kwargs:
    exc_type, exc_value, exc_traceback, err_msg, obj = (
      kwargs.get('exc_type'),
      kwargs.get('exc_value'),
      kwargs.get('exc_traceback'),
      kwargs.get('err_msg', 'Unraisable exception'),
      kwargs.get('object')
    )

    logging.getLogger('unraisablehook').exception(
      err_msg,
      exc_info=(exc_type, exc_value or obj, exc_traceback)
    )
  else:
    logging.getLogger('exception').error(
      f'any exception: argv={argv}, '
      f'kwargs={kwargs}'
    )


sys.excepthook = _exception_formatter
sys.unraisablehook = _exception_formatter
