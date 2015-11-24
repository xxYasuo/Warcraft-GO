"""Module for Wacraft: GO related player functionality."""

# Source.Python
from filters.iterator import _IterObject
from players import PlayerGenerator
from players.helpers import index_from_edict

# EasyPlayer
from easyplayer import EasyPlayer


class PlayerIter(_IterObject):
    """Class for iterating over all WCGO players."""

    @staticmethod
    def iterator():
        """Iterate over all WCGO player objects."""
        for edict in PlayerGenerator():
            yield Player(index_from_edict(edict))


class Player(easyplayer.EasyPlayer):
    """Player class with WCGO functionality."""

    def __init__(self, index):
        """Initialize a new player."""
        super().__init__(index)
        self.gold = gold
        self._hero = None
        self.heroes = {}

    @property
    def hero(self):
        """Get the player's active hero."""
        return self._hero

    @hero.setter
    def hero(self, value):
        """Set the player's active hero."""
        if value.clsid not in self.heroes:
            raise ValueError(
                "Hero {0} not owned by {1}".format(value.clsid, self.steamid))
        if value != self.hero:
            if self.hero is not None:
                self.hero.items.clear()
            self.restrictions.clear()
            self._hero = value
