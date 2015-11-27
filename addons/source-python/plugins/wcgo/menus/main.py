"""Provides the main_menu instance."""

# Source.Python
import menus

# Warcraft: GO
from wcgo.menus import strings
from wcgo.menus.heroes import current_hero_menu
from wcgo.menus.heroes import owned_categories_menu
from wcgo.player import Player


def _main_menu_build(menu, index):
    player = Player(index)
    menu[1].text = menu[1].text.format(gold=player.gold)

def _main_menu_select(menu, index, choice):
    next_menu = choice.value
    if next_menu is not None:
        next_menu.previous_menu = menu
        return next_menu

main_menu = menus.SimpleMenu(
    [
        menus.Text(strings.MAIN_MENU['Title']),
        menus.Text(strings.MAIN_MENU['Gold']),
        menus.Text(strings.SEPARATOR),
        menus.SimpleOption(1, strings.MAIN_MENU['Current Hero'], current_hero_menu),
        menus.SimpleOption(2, strings.MAIN_MENU['Owned Heroes'], owned_categories_menu),
        menus.Text(strings.SEPARATOR),
        menus.SimpleOption(9, strings.CLOSE, None)
    ],
    build_callback=_main_menu_build, select_callback=_main_menu_select)
