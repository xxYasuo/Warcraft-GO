"""Sub-module for Wacraft: GO initial menu."""

# Source.Python
from menus import SimpleMenu
from menus import SimpleOption
from menus import Text

# Warcraft: GO
from wcgo.menus.heroes import currenthero
from wcgo.menus.strings import mainmenu
from wcgo.menus.strings import separator
from wcgo.menus.strings import close

def _main_menu_selection(menu, index, choice):
    if choice.value is None:
        return
    menu = choice.value
    menu.previous_menu = menu
    return menu

menu = SimpleMenu(select_callback=_main_menu_selection)
menu.append([
    Text(mainmenu['title']),
    Text(separator),
    SimpleOption(1, mainmenu['currenthero'], currenthero),
    Text(separator),
    SimpleOption(9, close, None)
])