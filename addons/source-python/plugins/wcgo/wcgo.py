"""Main entry point for the plugin."""

# Python 3
import random

# Source.Python
from commands import CommandReturn
from commands.say import SayCommand
from commands.client import ClientCommand
from engines.server import engine_server
from entities import TakeDamageInfo
from entities.entity import Entity
from entities.helpers import index_from_pointer
from entities.helpers import index_from_inthandle
from entities.hooks import EntityPreHook
from entities.hooks import EntityCondition
from events import Event
from memory import make_object
from path import Path
from paths import PLUGIN_DATA_PATH
from weapons.entity import Weapon

# Warcraft: GO
import wcgo.configs as cfg
import wcgo.database
import wcgo.effects
import wcgo.entities
import wcgo.heroes
import wcgo.items
import wcgo.menus
import wcgo.player
import wcgo.strings
import wcgo.utilities


# Globals
database = None
_DATABASE_PATH = PLUGIN_DATA_PATH / 'wcgo.db'


def player_from_event(event, key):
    """Fetch player from an event's key."""
    if event[key]:
        return wcgo.player.Player.from_userid(event[key])
    return None


def load():
    """Setup the plugin."""
    # Make sure there are proper heroes on the server
    wcgo.utilities.import_modules(wcgo.heroes)
    wcgo.utilities.import_modules(wcgo.items)
    heroes = wcgo.entities.Hero.get_subclass_dict()
    if not heroes:
        raise NotImplementedError(
            "There are no heroes on the server")
    starting_heroes = cfg.starting_heroes.get_string().split(',')
    if not starting_heroes:
        raise NotImplementedError(
            "There are no starting heroes defined")
    for clsid in starting_heroes:
        if clsid not in heroes:
            raise ValueError(
                "Invalid starting hero clsid: '{0}'".format(clsid))

    # Initialize the database and restart the game
    global database
    database = wcgo.database.Database(_DATABASE_PATH)
    for player in wcgo.player.PlayerIter():
        _init_player(player)

    # Listen to Hero.e_level_up event and restart the game
    wcgo.entities.Hero.e_level_up += _on_hero_level_up
    engine_server.server_command('mp_restartgame 1\n')


def unload():
    """Finalize the plugin."""
    for player in wcgo.player.PlayerIter():
        database.save_player(player)
    database.close()
    wcgo.entities.Hero.e_level_up -= _on_hero_level_up


def _init_player(player):
    """Initialize the player."""
    database.load_player(player)
    hero_classes = wcgo.entities.Hero.get_subclass_dict()
    starting_heroes = cfg.starting_heroes.get_string().split(',')
    for clsid in starting_heroes:
        if clsid in hero_classes and clsid not in player.heroes:
            player.heroes[clsid] = hero_classes[clsid](owner=player)
    if player.hero is None:
        random_clsid = random.choice(starting_heroes)
        player.hero = player.heroes[random_clsid]


@Event('player_activate')
def _init_player_on_activate(event):
    """Initialize the player the when he gets activated."""
    player = player_from_event(event, 'userid')
    _init_player(player)


@Event('player_disconnect')
def _save_data_on_disconnect(event):
    """Save the player's data when he disconnects."""
    player = player_from_event(event, 'userid')
    database.save_player(player)


@Event('player_spawn')
def _save_data_on_spawn(event):
    """Save the player's data when he spawns."""
    if event['teamnum'] in (2, 3):
        player = player_from_event(event, 'userid')
        if player.steamid == 'BOT':
            return  # No need to save bots on spawn, only on disconnect
        database.save_player(player)


# Game messages

def _on_hero_level_up(hero, player, levels):
    """Alarm the player and play a sound when a hero level's up."""
    wcgo.strings.misc_messages['Level Up'].send(player.index, level=hero.level)
    wcgo.menus.heroes.current_hero_menu.send(player.index)
    wcgo.effects.level_up(player)
    if player.steamid == 'BOT':
        skills = [skill for skill in hero.skills if not skill.is_max_level()]
        random.shuffle(skills)
        for skill in skills:
            if skill.cost <= hero.skill_points:
                skill.level += 1
                if hero.skill_points == 0:
                    break


