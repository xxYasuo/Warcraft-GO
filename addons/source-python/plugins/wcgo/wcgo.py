"""Main entry point for the plugin."""

# Python 3
import random

# Source.Python
from commands.say import SayCommand
from engines.server import engine_server
from entities import TakeDamageInfo
from entities.helpers import index_from_pointer
from entities.hooks import EntityPreHook
from entities.hooks import EntityCondition
from events import Event
from memory import make_object
from weapons.entity import Weapon

# Warcraft: GO
import wcgo.configs as cfg
import wcgo.database
import wcgo.entities
import wcgo.heroes
import wcgo.menus
import wcgo.player
import wcgo.utilities


# Globals
database = None


def load():
    """Setup the plugin."""
    # Make sure there are proper heroes on the server
    wcgo.utilities.import_modules(wcgo.heroes)
    heroes = wcgo.entities.Hero.get_classes()
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
            player.heroes[clsid] = hero_classes[clsid](owner=player)
    if player.hero is None:
        random_clsid = random.choice(cfg.starting_heroes)
        player.hero = player.heroes[random_clsid]


@Event('player_activate')
def _on_player_activate(event):
    """Initialize the player the when he gets activated."""
    player = wcgo.player.Player.from_userid(event['userid'])
    _init_player(player)


@Event('player_disconnect')
def _on_player_disconnect(event):
    """Save the player's data when he disconnects."""
    player = wcgo.player.Player.from_userid(event['userid'])
    database.save_player(player)
    del wcgo.player.Player._data[player.userid]


@Event('player_spawn')
def _on_player_spawn(event):
    """Save the player's data when he spawns."""
    if event['teamnum'] in (2, 3):
        player = wcgo.player.Player.from_userid(event['userid'])
        database.save_player(player)


# Say command and client command decorations

@SayCommand('wcgo')
def _main_say_command(command, index, team):
    wcgo.menus.MENUS['main'].send(index)


# Skill executions, XP gain, and gold gain

def _execute_player_skills(event):
    """Execute skills for one player."""
    player = wcgo.player.Player.from_userid(event['userid'])
    eargs = event.variables.as_dict()
    del eargs['userid']
    eargs['player'] = player
    player.hero.execute_skills(event.get_name(), **eargs)


def _execute_attacker_victim_skills(event, attacker_ename, victim_ename):
    """Execute attacker's and victim's skills."""
    victim = wcgo.player.Player.from_userid(event['userid'])
    if event['userid'] != event['attacker'] and event['attacker']:
        attacker = wcgo.player.Player.from_userid(event['attacker'])
        eargs = event.variables.as_dict()
        del eargs['userid']
        eargs.update(attacker=attacker, victim=victim)
        attacker.hero.execute_skills(attacker_ename, player=attacker, **eargs)
        victim.hero.execute_skills(victim_ename, player=victim, **eargs)


@Event('player_spawn')
def _on_player_spawn(event):
    if event['teamnum'] in (2, 3):
        _execute_player_skills(event)


@Event('player_jump')
def _on_player_jump(event):
    _execute_player_skills(event)


@Event('player_death')
def _on_player_death(event):
    _execute_attacker_victim_skills(event, 'player_kill', 'player_death')
    victim = wcgo.player.Player.from_userid(event['userid'])
    victim.hero.items = [item for item in victim.hero.items
                         if item.stay_after_death]


@Event('player_hurt')
def _on_player_hurt(event):
    _execute_attacker_victim_skills(event, 'player_attack', 'player_victim')


# Take damage system hooks

@EntityPreHook(EntityCondition.is_player, 'on_take_damage')
def _pre_on_take_damage(args):
    victim_index = index_from_pointer(args[0])
    victim = wcgo.player.Player(victim_index)
    info = make_object(TakeDamageInfo, args[1])
    if info.attacker and info.attacker != victim_index:
        attacker = wcgo.player.Player(info.attacker)
        eargs = {
            'attacker': attacker,
            'victim': victim,
            'info': info,
            'weapon': attacker.active_weapon.class_name,
        }
        victim.hero.execute_skills('player_pre_victim', player=victim, **eargs)
        attacker.hero.execute_skills('player_pre_attack', player=attacker, **eargs)


# Restriction system hooks

@EntityPreHook(EntityCondition.is_player, 'bump_weapon')
def _pre_bump_weapon(args):
    player = wcgo.player.Player(index_from_pointer(args[0]))
    weapon = Weapon(index_from_pointer(args[1]))
    if weapon.classname in player.restrictions:
        return False


@EntityPreHook(EntityCondition.is_player, 'buy_internal')
def _on_buy_internal(args):
    player = wcgo.player.Player(index_from_pointer(args[0]))
    weapon = 'weapon_{}'.format(args[1])
    if weapon in player.restrictions:
        return 0


@Event('player_death')
def _clear_restrictions_and_gravity(event):
    player = wcgo.player.Player.from_userid(event['userid'])
    player.restrictions.clear()
    player.gravity = 1.0