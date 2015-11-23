"""Module for Warcraft: GO entities like heroes and skills."""


from wcgo.utilities import ClassProperty


class Entity:
    """Base class for all entities."""

    @ClassProperty
    def clsid(cls):
        """Get the class's ID."""
        return cls.__name__

    @ClassProperty
    def name(cls):
        """Get the class's name."""
        return cls.__name__.replace('_', ' ')

    @ClassProperty
    def description(cls):
        """Get the class's description."""
        return cls.__doc__ if cls.__doc__ is not None else ''

    authors = tuple()
