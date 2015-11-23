"""Module for Warcraft: GO entities like heroes and skills."""


# Warcraft: GO
from wcgo.utilities import ClassProperty


class _Entity:
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


class _LevelableEntity(_Entity):
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


class Hero(_LevelableEntity):
    """Character with unique skills to spice up the game."""

    _passive_classes = tuple()
    _skill_classes = tuple()
    restricted_items = tuple()

    def __init__(self, level=0, xp=0):
        """Initialize a new hero."""
        super().__init__(level)
        self._xp = xp
        self.passives = [cls() for cls in self._passive_classes]
        self.skills = [cls() for cls in self._skill_classes]
        self.items = []

    @Entity.level.setter
    def level(self, value):
        """Set the hero's level."""
        self._xp = 0
        Entity.level.fset(self, value)

    @property
    def xp(self):
        """Get the hero's experience points."""
        return self._xp

    @xp.setter
    def xp(self, value):
        """Set the hero's experience points."""
        if value < self.xp:
            self.take_xp(self.xp - value)
        elif value > self.xp:
            self.give_xp(value - self.xp)

    def take_xp(self, value):
        """Take experience points from the hero."""
        if value > 0:
            raise ValueError(
                "Positive value passed to take_xp, use give_xp instead")
        raise NotImplementedError(
            "Taking XP from a hero is not quite ready :(")

    def give_xp(self, value):
        """Give experience points to the hero."""
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

    def execute_skills(self, method_name, **eargs):
        """Execute the hero's skills."""
        for passive in self.passives:
            passive.execute_method(method_name, **eargs)
        for skill in self.skills:
            skill.execute_method(method_name, **eargs)
        for item in self.items:
            item.execute_method(method_name, **eargs)


class Skill(_LevelableEntity):
    """Class for creating skills for heroes."""

    cost = 1
    required_level = 0

    def execute_method(self, name, **eargs):
        """Executes the skill's method with matching name."""
        method = getattr(type(self), name, None)
        if method is not None:
            method(self, **eargs)


class Item(_Entity):
    """Item is a temporary skill that can be bought for a hero."""

    stay_on_death = False
    limit = 1

    def execute_method(self, name, **eargs):
        """Executes the items's method with matching name."""
        method = getattr(type(self), name, None)
        if method is not None:
            method(self, **eargs)

    @property
    def sell_value(self):
        """Get the item's sell value."""
        return round(self.cost * 0.75)
