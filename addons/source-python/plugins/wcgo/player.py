"""Module for Wacraft: GO related player functionality."""

# Source.Python
from entities.helpers import index_from_edict
from filters.iterator import PlayerIter as SPPlayerIter
from players import PlayerGenerator
from players.helpers import index_from_userid

# EasyPlayer
import easyplayer


class PlayerIter(SPPlayerIter):
    """Class for iterating over all WCGO players."""

    @staticmethod
    def iterator():
        """Iterate over all WCGO player objects."""
        for edict in PlayerGenerator():
            yield Player(index_from_edict(edict))

# Set the filters to be the same as SP's
PlayerIter._filters = dict(SPPlayerIter.filters)


class Player(easyplayer.EasyPlayer):
    """Player class with WCGO functionality."""

    def __init__(self, index):
        """Initialize a new player."""
        super().__init__(index)
        self.gold = 0
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
            self.client_command('kill', True)