@Event('player_spawn')
def _execute_spawn_message(event):
    """Send a message informing player of his level and XP."""
    if event['teamnum'] in (2, 3):
        player = player_from_event(event, 'userid')
        if player.steamid == 'BOT' and player.hero is None:
            return  # Bots sometimes spawn before their data is loaded
        wcgo.strings.misc_messages['Hero Info'].send(player.index, hero=player.hero)


# Say command and client command decorations

@ClientCommand('wcgo')
@SayCommand('wcgo')
def _main_say_command(command, index, team=None):
    """Send the main menu to a player."""
    wcgo.menus.main_menu.send(index)
    return CommandReturn.BLOCK


@ClientCommand(['showxp', 'heroinfo'])
@SayCommand(['showxp', 'heroinfo'])
def _showxp_say_command(command, index, team=None):
    """Display player's level and xp."""
    player = wcgo.player.Player(index)
    wcgo.strings.misc_messages['Hero Info'].send(index, hero=player.hero)
    return CommandReturn.BLOCK


@ClientCommand('ultimate')
@SayCommand('ultimate')
def _ultimate_say_command(command, index, team=None):
    player = wcgo.player.Player(index)
    if player.team in (2, 3) and player.isdead is False:
        player.hero.execute_skills('player_ultimate', player=player)
    else:
        wcgo.strings.misc_messages['Ultimate Failed'].send(index)
    return CommandReturn.BLOCK


# Skill executions, XP gain, and gold gain

def _execute_player_skills(event):
    """Execute skills for the player in the event."""
    player = player_from_event(event, 'userid')
    if player.steamid == 'BOT' and player.hero is None:
        return  # Bots sometimes spawn before their data is loaded
    eargs = event.variables.as_dict()
    del eargs['userid']
    player.hero.execute_skills(event.get_name(), player=player, **eargs)


@Event('round_start')
def _round_start(event):
    for player in wcgo.player.PlayerIter():
        player.hero.execute_skills('round_start', player=player)


@Event('round_end')
def _round_end(event):
    winner = event['winner']
    for player in wcgo.player.PlayerIter():
        if player.hero is None:
            continue
        key = 'Round {0}'.format('Win' if player.team == winner else 'Loss')
        xp = cfg.exp_values[key].get_int()
        player.hero.give_xp(xp)
        player.gold += cfg.gold_values[key].get_int()
        player.hero.execute_skills('round_end', player=player, winner=winner)
        wcgo.strings.xp_messages[key].send(player.index, xp=xp, hero=player.hero)


@Event('bomb_planted')
def _bomb_planted(event):
    player = player_from_event(event, 'userid')
    player.hero.give_xp(cfg.exp_values['Bomb Plant'].get_int())
    ally_xp = cfg.exp_values['Bomb Plant Team'].get_int()
    for ally in wcgo.player.PlayerIter():
        if ally.team == player.team and ally.userid != player.userid:
            ally.hero.give_xp(ally_xp)
    player.hero.execute_skills('bomb_planted', player=player)


@Event('bomb_exploded')
def _bomb_exploded(event):
    player = player_from_event(event, 'userid')
    player.hero.give_xp(cfg.exp_values['Bomb Explode'].get_int())
    ally_xp = cfg.exp_values['Bomb Explode Team'].get_int()
    for ally in wcgo.player.PlayerIter():
        if ally.team == player.team and not ally.userid == player.userid:
            ally.hero.give_xp(ally_xp)
    player.hero.execute_skills('bomb_exploded', player=player)


@Event('bomb_defused')
def _bomb_defused(event):
    player = player_from_event(event, 'userid')
    player.hero.give_xp(cfg.exp_values['Bomb Defuse'].get_int())
    ally_xp = cfg.exp_values['Bomb Defuse Team'].get_int()
    for ally in wcgo.player.PlayerIter():
        if ally.team == player.team and not ally.userid == player.userid:
            ally.hero.give_xp(ally_xp)
    player.hero.execute_skills('bomb_defused', player=player)


@Event('hostage_follows')
def _hostage_follows(event):
    player = player_from_event(event, 'userid')
    player.hero.give_xp(cfg.exp_values['Hostage Pick Up'].get_int())
    ally_xp = cfg.exp_values['Hostage Pick Up Team'].get_int()
    for ally in wcgo.player.PlayerIter():
        if ally.team == player.team and not ally.userid == player.userid:
            ally.hero.give_xp(ally_xp)
    player.hero.execute_skills('hostage_follows', player=player)


