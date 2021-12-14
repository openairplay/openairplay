
from functools import wraps
import inspect

from . import log


class SimpleRepr(object):
    """A mixin implementing a simple __repr__.

    https://stackoverflow.com/a/44595303/2375851
    """
    def __repr__(self):
        return "<{klass} @{id:x} {attrs}>".format(
            klass=self.__class__.__name__,
            id=id(self) & 0xFFFFFF,
            attrs=" ".join("{}={!r}".format(k, v) for k, v in self.__dict__.items()),
        )
