import logging
from functools import wraps


def logged(log='trace'):
    def wrap(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            logger = logging.getLogger(log)
            logger.debug("Calling function '{}' with args={} kwargs={}"
                         .format(function.__name__, args, kwargs))
            try:
                response = function(self, *args, **kwargs)
            except Exception as error:
                logger.debug("Function '{}' raised {} with error '{}'"
                             .format(function.__name__,
                                     error.__class__.__name__,
                                     str(error)))
                raise error
            logger.debug("Function '{}' returned {}"
                         .format(function.__name__,
                                 response))
            return response

        return wrapper

    return wrap
