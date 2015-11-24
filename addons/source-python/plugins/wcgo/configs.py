"""This module contains configurable settings for server operators."""

# Imports -- these are required for this file to work, don't edit
import os

# Admins' SteamIDs, separated by commas
admins = (
    'STEAM_0:0:20178479',  # Mahi
    'STEAM_1:0:120220385',  # Predz
)

# Amounts of experience points to gain from objectives
exp_values = {

    # Kill values
    'Kill': 30,
    'Headshot': 15,
    'Assist': 15,

    # Round values
    'Round Win': 30,
    'Round Loss': 15,

    # Bomb values
    'Bomb Plant': 15,
    'Bomb Plant Team': 5,
    'Bomb Explode': 25,
    'Bomb Explode Team ': 10,
    'Bomb Defuse': 30,
    'Bomb Defuse Team ': 15,

    # Hostage values
    'Hostage Pick Up': 5,
    'Hostage Pick Up Team': 0,
    'Hostage Rescue': 25,
    'Hostage Rescue Team': 10
}

# Multiplier for experience points gained upon events
exp_multiplier = 1.0

# Amounts of gold gained from objectives
gold_values = {

    # Kill values
    'Kill': 2,
    'Assist': 1,

    # Round values
    'Round Win': 3,
    'Round Loss': 2
}

# Show messages for gold gain
show_gold_messages = True

# Prefix for messages sent by the plugin
message_prefix = '>> WCGO: '

reset_skills_cost = 50

# Starting heroes for when an user joins the server for the first time
starting_heroes = (
    'Test_Hero',
)

# Hero category to use when no category is defined
default_hero_category = 'others'

# Item category to use when no category is defined
default_item_category = 'others'

# Items' default sell value's multiplier
item_sell_value_multiplier = 0.5

# Base value for the experience points required to level up 
required_xp_base = 100

# This value gets added to required XP for every level
required_xp_addition = 20

# Path to database file (don't edit if unsure of what it does)
database_path = os.path.join(os.path.dirname(__file__), 'wcgo.db')
