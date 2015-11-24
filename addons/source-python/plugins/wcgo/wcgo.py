"""Main entry point for the plugin."""

# Source.Python
from engines.server import engine_server

# Warcraft: GO
import wcgo.configs as cfg
import wcgo.database
import wcgo.player


# Globals
database = None


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
    for player in wcgo.player.PlayerIter():
        database.save_player(player)
    database.close()
