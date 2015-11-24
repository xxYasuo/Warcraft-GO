"""Module for Wacraft: GO menu strings."""

SEPARATOR = ' '
BACK = 'Back'
NEXT = 'Next'
CLOSE = 'Close'

MAIN_MENU = {
    'Title': 'Warcraft (Main Menu)',
    'Gold': '- {gold} Gold',
    'Current Hero': 'Current Hero',
    'Owned Heroes': 'Owned Heroes',
    'Buy Heroes': 'Buy Heroes',
}

CURRENT_HERO_MENU = {
    'Title': '{hero} ({levelinfo})',
    'Skill': '{skill} ({levelinfo})',
    'Reset': 'Reset Skills ({gold} Gold)',
}

OWNED_HEROES_MENU = {
    'Title': 'Warcraft (Owned Heroes)',
    'Change': 'Change'
    'Hero': '{hero} ({levelinfo})'
    'Skill': '{skill} ({levelinfo})\n{description}'
}