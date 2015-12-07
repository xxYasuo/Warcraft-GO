"""Provides the main menu instance."""

# Source.Python
import menus

# Warcraft: GO
import wcgo.configs
import wcgo.player
import wcgo.strings
from wcgo.menus.heroes import current_hero_menu
from wcgo.menus.heroes import owned_categories_menu
from wcgo.menus.heroes import buy_categories_menu
from wcgo.menus.items import item_categories_menu
from wcgo.menus.items import item_sell_menu
from wcgo.menus.players import player_list_menu


# Menu translations
_tr = wcgo.strings.menus['main']


# Main menu instance

def _main_menu_build(menu, index):
    player = wcgo.player.Player(index)
    menu[1].text = _tr['Gold'].get_string(gold=player.gold)


def _main_menu_select(menu, index, choice):
    next_menu = choice.value
    if next_menu is not None:
        next_menu.previous_menu = menu
        return next_menu


main_menu = menus.SimpleMenu(
    [
        menus.Text(_tr['Title']),
        menus.Text(' '),
        menus.Text(wcgo.configs.menu_separator),
        menus.SimpleOption(1, _tr['Current Hero'], current_hero_menu),
        menus.SimpleOption(2, _tr['Owned Heroes'], owned_categories_menu),
        menus.SimpleOption(3, _tr['Buy Heroes'], buy_categories_menu),
        menus.Text(wcgo.configs.menu_separator),
        menus.SimpleOption(4, _tr['Buy Items'], item_categories_menu),
        menus.SimpleOption(5, _tr['Sell Items'], item_sell_menu),
        menus.Text(wcgo.configs.menu_separator),
        menus.SimpleOption(6, _tr['Player Info'], player_list_menu),
        menus.Text(wcgo.configs.menu_separator),
        menus.SimpleOption(9, wcgo.strings.menus['defaults']['Close'], highlight=False)
    ],
    build_callback=_main_menu_build,
    select_callback=_main_menu_select)
