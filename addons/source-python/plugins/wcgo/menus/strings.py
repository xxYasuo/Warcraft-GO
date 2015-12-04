"""Module containing all menu strings."""

# Source.Python
from messages import SayText2

# Warcraft: GO
from wcgo.configs import message_template


def message(index, msg_id, **kwargs):
    """Send a message to a player."""
    message = MESSAGES[msg_id].format(**kwargs)
    SayText2(message_template.format(message)).send(index)

SEPARATOR = ' '
BACK = 'Back'
NEXT = 'Next'
CLOSE = 'Close'

MESSAGES = {
    'Change Hero Success': '\x01Changed hero to \x05{hero}\x01.',
    'Change Hero Failed': '\x01Cannot change hero to \x05{hero}\x01.',
    'Buy Hero Success': '\x01Purchased \x05{hero} \x01for \x07{cost} gold\x01.',
    'Buy Hero Failed': '\x01Cannot purchase \x05{hero} \x01for \x07{cost} gold\x01.',
    'Reset Skills Success': '\x01Reset your \x05current skills \x04to 0.',
    'Reset Skills Failed': '\x01Resetting your \x04skills \x01costs \x07{cost} gold\x01.',
    'Buy Item Success': '\x01Purchased \x05{item} \x01for \x07${cost}\x01.',
    'Buy Item Failed': '\x01Cannot purchase \x05{item} \x01for \x07${cost}\x01.',
    'Sell Item Success': '\x01Sold \x05{item} \x01for \x07${cost}\x01.',
}

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
    'Skill': '{skill} ({levelinfo})\n{description}',
}

BUY_HERO_MENU = {
    'Title': 'Warcraft ({hero})',
    'Description': '{description}',
    'Buy': 'Buy',
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