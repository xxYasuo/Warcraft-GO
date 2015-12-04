"""Main entry point for the plugin."""

# Python 3
import random

# Source.Python
from commands import CommandReturn
from commands.say import SayCommand
from commands.client import ClientCommand
from engines.server import engine_server
from entities import TakeDamageInfo
from entities.helpers import index_from_pointer
from entities.helpers import index_from_inthandle
from entities.hooks import EntityPreHook
from entities.hooks import EntityCondition
from events import Event
from memory import make_object
from messages import HintText
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
    for clsid in cfg.starting_heroes:
        if clsid in hero_classes and clsid not in player.heroes:
            player.heroes[clsid] = hero_classes[clsid](owner=player)
    if player.hero is None:
        random_clsid = random.choice(cfg.starting_heroes)
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
            return  # No need to save bots all the time
        database.save_player(player)


# Game messages

def _on_hero_level_up(hero, player, levels):
    """Alarm the player and play a sound when a hero level's up."""
    wcgo.strings.message(player.index, 'Level Up', level=hero.level)
    wcgo.menus.heroes.current_hero_menu.send(player.index)
    wcgo.effects.level_up(player)


def _execute_spawn_message(event):
    player = player_from_event(event, 'userid')
    if player.steamid == 'BOT' and player.hero is None:
        return  # Bots sometimes spawn before their data is loaded
    hero = player.hero
    wcgo.strings.message(player.index, 'Show XP', hero=hero.name,
        level=hero.level, xp=hero.xp, needed=hero.required_xp)


# Say command and client command decorations

@ClientCommand('wcgo')
@SayCommand('wcgo')
def _main_say_command(command, index, team=None):
    wcgo.menus.main_menu.send(index)
    return CommandReturn.BLOCK

@ClientCommand('showxp')
@SayCommand('showxp')
def _showxp_say_command(command, index, team=None):
    player = wcgo.player.Player(index)
    hero = player.hero
    wcgo.strings.message(index, 'Show XP', hero=hero.name,
        level=hero.level, xp=hero.xp, needed=hero.required_xp)
    return CommandReturn.BLOCK


# Skill executions, XP gain, and gold gain

def _execute_player_skills(event):
    """Execute skills for one player."""
    player = player_from_event(event, 'userid')
    if player.steamid == 'BOT' and player.hero is None:
        return  # Bots sometimes spawn before their data is loaded
    eargs = event.variables.as_dict()
    del eargs['userid']
    player.hero.execute_skills(event.get_name(), player=player, **eargs)


@Event('round_start')
def _round_start(event):
    for player in wcgo.player.PlayerIter():
        player.hero.execute_skills(
            'round_start', player=player)


@Event('round_end')
def _round_end(event):
    winner = event['winner']

    for player in wcgo.player.PlayerIter():
        win_or_loss = 'Win' if player.team is winner else 'Loss'
        if not player.hero is None:
            player.hero.give_xp(cfg.exp_values.get('Round {}'.format(win_or_loss), 0))
            player.gold += cfg.gold_values.get('Round {}'.format(win_or_loss), 0)
            player.hero.execute_skills('round_end', player=player, winner=winner)
            wcgo.strings.message(player.index, 'Round {}'.format(win_or_loss),
                msg_cls=HintText,
                use_template=False,
                xp=cfg.exp_values.get('Round {}'.format(win_or_loss), 0),
                hero=player.hero.name,
                current=player.hero.xp,
                needed=player.hero.required_xp)


@Event('bomb_planted')
def _bomb_planted(event):
    player = player_from_event(event, 'userid')
    player.hero.give_xp(cfg.exp_values.get('Bomb Plant', 0))
    for ally in wcgo.player.PlayerIter():
        if ally.team == player.team and ally.userid != player.userid:
            ally.hero.give_xp(cfg.exp_values.get('Bomb Plant Team', 0))
    player.hero.execute_skills('bomb_planted', player=player)


@Event('bomb_exploded')
def _bomb_exploded(event):
    player = player_from_event(event, 'userid')
    player.hero.give_xp(cfg.exp_values.get('Bomb Explode', 0))
    for ally in wcgo.player.PlayerIter():
        if ally.team == player.team and ally.userid != player.userid:
            ally.hero.give_xp(cfg.exp_values.get('Bomb Explode Team', 0))
    player.hero.execute_skills('bomb_exploded', player=player)


