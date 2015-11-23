"""Module for tools and utilities that are required internally."""


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
