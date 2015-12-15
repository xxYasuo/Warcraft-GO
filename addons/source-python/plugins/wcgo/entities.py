"""Module for Warcraft: GO entities like heroes and skills."""

# Warcraft: GO
import wcgo.configs as cfg
import wcgo.event
import wcgo.utilities


class _Entity:
    """Base class for all entities."""

    authors = tuple()
    cost = 0

    def __init__(self, owner=None):
        """Initialize a new entity."""
        self.owner = owner

    @classmethod
    def get_subclass_dict(cls):
        """Get a dict of all the subclasses of an entity class."""
        return {subcls.clsid: subcls
                for subcls in wcgo.utilities.get_subclasses(cls)
                if getattr(subcls, '_register', True)}

    @wcgo.utilities.ClassProperty
    def clsid(cls):
        """Get the class's ID."""
        return cls.__name__

    @wcgo.utilities.ClassProperty
    def name(cls):
        """Get the class's name."""
        return cls.__name__.replace('_', ' ')

    @wcgo.utilities.ClassProperty
    def description(cls):
        """Get the class's description."""
        return cls.__doc__ if cls.__doc__ is not None else ''


class _LevelableEntity(_Entity):
    """Entity class which implements a level system."""

    max_level = None

    def __init__(self, owner=None, level=0):
        """Initialize a new entity with levels."""
        super().__init__(owner)
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

    def is_max_level(self):
        """Return True if the entity's level is maxed out."""
        return self.max_level is not None and self.level >= self.max_level

    @property
    def level_info(self):
        """Get the entity's level info as a string."""
        if self.max_level is None:
            return str(self.level)
        return '{entity.level}/{entity.max_level}'.format(entity=self)


class Hero(_LevelableEntity):
    """Character with unique skills to spice up the game."""

    _passive_classes = tuple()
    _skill_classes = tuple()
    restricted_items = tuple()
    category = cfg.default_hero_category.get_string()
    e_level_up = wcgo.event.Event()

    def __init__(self, owner=None, level=0, xp=0):
        """Initialize a new hero."""
        super().__init__(owner, level)
        self._xp = xp
        self.passives = [cls(owner=self) for cls in self._passive_classes]
        self.skills = [cls(owner=self) for cls in self._skill_classes]
        self.items = []

    @_LevelableEntity.level.setter
    def level(self, value):
        """Set the hero's level."""
        self._xp = 0
        _LevelableEntity.level.fset(self, value)

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
        self._xp -= value
        while self.level > 0 and self._xp < 0:
            self._level -= 1
            self._xp += self.required_xp

    def give_xp(self, value):
        """Give experience points to the hero."""
        if value < 0:
            raise ValueError(
                "Negative value passed to give_xp, use take_xp instead")
        self._xp += value
        level = self.level
        while not self.is_max_level() and self._xp >= self.required_xp:
            self._xp -= self.required_xp
            self._level += 1
        if self.level > level:
            self.e_level_up.fire(
                self, levels=self.level - level, player=self.owner)

    @property
    def required_xp(self):
        """Get the required XP for the hero to level up."""
        if self.is_max_level():
            return None
        return (cfg.required_xp_base.get_int() +
            cfg.required_xp_addition.get_int() * self.level)

    @property
    def skill_points(self):
        """Get the amount of hero's unused skill points."""
        used_points = sum(skill.level * skill.cost for skill in self.skills)
        return self.level - used_points

    @property
    def xp_info(self):
        """Get the hero's XP info as a string."""
        if self.is_max_level():
            return str(self.xp)
        return '{hero.xp}/{hero.required_xp}'.format(hero=self)

    @classmethod
    def passive(cls, passive_cls):
        """Add a skill class to hero's passive classes."""
        cls._passive_classes += (passive_cls,)
        return passive_cls

    @classmethod
    def skill(cls, skill_cls):
        """Add a skill class to hero's skill classes."""
        cls._skill_classes += (skill_cls,)
        return skill_cls

    def execute_skills(self, method_name, **eargs):
        """Execute the hero's skills."""
        for passive in self.passives:
            passive.execute_method(method_name, **eargs)
        for skill in self.skills:
            if skill.level > 0:
                skill.execute_method(method_name, **eargs)
        for item in self.items:
            item.execute_method(method_name, **eargs)


class Skill(_LevelableEntity):
    """Class for creating skills for heroes."""

    cost = 1
    required_level = 0

    def execute_method(self, name, **eargs):
        """Executes the skill's method with matching name."""
        method = getattr(self, name, None)
        if method is not None:
            method(**eargs)


class Item(_Entity):
    """Item is a temporary skill that can be bought for a hero."""

    stay_after_death = False
    limit = 1
    category = cfg.default_item_category.get_string()

    def execute_method(self, name, **eargs):
        """Executes the items's method with matching name."""
        method = getattr(self, name, None)
        if method is not None:
            method(**eargs)

    @property
    def sell_value(self):
        """Get the item's sell value."""
        return round(self.cost * cfg.item_sell_value_multiplier.get_float())
