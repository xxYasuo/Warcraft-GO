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


class LevelableEntity(Entity):
    """Entity class which implements a level system."""

    max_level = None

    def __init__(self, level=0):
        """Initialize a new entity with levels."""
        self._level = level

    @property
    def level(self):
        """Get the entity's level."""
        return self._level

    @level.setter
    def level(self, value):
        """Set the entity's level."""
        if value < 0:
            raise ValueError("Entity's level can't be negative")
        if self.max_level is not None and value > self.max_level:
            raise ValueError("Entity's level bigger than its max_level")
        self._level = value
