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
    cost = 0


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
            raise ValueError(
                "Entity's level can't be negative")
        if self.max_level is not None and value > self.max_level:
            raise ValueError(
                "Entity's level can't be bigger than its max_level")
        self._level = value


class Hero(LevelableEntity):
    """Character with unique skills to spice up the game."""

    _passive_classes = tuple()
    _skill_classes = tuple()

    def __init__(self, level=0, xp=0):
        """Initialize a new hero."""
        super().__init__(level)
        self._xp = xp
        self.passives = [cls() for cls in self._passive_classes]
        self.skills = [cls() for cls in self._skill_classes]

    @Entity.level.setter
    def level(self, value):
        """Set the hero's level."""
        self._xp = 0
        Entity.level.fset(self, value)

    @property
    def xp(self):
        """Get the hero's experience points."""
        return self._xp

    @property
    def xp(self, value):
        """Set the hero's experience points."""
        if value < 0:
            self.take_xp(value)
        elif value > 0:
            self.give_xp(value)

    def take_xp(self, value):
        """Take experience points from a hero."""
        if value > 0:
            raise ValueError(
                "Positive value passed to take_xp, use give_xp instead")
        raise NotImplementedError(
            "Taking XP from a hero is not quite ready :(")

    def give_xp(self, value):
        """Give experience points to a hero."""
        if value < 0:
            raise ValueError(
                "Negative value passed to give_xp, use take_xp instead")
        self._xp += value
        while self.required_xp is not None and self._xp >= self.required_xp:
            self._xp -= self.required_xp
            self._level += 1
        if self.required_xp is None:
            self._xp = 0

    @property
    def required_xp(self):
        """Get the required XP for the hero to level up."""
        if self.max_level is not None and self.level >= self.max_level:
            return None
        return 80 + 20 * self.level

    @property
    def skill_point(self):
        """Get the amount of hero's unused skill points."""
        used_points = sum(skill.level * skill.cost for skill in self.skills)
        return self.level - used_points

    @classmethod
    def passive(cls, passive_cls):
        """Add a skill class to hero's passive classes."""
        cls._passive_classes += (passive_cls,)
        return passive_cls

    @classmethod
    def skill(cls, skill_cls):
        """Add a skill class to hero's skill classes."""
        cls._skill_classes += (skill_class,)
        return skill_cls


class Skill(LevelableEntity):
    """Class for creating skills for heroes."""
   
    cost = 1
    required_level = 0