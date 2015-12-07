"""Provides the player info menu instance."""

# Source.Python
from menus import PagedOption

# Warcraft: GO
import wcgo.entities
import wcgo.player
import wcgo.strings
from wcgo.menus.extensions import PagedMenu


def _level_info(entity):
    """Get entity's level information as a string."""
    if entity.is_max_level():
        return 'Maxed'
    if entity.max_level is not None:
        return '{entity.level}/{entity.max_level}'.format(entity=entity)
    return entity.level


# Translations for menus
_tr = wcgo.strings.menus


# Player list menu instance

def _player_list_menu_build(menu, index):
    menu.clear()
    for player in wcgo.player.PlayerIter():
        option = PagedOption(
            _tr['player_list']['Player'].get_string(name=player.name), player)
        menu.append(option)


def _player_list_menu_select(menu, index, choice):
    player = choice.value
    player_info_menu.title = _tr['player_info']['Title'].get_string(name=player.name)
    player_info_menu.target = player
    player_info_menu.previous_menu = menu
    return player_info_menu


player_list_menu = PagedMenu(
    title=_tr['player_list']['Title'],
    build_callback=_player_list_menu_build,
    select_callback=_player_list_menu_select)


# Player info menu instance

def _player_info_menu_build(menu, index):
    player = menu.target
    hero = player.hero

    menu.description = _tr['player_info']['Description'].get_string(
        hero=hero.name, levelinfo=_level_info(hero))
    menu.clear()

    for skill in hero.skills:
        option = _tr['player_info']['Skill'].get_string(
            skill=skill.name, levelinfo=_level_info(skill))
        menu.append(option)

    lines_to_fill = 6 - len(hero.skills)
    menu.extend([' \n'] * lines_to_fill)


def _player_info_menu_select(menu, index, choice):
    return menu


player_info_menu = PagedMenu(
    build_callback=_player_info_menu_build,
    select_callback=_player_info_menu_select)