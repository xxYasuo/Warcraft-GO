"""This module contains configurable settings for server operators."""

# Source.Python
from config.manager import ConfigManager
from translations.strings import LangStrings

# Warcraft: GO
from wcgo.info import info

# Admins' SteamIDs, separated by commas
admins = (
    'STEAM_0:0:20178479',  # Mahi
    'STEAM_1:0:120220385',  # Predz
)

config_strings = LangStrings(info.basename + '/config')
exp_values = dict()
gold_values = dict()

# Create the cfg file
with ConfigManager(info.basename, info.basename + '_') as _config:

    # Add the menu separator convar
    menu_separator = _config.cvar(
        'menu_separator', ' ', config_strings['Separator'])

    _config.section(config_strings['Section:Exp'])

    # Add the kill experience configurations
    exp_values['Kill'] = _config.cvar(
        'kill_xp', 30, config_strings['Exp:Kill'], 0)
    exp_values['Headshot'] = _config.cvar(
        'headshot_xp', 45,
        config_strings['Exp:Headshot'], 0)
    exp_values['Assist'] = _config.cvar(
        'assist_xp', 15,
        config_strings['Exp:Assist'], 0)

    # Add the round experience configurations
    exp_values['Round Win'] = _config.cvar(
        'round_win_xp', 30,
        config_strings['Exp:Round Win'], 0)
    exp_values['Round Loss'] = _config.cvar(
        'round_loss_xp', 15,
        config_strings['Exp:Round Loss'], 0)

    # Add the bomb experience configurations
    exp_values['Bomb Plant'] = _config.cvar(
        'bomb_plant_xp', 15,
        config_strings['Exp:Bomb Plant'], 0)
    exp_values['Bomb Plant Team'] = _config.cvar(
        'bomb_plant_xp_team', 5,
        config_strings['Exp:Bomb Plant Team'], 0)
    exp_values['Bomb Explode'] = _config.cvar(
        'bomb_explode_xp', 25,
        config_strings['Exp:Bomb Explode'], 0)
    exp_values['Bomb Explode Team'] = _config.cvar(
        'bomb_explode_xp_team', 10,
        config_strings['Exp:Bomb Explode Team'], 0)
    exp_values['Bomb Defuse'] = _config.cvar(
        'bomb_defuse_xp', 30,
        config_strings['Exp:Bomb Defuse'], 0)
    exp_values['Bomb Defuse Team'] = _config.cvar(
        'bomb_defuse_xp_team', 15,
        config_strings['Exp:Bomb Defuse Team'], 0)

    # Add the hostage experience configurations
    exp_values['Hostage Pick Up'] = _config.cvar(
        'hostage_pickup_xp', 5,
        config_strings['Exp:Hostage Pick Up'], 0)
    exp_values['Hostage Pick Up Team'] = _config.cvar(
        'hostage_pickup_xp_team', 0,
        config_strings['Exp:Hostage Pick Up Team'], 0)
    exp_values['Hostage Rescue'] = _config.cvar(
        'hostage_rescue_xp', 25,
        config_strings['Exp:Hostage Rescue'], 0)
    exp_values['Hostage Rescue Team'] = _config.cvar(
        'hostage_rescue_xp_team', 10,
        config_strings['Exp:Hostage Rescue Team'], 0)

    # Add the multiplier configuration
    exp_multiplier = _config.cvar(
        'exp_multiplier', 1.0,
        config_strings['Exp:Multiplier'])

    # Add the required XP configurations
    required_xp_base = _config.cvar(
        'required_xp_base', 100,
        config_strings['Exp:Required Base'])
    # This value gets added to required XP for every level
    required_xp_addition = _config.cvar(
        'required_xp_addition', 20,
        config_strings['Exp:Required Addition'])

    _config.section(config_strings['Section:Gold'])

    # Add the gold gain kill configurations
    gold_values['Kill'] = _config.cvar(
        'gold_per_kill', 2,
        config_strings['Gold:Kill'])
    gold_values['Headshot'] = _config.cvar(
        'gold_per_headshot', 3,
        config_strings['Gold:Headshot'])
    gold_values['Assist'] = _config.cvar(
        'gold_per_assist', 2,
        config_strings['Gold:Assist'])

    # Add the gold gain round configurations
    gold_values['Round Win'] = _config.cvar(
        'gold_per_win', 3, config_strings['Gold:Round Win'])
    gold_values['Round Loss'] = _config.cvar(
        'gold_per_win', 2, config_strings['Gold:Round Loss'])

    # Add the skill reset cost convar
    reset_skills_cost = _config.cvar(
        'reset_skills_cost', 50,
        config_strings['Gold:Reset Skills Cost'], 0)

    # Add the item sell value multiplier convar
    item_sell_value_multiplier = _config.cvar(
        'item_sell_value_multiplier', 0.5,
        config_strings['Gold:Item Sell Value Multiplier'])

    _config.section(config_strings['Section:Hero'])

    # Add the default category configurations
    default_hero_category = _config.cvar(
        'default_hero_category', 'Others',
        config_strings['Hero:Default Hero Category'])
    default_item_category = _config.cvar(
        'default_item_category', 'Others',
        config_strings['Hero:Default Item Category'])

    # Add the starting hero convar
    starting_heroes = _config.cvar(
        'starting_heroes', 'Predz_Debug_Hero',
        config_strings['Hero:Starting Heroes'])
    starting_heroes.Notes.append(
        config_strings['Hero:Starting Heroes:Notes:0'])
