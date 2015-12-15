"""Provides the main menu instance."""

# Source.Python
from menus import SimpleMenu
from menus import SimpleOption
from menus import Text

# Warcraft: GO
import wcgo.configs
import wcgo.player
from wcgo.strings import menu_options
from wcgo.menus.heroes import current_hero_menu
from wcgo.menus.heroes import owned_categories_menu
from wcgo.menus.heroes import buy_categories_menu
from wcgo.menus.items import item_categories_menu
from wcgo.menus.items import item_sell_menu
from wcgo.menus.players import player_list_menu


# Main menu instance

def _main_menu_build(menu, index):
    player = wcgo.player.Player(index)
    menu[1].text = menu_options['Gold'].get_string(gold=player.gold)


def _main_menu_select(menu, index, choice):
    next_menu = choice.value
    if next_menu is not None:
        next_menu.previous_menu = menu
        return next_menu


main_menu = SimpleMenu(
    [
        Text(menu_options['Main Menu']),
        Text(' '),
        Text(wcgo.configs.menu_separator.get_string()),
        SimpleOption(1, menu_options['Current Hero'], current_hero_menu),
        SimpleOption(2, menu_options['Owned Heroes'], owned_categories_menu),
        SimpleOption(3, menu_options['Buy Heroes'], buy_categories_menu),
        Text(wcgo.configs.menu_separator.get_string()),
        SimpleOption(4, menu_options['Buy Items'], item_categories_menu),
        SimpleOption(5, menu_options['Sell Items'], item_sell_menu),
        Text(wcgo.configs.menu_separator.get_string()),
        SimpleOption(6, menu_options['Player Info'], player_list_menu),
        Text(wcgo.configs.menu_separator.get_string()),
        SimpleOption(9, menu_options['Close'], highlight=False),
    ],
    build_callback=_main_menu_build,
    select_callback=_main_menu_select)
