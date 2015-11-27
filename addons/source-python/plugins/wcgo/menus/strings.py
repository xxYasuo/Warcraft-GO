"""Module for Wacraft: GO menu strings."""

SEPARATOR = ' '
BACK = 'Back'
NEXT = 'Next'
CLOSE = 'Close'

MAIN_MENU = {
    'Title': 'Warcraft (Main Menu)',
    'Gold': '{gold} Gold',
    'Current Hero': 'Current Hero',
    'Owned Heroes': 'Owned Heroes',
    'Buy Heroes': 'Buy Heroes',
}

CURRENT_HERO_MENU = {
    'Title': 'Warcraft (Current Hero)',
    'Description': '{hero} ({levelinfo})',
    'Skill': '{skill} ({levelinfo})',
    'Reset': 'Reset Skills ({gold} Gold)',
}

CATEGORIES_HEROES_MENU = {
    'Title': 'Warcraft ({category})',
}

CATEGORIES_MENU = {
    'Title': 'Warcraft (Categories)',
}

OWNED_HERO_MENU = {
    'Title': 'Warcraft ({hero})',
    'Description': '- {description}',
    'Change': 'Change',
    'Skill': '{skill} ({levelinfo})\n{description}',
}