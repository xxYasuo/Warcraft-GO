"""Provides the hero menu instances."""

# Python 3
import collections

# Source.Python
from menus import PagedOption

# Warcraft: GO
import wcgo.configs
import wcgo.entities
import wcgo.player
from wcgo.menus.extensions import PagedMenu
from wcgo.strings import menu_options
from wcgo.strings import menu_messages


# Buy hero display instance

def _buy_hero_menu_build(menu, index):
    player = wcgo.player.Player(index)
    hero_cls = menu.hero_cls
    menu.clear()

    menu.title = hero_cls.name
    menu.description = hero_cls.description
    can_use = player.gold >= hero_cls.cost
    buy_option = PagedOption(
        menu_options['Buy'], hero_cls, highlight=can_use, selectable=can_use)
    menu.constants = {6: buy_option}

    text = '{passive.name}\n{passive.description}'
    for passive_cls in hero_cls._passive_classes:
        menu.append(text.format(passive=passive_cls))

    base_text = '{{skill.name}}{max_level}\n{{skill.description}}'
    for skill_cls in hero_cls._skill_classes:
        if skill_cls.max_level is None:
            text = base_text.format(max_level='')
        else:
            text = base_text.format(max_level=' ({skill.max_level})')
        option = PagedOption(text.format(skill=skill_cls))
        menu.append(option)

    menu.append(' \n')


def _buy_hero_menu_select(menu, index, choice):
    player = wcgo.player.Player(index)
    hero_cls = choice.value
    if hero_cls is None:
        return menu
    elif hero_cls.cost <= player.gold:
        player.heroes[hero_cls.clsid] = hero_cls(owner=player)
        player.gold -= hero_cls.cost
        menu_messages['Buy Hero Success'].send(index, hero=hero_cls)
    else:
        menu_messages['Buy Hero Failed'].send(index, hero=hero_cls)


buy_hero_menu = PagedMenu(
    build_callback=_buy_hero_menu_build,
    select_callback=_buy_hero_menu_select)


# Buy heroes selection menu instance

def _buy_heroes_menu_build(menu, index):
    menu.clear()
    text = '{hero.name} ({hero.cost})'
    for hero_cls in menu.hero_classes:
        option = PagedOption(text.format(hero=hero_cls), hero_cls)
        menu.append(option)


def _buy_heroes_menu_select(menu, index, choice):
    buy_hero_menu.hero_cls = choice.value
    buy_hero_menu.previous_menu = menu
    return buy_hero_menu


buy_heroes_menu = PagedMenu(
    build_callback=_buy_heroes_menu_build,
    select_callback=_buy_heroes_menu_select)


# Buy heroes category menu instance

def _buy_categories_menu_build(menu, index):
    player = wcgo.player.Player(index)
    menu.clear()

    categories = collections.defaultdict(list)
    hero_classes = wcgo.entities.Hero.get_subclass_dict()
    for clsid, hero_cls in hero_classes.items():
        if clsid not in player.heroes:
            categories[hero_cls.category].append(hero_cls)

    for category, items in categories.items():
        option = PagedOption(category, (category, items))
        menu.append(option)


def _buy_categories_menu_select(menu, index, choice):
    category, buy_heroes_menu.hero_classes = choice.value
    buy_heroes_menu.title = category
    buy_heroes_menu.previous_menu = menu
    return buy_heroes_menu


buy_categories_menu = PagedMenu(
    title=menu_options['Buy Heroes'],
    build_callback=_buy_categories_menu_build,
    select_callback=_buy_categories_menu_select)


# Owned hero display instance.

def _owned_hero_menu_build(menu, index):
    hero = menu.hero
    menu.clear()

    menu.title = hero.name
    menu.description = hero.description
    menu.constants = {6: PagedOption(menu_options['Change'], hero)}

    text = '{passive.name}\n{passive.description}'
    for passive in hero.passives:
        menu.append(text.format(passive=passive))

    text = '{skill.name} ({skill.level_info})\n{skill.description}'
    for skill in hero.skills:
        option = PagedOption(text.format(skill=skill))
        menu.append(option)

    menu.append(' \n')


def _owned_hero_menu_select(menu, index, choice):
    player = wcgo.player.Player(index)
    hero = choice.value
    if hero is None:
        return menu
    elif player.hero.clsid != hero.clsid:
        menu_messages['Change Hero Success'].send(index, hero=hero)
        player.hero = choice.value
    else:
        menu_messages['Change Hero Failed'].send(index, hero=hero)


owned_hero_menu = PagedMenu(
    build_callback=_owned_hero_menu_build,
    select_callback=_owned_hero_menu_select)


# Owned heroes selection menu instance

def _owned_heroes_menu_build(menu, index):
    menu.clear()
    for hero in menu.heroes:
        option = PagedOption(hero.name, hero)
        menu.append(option)


def _owned_heroes_menu_select(menu, index, choice):
    owned_hero_menu.hero = choice.value
    owned_hero_menu.previous_menu = menu
    return owned_hero_menu


owned_heroes_menu = PagedMenu(
    build_callback=_owned_heroes_menu_build,
    select_callback=_owned_heroes_menu_select)


# Owned heroes category menu instance

def _owned_categories_menu_build(menu, index):
    player = wcgo.player.Player(index)
    menu.clear()

    categories = collections.defaultdict(list)
    for hero in player.heroes.values():
        categories[hero.category].append(hero)

    for category, items in categories.items():
        option = PagedOption(category, (category, items))
        menu.append(option)


def _owned_categories_menu_select(menu, index, choice):
    category, heroes = choice.value
    owned_heroes_menu.heroes = heroes
    owned_heroes_menu.title = category
    owned_heroes_menu.previous_menu = menu
    return owned_heroes_menu


owned_categories_menu = PagedMenu(
    title=menu_options['Owned Heroes'],
    build_callback=_owned_categories_menu_build,
    select_callback=_owned_categories_menu_select)


# Current hero menu instance

def _current_hero_menu_build(menu, index):
    player = wcgo.player.Player(index)
    hero = player.hero
    menu.clear()

    menu.title = menu_options['Current Hero']
    menu.description = '{hero.name} ({hero.level_info})'.format(hero=hero)
    can_use = player.gold >= wcgo.configs.reset_skills_cost
    menu.constants = {6: PagedOption(
                menu_options['Reset Skills'].get_string(
                    gold=wcgo.configs.reset_skills_cost),
                highlight=can_use,
                selectable=can_use)}

    text = '{skill.name} ({skill.level_info})'
    for skill in hero.skills:
        can_use = not skill.is_max_level() and hero.skill_points >= skill.cost
        option = PagedOption(
            text.format(skill=skill),
            skill,
            highlight=can_use,
            selectable=can_use)
        menu.append(option)

    lines_to_fill = 6 - len(hero.skills)
    menu.extend([' \n'] * lines_to_fill)


def _current_hero_menu_select(menu, index, choice):
    player = wcgo.player.Player(index)
    if choice.value is None:
        for skill in player.hero.skills:
            skill.level = 0
        player.gold -= wcgo.configs.reset_skills_cost
        menu_messages['Reset Skills Success'].send(index)
    else:
        skill = choice.value
        if (skill.cost <= player.hero.skill_points and
                skill.required_level <= player.hero.level and
                not skill.is_max_level()):
            skill.level += 1
    return menu


current_hero_menu = PagedMenu(
    build_callback=_current_hero_menu_build,
    select_callback=_current_hero_menu_select)
