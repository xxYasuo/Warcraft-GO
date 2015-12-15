"""Provides the player info menu instance."""

# Source.Python
from menus import PagedOption

# Warcraft: GO
import wcgo.entities
import wcgo.player
from wcgo.menus.extensions import PagedMenu
from wcgo.strings import menu_messages
from wcgo.strings import menu_options


# Player list menu instance

def _player_list_menu_build(menu, index):
    menu.clear()
    for player in wcgo.player.PlayerIter():
        option = PagedOption(player.name, player)
        menu.append(option)


def _player_list_menu_select(menu, index, choice):
    player = choice.value
    player_info_menu.title = player.name
    player_info_menu.target = player
    player_info_menu.previous_menu = menu
    return player_info_menu


player_list_menu = PagedMenu(
    title=menu_options['Player Info'],
    build_callback=_player_list_menu_build,
    select_callback=_player_list_menu_select)


# Player info menu instance

def _player_info_menu_build(menu, index):
    player = menu.target
    hero = player.hero

    menu.description = '{hero.name}\n{hero.description}'.format(hero=hero)
    menu.clear()

    text = '- {skill.name} ({skill.level_info})'
    for skill in hero.skills:
        option = text.format(skill=skill)
        menu.append(option)

    lines_to_fill = 6 - len(hero.skills)
    menu.extend([' \n'] * lines_to_fill)


def _player_info_menu_select(menu, index, choice):
    return menu


player_info_menu = PagedMenu(
    build_callback=_player_info_menu_build,
    select_callback=_player_info_menu_select)