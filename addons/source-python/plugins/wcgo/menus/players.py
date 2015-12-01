"""Provides the player info menu instance."""

# Source.Python
import menus

# Warcraft: GO
import wcgo.configs as cfg
import wcgo.entities
from wcgo.menus.extensions import PagedMenu
from wcgo.menus import strings
from wcgo.player import Player
from wcgo.player import PlayerIter

# Levelinfo formatting for use in menus

def _level_info(target):
    if target.is_max_level():
        return 'Maxed'
    return '{target.level}/{target.max_level}'.format(target=target)

# Player list menu instance

def _player_list_menu_build(menu, index):
    menu.clear()
    for player in PlayerIter():
        option = menus.PagedOption(strings.PLAYER_LIST_MENU['Player'].format(
            name=player.name), player)
        menu.append(option)

def _player_list_menu_select(menu, index, choice):
    player = choice.value
    player_info_menu.title = strings.PLAYER_INFO_MENU['Title'].format(
        name=player.name)
    player_info_menu.target = player
    player_info_menu.previous_menu = menu
    return player_info_menu

player_list_menu = PagedMenu(
    title=strings.PLAYER_LIST_MENU['Title'],
    build_callback=_player_list_menu_build,
    select_callback=_player_list_menu_select)

# Player info menu instance

def _player_info_menu_build(menu, index):
    player = menu.target
    hero = player.hero

    menu.description = strings.PLAYER_INFO_MENU['Description'].format(
        hero=hero.name, levelinfo=_level_info(hero))
    menu.clear()

    for skill in hero.skills:
        # Append the skill in iteration to the menu
        option = strings.PLAYER_INFO_MENU['Skill'].format(skill=skill.name, levelinfo=_level_info(skill))
        menu.append(option)

    lines_to_fill = 6 - len(hero.skills)
    while lines_to_fill > 1:
        menu.append(' \n')
        lines_to_fill -= 1

def _player_info_menu_select(menu, index, choice):
    return menu

player_info_menu = PagedMenu(
    build_callback=_player_info_menu_build,
    select_callback=_player_info_menu_select)