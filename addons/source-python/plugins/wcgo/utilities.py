"""Module for tools and utilities that are required internally."""


# Python 3
import importlib
import pkgutil
import collections

"""Class utilities for Warcraft: GO."""

class ClassProperty:
    """Read-only property for classes."""

    def __init__(self, fget=None, doc=None):
        """Initialize a new class property."""
        self.fget = fget
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, cls=None):
        """Descriptor for calling the fget on the class."""
        if cls is None:
            if obj is None:
                raise ValueError("Both obj and cls set to None")
            cls = type(obj)
        return self.fget(cls)

class KeyDefaultDict(collections.defaultdict):
    """Key based defaultdict."""

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        default = self[key] = self.default_factory(key)
        return default

"""Function utilities for Warcraft: GO."""

def import_modules(package):
    """Get a dict of all modules from a package."""
    modules = {}
    for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__):
        if module_name[0] != '_':
            full_name = package.__name__ + '.' + module_name
            modules[full_name] = importlib.import_module(full_name)
    return modules