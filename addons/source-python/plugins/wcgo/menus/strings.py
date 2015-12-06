"""Module containing all menu strings."""

# Source.Python
from messages import SayText2
from translations.strings import LangStrings

# Warcraft: GO
from wcgo.info import info


def message(player_index, msg_id, **kwargs):
    """Send a message to a player."""
    SayText2(MENU_MESSAGES[msg_id]).send(player_index, **kwargs)

SEPARATOR = ' '
BACK = 'Back'
NEXT = 'Next'
CLOSE = 'Close'

MENU_MESSAGES = LangStrings(info.basename + '/menus')

MAIN_MENU = {
    'Title': 'Warcraft (Main Menu)',
    'Gold': '{gold} Gold',
    'Current Hero': 'Current Hero',
    'Owned Heroes': 'Owned Heroes',
    'Buy Heroes': 'Buy Heroes',
    'Buy Items': 'Buy Items',
    'Sell Items': 'Sell Items',
    'Player Info': 'Playerinfo',
}

CURRENT_HERO_MENU = {
    'Title': 'Warcraft (Current Hero)',
    'Description': '{hero} ({levelinfo})',
    'Skill': '{skill} ({levelinfo})',
    'Reset': 'Reset Skills ({gold} Gold)',
}

CATEGORIES_ENTITY_MENU = {
    'Title': 'Warcraft ({category})',
    'Entity': '{entity} ({cost})',
}

CATEGORIES_MENU = {
    'Title': 'Warcraft (Categories)',
}

OWNED_HERO_MENU = {
    'Title': 'Warcraft ({hero})',
    'Description': '{description}',
    'Change': 'Change',
    'Passive': 'P. {passive} \n{description}',
    'Skill': '{skill} ({levelinfo})\n{description}',
}

BUY_HERO_MENU = {
    'Title': 'Warcraft ({hero})',
    'Description': '{description}',
    'Buy': 'Buy',
    'Passive': 'P. {passive} \n{description}',
    'Skill': '{skill} ({levelinfo})\n{description}',
}

SELL_ITEM_MENU = {
    'Title': 'Warcraft (Sell)',
}

PLAYER_LIST_MENU = {
    'Title': 'Warcraft (Players)',
    'Player': '{name}',
}

PLAYER_INFO_MENU = {
    'Title': 'Warcraft ({name})',
    'Description': '{hero} ({levelinfo})',
    'Skill': '- {skill} ({levelinfo})',
}
