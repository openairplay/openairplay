
"""
Robobenklein's favorite logging snippets
"""

import inspect
import logging
import coloredlogs

logger = logging.getLogger(__name__)

coloredlogs.install(
    fmt="[%(asctime)s] [%(levelname)8s] [%(module)s %(funcName)s] %(message)s",
    logger=logger,
    level=logging.DEBUG
)
logger.setLevel(logging.INFO)

class bcolors:
    """Colors for general use. Done using terminal escape sequences."""

    PURPLE = '\033[35m'
    BRIGHT_PURPLE = '\033[95m'

    BLUE = '\033[34m'
    BRIGHT_BLUE = '\033[94m'

    GREEN = '\033[32m'
    BRIGHT_GREEN = '\033[92m'

    BLACK = '\033[30m'
    BRIGHT_BLACK = '\033[90m'
    GREY = BRIGHT_BLACK

    WHITE = '\033[37m'
    BRIGHT_WHITE = '\033[97m'

    YELLOW = '\033[33m'
    BRIGHT_YELLOW = '\033[93m'

    RED = '\033[31m'
    BRIGHT_RED = '\033[91m'  # High Red

    ENDC = '\033[0m'  # Reset
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class verbose_logger():
    """
    Maximizes the logger verbosity temporarily.

    Used to temporarily increase logger verbosity
     for a single section of code.

    Use a 'with' statement:
    with verbose_logger():
        # your code

    """

    def __enter__(self):
        # set logger level to debug
        self._prev_state = logger.getEffectiveLevel()
        logger.setLevel(logging.DEBUG)

    def __exit__(self, type, value, traceback):
        # set logger level to previous
        logger.setLevel(self._prev_state)


class supress_stdout():
    """
    Stops the logger's StreamHandlers temporarily.

    Used to prevent output from messing with ncurses views
     or other terminal full-windows views.

    Use a 'with' statement:
    with supress_stdout():
        # your code

    """

    def __enter__(self):
        global logger
        self.inactive_handlers = []
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                self.inactive_handlers.append(handler)
        for handler in self.inactive_handlers:
            logger.removeHandler(handler)

    def __exit__(self, type, value, traceback):
        global logger
        for handler in self.inactive_handlers:
            logger.addHandler(handler)
        del(self.inactive_handlers)


class OutputHandler(logging.Handler):
    """
    Logging handler which calls function with log text.

    For Discivide this is used to provide logging messages
     back to the application via a function call.
    """

    def __init__(self, function):
        logging.Handler.__init__(self)
        self.function = function

    def emit(self, record):
        try:
            msg = self.format(record)
            self.function(msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


# Code from gist: https://gist.github.com/techtonik/2151727
def get_caller_name(skip: int =3):
    """Get a name of a caller in the format module.class.method.

    `skip` specifies how many levels of stack to skip while getting caller
    name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

    An empty string is returned if skipped levels exceed stack height.
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]

    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append(codename)  # function or a method
    del parentframe
    return ".".join(name)


def prepend_caller(message: str):
    """Get the common name for the caller."""
    caller = get_caller_name()
    # if caller.startswith("__main__"):
    #     caller = caller.replace("__main__", bcolors.PURPLE + "Main" + bcolors.ENDC)
    message = "[" + caller + "]" + " " + message
    return message


log = info = logger.info
err = error = logger.error
dbg = debug = logger.debug
crit = critical = logger.critical
warn = warning = logger.warning
setLevel = logger.setLevel
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARNING

# Multi-line debugging output
def trace(f, message: str):
    """Print a mutliline string, for things like tracebacks."""
    for line in message.split("\n"):
        f("[TRACE] " + line)


if __name__ == "__main__":
    # stdoutlog = logging.StreamHandler()
    # stdoutlog.setFormatter(formatter)
    # logger.addHandler(stdoutlog)

    logger.setLevel(logging.INFO)

    with verbose_logger():
        logger.debug("Debug info in verbose_logger")
    logger.debug("Unseen debug message.")
    logger.info("Info info, with info")
    logger.warning("Warning info")
    logger.error("Error info")
    logger.critical("Critical info")
