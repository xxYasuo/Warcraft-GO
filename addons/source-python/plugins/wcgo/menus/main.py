"""Provides the main_menu instance."""

# Source.Python
import menus

# Warcraft: GO
import wcgo.menus.strings as strings
from wcgo.menus.heroes import current_hero_menu


def _main_menu_select(menu, index, choice):
    """Select callback for main menu."""
    next_menu = choice.value
    if next_menu is not None:
        next_menu.previous_menu = menu
        return next_menu


menu_main = menus.SimpleMenu(
    [
        menus.Text(strings.MAIN_MENU['Title']),
        menus.Text(strings.SEPARATOR),
        menus.SimpleOption(1, strings.MAIN_MENU['Current Hero'], current_hero_menu),
        menus.Text(strings.SEPARATOR),
        menus.SimpleOption(9, strings.CLOSE, None)
    ],
    select_callback=_main_menu_select
)
