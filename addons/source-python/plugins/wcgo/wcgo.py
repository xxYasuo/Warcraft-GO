"""Main entry point for the plugin."""

# Source.Python
from engines.server import engine_server
from events import Event

# Warcraft: GO
import wcgo.configs as cfg
import wcgo.database
import wcgo.entities
from wcgo.player import Player


# Globals
database = None
active_players = set()


def load():
    """Setup the plugin."""
    # Make sure there are heroes on the server
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
    engine_server.server_command('mp_restartgame 1\n')


def unload():
    """Finalize the plugin."""
    for userid in active_players:
        player = Player.from_userid(userid)
        database.save_player(player)
    active_players.clear()
    database.close()


@Event('player_spawn')
def _activate_player(event):
    """Activate player when he spawns for the first time."""
    userid = event['userid']
    if userid not in active_players:
        player = Player.from_userid(userid)
        database.load_player(player)
        hero_classes = wcgo.entities.Hero.get_classes()
        for clsid in cfg.starting_heroes:
            if clsid in hero_classes and clsid not in player.heroes:
                player.heroes[clsid] = hero_classes[clsid]()
        active_players.add(userid)
    else:
        database.save_player(player)


@Event('player_disconnect')
def _deactivate_player(event):
    """Deactivate player when he disconnects."""
    userid = event['userid']
    if userid in active_players:
        player = Player.from_userid(userid)
        database.save_player(player)
        active_players.remove(userid)