@Event('hostage_rescued')
def _hostage_rescued(event):
    player = player_from_event(event, 'userid')
    player.hero.give_xp(cfg.exp_values['Hostage Rescue'].get_int())
    ally_xp = cfg.exp_values['Hostage Rescue Team'].get_int()
    for ally in wcgo.player.PlayerIter():
        if ally.team == player.team and not ally.userid == player.userid:
            ally.hero.give_xp(ally_xp)
    player.hero.execute_skills('hostage_rescued', player=player)


@Event('player_spawn')
def _on_player_spawn(event):
    if event['teamnum'] in (2, 3):
        _execute_player_skills(event)


@Event('player_jump')
def _on_player_jump(event):
    _execute_player_skills(event)


@Event('player_death')
def _on_player_death(event):
    victim = player_from_event(event, 'userid')
    attacker = player_from_event(event, 'attacker')
    assister = player_from_event(event, 'assister')
    eargs = event.variables.as_dict()
    del eargs['userid']
    eargs.update(attacker=attacker, victim=victim, assister=assister)

    if assister is not None:
        assister.hero.execute_skills('player_assist', player=assister, **eargs)
        xp = cfg.exp_values['Assist'].get_int()
        assister.hero.give_xp(xp)
        assister.gold += cfg.gold_values['Assist'].get_int()
        wcgo.strings.xp_messages['Assist'].send(assister.index, xp=xp, hero=assister.hero)

    if attacker is None or attacker.userid == victim.userid:
        victim.hero.execute_skills('player_suicide', player=victim, **eargs)
        victim.hero.items = [item for item in victim.hero.items
                             if item.stay_after_death]
        return

    key = 'Headshot' if eargs['headshot'] else 'Kill'
    attacker.hero.execute_skills('player_kill', player=attacker, **eargs)
    xp = cfg.exp_values[key].get_int()
    attacker.hero.give_xp(xp)
    attacker.gold += cfg.gold_values[key].get_int()
    wcgo.strings.xp_messages[key].send(attacker.index, xp=xp, hero=attacker.hero)

    victim.hero.execute_skills('player_death', player=victim, **eargs)
    victim.hero.items = [item for item in victim.hero.items
                         if item.stay_after_death]


@Event('player_hurt')
def _on_player_hurt(event):
    victim = player_from_event(event, 'userid')
    attacker = player_from_event(event, 'attacker')
    eargs = event.variables.as_dict()
    del eargs['userid']
    eargs.update(attacker=attacker, victim=victim)
    if attacker is None or attacker.userid == victim.userid:
        victim.hero.execute_skills('player_self_injury', player=victim, **eargs)
        return
    if attacker.hero is not None:
        attacker.hero.execute_skills('player_attack', player=attacker, **eargs)
    if victim.hero is not None:
        victim.hero.execute_skills('player_victim', player=victim, **eargs)


# Take damage system hooks

@EntityPreHook(EntityCondition.is_player, 'on_take_damage')
def _pre_on_take_damage(args):
    info = make_object(TakeDamageInfo, args[1])

    entity = Entity(info.attacker) if info.attacker else None
    if entity is not None and entity.is_player():
        attacker = wcgo.player.Player(entity.index)
    else:
        attacker = None

    victim = wcgo.player.Player(index_from_pointer(args[0]))
    eargs = {
        'attacker': attacker,
        'victim': victim,
        'info': info,
    }
    # Adds the weapon argument dependent on scenario
    if attacker is not None and attacker.active_weapon != -1:
        eargs['weapon'] = Weapon(index_from_inthandle(attacker.active_weapon))
    else:
        eargs['weapon'] = None

    if attacker is None or attacker.userid == victim.userid:
        victim.hero.execute_skills('player_pre_self_injury', player=victim, **eargs)
        return
    if not (attacker.steamid == 'BOT' and attacker.hero is None):
        attacker.hero.execute_skills('player_pre_attack', player=attacker, **eargs)
    if not (victim.steamid == 'BOT' and victim.hero is None):
        victim.hero.execute_skills('player_pre_victim', player=victim, **eargs)
