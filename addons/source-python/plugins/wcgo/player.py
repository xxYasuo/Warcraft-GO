"""Module for Wacraft: GO related player functionality."""

# Source.Python
from entities.helpers import index_from_edict
from filters.iterator import _IterObject
from players import PlayerGenerator
from players.helpers import index_from_userid
import players.entity


class PlayerIter(_IterObject):
    """Class for iterating over all WCGO players."""

    @staticmethod
    def iterator():
        """Iterate over all WCGO player objects."""
        for edict in PlayerGenerator():
            yield Player(index_from_edict(edict))


class Player(players.entity.Player):
    """Player class with WCGO functionality."""

    _data = {}

    def __init__(self, index):
        """Initialize a new player."""
        super().__init__(index)
        if self.userid not in Player._data:
            Player._data[self.userid] = {
                'gold': 0,
                'hero': None,
                'heroes': {},
                'restrictions': set(),
            }

    @property
    def gold(self):
        """Get the player's gold."""
        return Player._data[self.userid]['gold']

    @gold.setter
    def gold(self, value):
        """Set the player's gold."""
        Player._data[self.userid]['gold'] = value

    @property
    def hero(self):
        """Get the player's active hero."""
        return Player._data[self.userid]['hero']

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
            Player._data[self.userid]['hero'] = value
            self.client_command('kill', True)

    @property
    def heroes(self):
        """Get the player's heroes."""
        return Player._data[self.userid]['heroes']

    @property
    def restrictions(self):
        """Get the player's restrictions."""
        return Player._data[self.userid]['restrictions']

    @classmethod
    def from_userid(cls, userid):
        """Return an instance of the player from an userid."""
        return cls(index_from_userid(userid))