@Event('bomb_defused')
def _bomb_defused(event):
    player = player_from_event(event, 'userid')
    player.hero.give_xp(cfg.exp_values.get('Bomb Defuse', 0))
    for ally in wcgo.player.PlayerIter():
        if ally.team == player.team and ally.userid != player.userid:
            ally.hero.give_xp(cfg.exp_values.get('Bomb Defuse Team', 0))
    player.hero.execute_skills('bomb_defused', player=player)


@Event('hostage_follows')
def _hostage_follows(event):
    player = player_from_event(event, 'userid')
    player.hero.give_xp(cfg.exp_values.get('Hostage Pick Up', 0))
    for ally in wcgo.player.PlayerIter():
        if ally.team == player.team and ally.userid != player.userid:
            ally.hero.give_xp(cfg.exp_values.get('Hostage Pick Up Team', 0))
    player.hero.execute_skills('hostage_follows', player=player)


@Event('hostage_rescued')
def _hostage_rescued(event):
    player = player_from_event(event, 'userid')
    player.hero.give_xp(cfg.exp_values.get('Hostage Rescue', 0))
    for ally in wcgo.player.PlayerIter():
        if ally.team == player.team and ally.userid != player.userid:
            ally.hero.give_xp(cfg.exp_values.get('Hostage Rescue Team', 0))
    player.hero.execute_skills('hostage_rescued', player=player)


@Event('player_spawn')
def _on_player_spawn(event):
    if event['teamnum'] in (2, 3):
        _execute_player_skills(event)
        _execute_spawn_message(event)


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
    if attacker is None or attacker.userid == victim.userid:
        victim.hero.execute_skills('player_suicide', player=victim, **eargs)
        victim.hero.items = [item for item in victim.hero.items
                             if item.stay_after_death]
        return
    # Checks if assister exists first, then check if player is bot
    if not assister is None and assister.steamid != 'BOT':
        assister.hero.execute_skills('player_assist', player=assister, **eargs)
        assister.hero.give_xp(cfg.exp_values.get('Assist', 0))
        assister.gold += cfg.gold_values.get('Assist', 2)
        wcgo.strings.message(assister.index, 'Assist',
            msg_cls=HintText,
            use_template=False,
            xp=cfg.exp_values.get('Assist', 0),
            hero=assister.hero.name,
            current=assister.hero.xp,
            needed=assister.hero.required_xp)

    if not (attacker.steamid == 'BOT' and attacker.hero is None):
        attacker.hero.execute_skills('player_kill', player=attacker, **eargs)
        attacker.gold += cfg.gold_values.get('Kill', 3)
        if eargs['headshot'] is True:
            attacker.hero.give_xp(cfg.exp_values.get('Headshot', 0))
            wcgo.strings.message(attacker.index, 'Headshot',
                msg_cls=HintText,
                use_template=False,
                xp=cfg.exp_values.get('Headshot', 0),
                hero=attacker.hero.name,
                current=attacker.hero.xp,
                needed=attacker.hero.required_xp)
        else:
            attacker.hero.give_xp(cfg.exp_values.get('Kill', 0))
            wcgo.strings.message(attacker.index, 'Kill',
                msg_cls=HintText,
                use_template=False,
                xp=cfg.exp_values.get('Kill', 0),
                hero=attacker.hero.name,
                current=attacker.hero.xp,
                needed=attacker.hero.required_xp)

    if not (victim.steamid == 'BOT' and victim.hero is None):
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
    if not attacker.hero is None:
        attacker.hero.execute_skills('player_attack', player=attacker, **eargs)
    if not victim.hero is None:
        victim.hero.execute_skills('player_victim', player=victim, **eargs)


# Take damage system hooks

@EntityPreHook(EntityCondition.is_player, 'on_take_damage')
def _pre_on_take_damage(args):
    info = make_object(TakeDamageInfo, args[1])
    attacker = wcgo.player.Player(info.attacker) if info.attacker else None
    victim = wcgo.player.Player(index_from_pointer(args[0]))
    eargs = {
        'attacker': attacker,
        'victim': victim,
        'info': info,
    }
    # Adds the weapon argument dependent on scenario
    if not attacker is None and attacker.active_weapon != -1:
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
