"""Provides the hero menu instances."""

# Source.Python
import menus

# Warcraft: GO
import wcgo.configs as cfg
from wcgo.menus.extensions import PagedMenu
import wcgo.menus.strings as strings
from wcgo.player import Player

def _current_hero_menu_build(menu, index):
    player = Player(index)
    hero = player.hero
    levelinfo = '{hero.level}/{hero.max_level}'.format(hero=hero)
        if not hero.is_max_level() else 'Maxed'

    # Construct menu ready for addition of items
    menu.title = strings.CURRENT_HERO_MENU['Title'].format(
        hero=hero.name,
        levelinfo=levelinfo
        )
    menu.description = hero.description
    menu.clear()

    position = 1
    for skill in hero.skills:
        # Check whether reset should be added
        if position % 6 == 0:
            menu.append(menus.PagedOption(
                strings.CURRENT_HERO_MENU['Reset'].format(gold=cfg.reset_skills_cost),
                None))

        # Append the skill in iteration to the menu
        levelinfo = '{skill.level}/{skill.max_level}'.format(skill=skill)
            if not skill.is_max_level() else 'Maxed'
        menu.append(menus.PagedOption(
            strings.CURRENT_HERO_MENU['Reset'].format(skill=skill.name, levelinfo=levelinfo),
            skill))
        position += 1

def _current_hero_menu_select(menu, index, choice):
    player = Player(index)
    if choice.value is None:
        if player.gold >= cfg.reset_skills_cost:
            for skill in player.hero.skills:
                skill.level = 0
            player.gold -= 50
    else:
        if (skill.cost <= player.hero.skill_points and
            skill.required_level <= player.hero.level and
            not skill.is_max_level()):
            skill.level += 1
    return menu

current_hero_menu = PagedMenu(
    build_callback= _current_hero_menu_build,
    select_callback=_current_hero_menu_select
)