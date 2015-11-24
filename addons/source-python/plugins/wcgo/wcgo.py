"""Main entry point for the plugin."""

# Source.Python
from engines.server import engine_server
from events import Event

# Warcraft: GO
import wcgo.configs as cfg
import wcgo.database
import wcgo.entities
import wcgo.player


# Globals
database = None


def load():
    """Setup the plugin."""
    # Make sure there are proper heroes on the server
    heroes = Hero.get_subclasses()
    if not heroes:
        raise NotImplementedError(
            "There are no heroes on the server")
    if not cfg.starting_heroes:
        raise NotImplementedError(
            "There are no starting heroes defined")
    for clsid in cfg.starting_heroes:
        if clsid not in heroes:
            raise ValueError(
                "Invalid starting hero clsid: {0}".format(clsid))

    # Initialize the database and restart the game
    global database
    database = wcgo.database.Database(cfg.database_path)
    engine_server.server_command('mp_restartgame_immediate 1\n')
    for player in wcgo.player.PlayerIter():
        _init_player(player)


def unload():
    """Finalize the plugin."""
    for player in wcgo.player.PlayerIter():
        database.save_player(player)
    database.close()


def _init_player(player):
    """Initialize the player."""
    database.load_player(player)
    hero_classes = wcgo.entities.Hero.get_classes()
    for clsid in cfg.starting_heroes:
        if clsid in hero_classes and clsid not in player.heroes:
            player.heroes[clsid] = hero_classes[clsid]()
    if player.hero is None:
        player.hero = player.heroes[0]


@Event('player_activate')
def _on_player_activate(event):
    """Initialize the player the when he gets activated."""
    player = Player.from_userid(event['userid'])
    _init_player(player)


@Event('player_disconnect', 'player_spawn')
def _save_player_data(event):
    """Save the player's data when he disconnects or spawns."""
    player = Player.from_userid(event['userid'])
    database.save_player(player)
