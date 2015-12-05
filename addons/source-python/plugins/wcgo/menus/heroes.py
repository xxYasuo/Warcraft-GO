"""Provides the hero menu instances."""

# Python 3
import collections

# Source.Python
import menus

# Warcraft: GO
import wcgo.configs as cfg
import wcgo.entities
from wcgo.menus.extensions import PagedMenu
from wcgo.menus import strings
from wcgo.player import Player


# Levelinfo formatting for use in menus

def _level_info(target):
    if target.is_max_level():
        return 'Maxed'
    return '{target.level}/{target.max_level}'.format(target=target)


# Buy hero display instance.

def _buy_hero_menu_build(menu, index):
    player = Player(index)
    hero = menu.hero

    # Construct menu ready for addition of items
    menu.title = strings.BUY_HERO_MENU['Title'].format(
        hero=hero.name)
    menu.description = strings.BUY_HERO_MENU['Description'].format(
        description=hero.description)
    can_use = player.gold >= hero.cost
    menu.constants = {6: menus.PagedOption(strings.BUY_HERO_MENU['Buy'], hero,
        highlight=can_use, selectable=can_use)}
    menu.clear()

    for passive in hero.passives:
        menu.append(strings.BUY_HERO_MENU['Passive'].format(
            passive=passive.name, description=passive.description))

    for skill in hero.skills:
        # Append the skill in iteration to the menu
        option = menus.PagedOption(
            strings.BUY_HERO_MENU['Skill'].format(
                skill=skill.name, levelinfo=_level_info(skill), description=skill.description),
            None)
        menu.append(option)

    menu.append(' \n')


def _buy_hero_menu_select(menu, index, choice):
    player = Player(index)
    hero = choice.value
    if hero is None:
        return menu
    elif hero.cost <= player.gold:
        player.heroes[hero.clsid] = hero
        player.gold -= hero.cost
        strings.message(index, 'Buy Hero Success', hero=hero.name, cost=hero.cost)
    else:
        strings.message(index, 'Buy Hero Failed', hero=hero.name, cost=hero.cost)

        
buy_hero_menu = PagedMenu(
    build_callback=_buy_hero_menu_build,
    select_callback=_buy_hero_menu_select)


# Buy heroes selection menu instance

def _buy_heroes_menu_build(menu, index):
    menu.clear()
    for hero in menu.heroes:
        option = menus.PagedOption(strings.CATEGORIES_ENTITY_MENU['Entity'].format(
            entity=hero.name, cost='{} Gold'.format(hero.cost)),
            hero)
        menu.append(option)


def _buy_heroes_menu_select(menu, index, choice):
    buy_hero_menu.hero = choice.value()
    buy_hero_menu.previous_menu = menu
    return buy_hero_menu


buy_heroes_menu = PagedMenu(
    build_callback=_buy_heroes_menu_build,
    select_callback=_buy_heroes_menu_select)


# Buy heroes category menu instance

def _buy_categories_menu_build(menu, index):
    player = Player(index)

    # Retrieve all buyable heroes available for player
    categories = collections.defaultdict(list)
    heroes = wcgo.entities.Hero.get_subclass_dict()
    for hero in heroes:
        if not hero in player.heroes:
            categories[heroes[hero].category].append(heroes[hero])

    menu.clear()

    # Construct menu from categories
    for category in categories:
        option = menus.PagedOption(category, (category, categories[category]))
        menu.append(option)


def _buy_categories_menu_select(menu, index, choice):
    category, heroes = choice.value
    buy_heroes_menu.heroes = heroes
    buy_heroes_menu.title = strings.CATEGORIES_ENTITY_MENU['Title'].format(
        category=category)
    buy_heroes_menu.previous_menu = menu
    return buy_heroes_menu


buy_categories_menu = PagedMenu(
    title=strings.CATEGORIES_MENU['Title'],
    build_callback=_buy_categories_menu_build,
    select_callback=_buy_categories_menu_select)


# Owned hero display instance.

def _owned_hero_menu_build(menu, index):
    hero = menu.hero

    # Construct menu ready for addition of items
    menu.title = strings.OWNED_HERO_MENU['Title'].format(
        hero=hero.name)
    menu.description = strings.OWNED_HERO_MENU['Description'].format(
        description=hero.description)
    menu.constants = {6: menus.PagedOption(strings.OWNED_HERO_MENU['Change'], hero)}
    menu.clear()

    for passive in hero.passives:
        menu.append(strings.OWNED_HERO_MENU['Passive'].format(
            passive=passive.name, description=passive.description))

    for skill in hero.skills:
        # Append the skill in iteration to the menu
        option = menus.PagedOption(
            strings.OWNED_HERO_MENU['Skill'].format(
                skill=skill.name, levelinfo=_level_info(skill), description=skill.description),
            None)
        menu.append(option)

    menu.append(' \n')


def _owned_hero_menu_select(menu, index, choice):
    player = Player(index)
    hero = choice.value
    if hero == None:
        return menu
    elif player.hero.clsid != hero.clsid:
        strings.message(index, 'Change Hero Success', hero=hero.name, cost=hero.cost)
        player.hero = choice.value
    else:
        strings.message(index, 'Change Hero Failed', hero=hero.name, cost=hero.cost)
        

owned_hero_menu = PagedMenu(
    build_callback=_owned_hero_menu_build,
    select_callback=_owned_hero_menu_select)


# Owned heroes selection menu instance

def _owned_heroes_menu_build(menu, index):
    menu.clear()
    for hero in menu.heroes:
        option = menus.PagedOption(hero.name, hero)
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
    player = Player(index)

    # Retrieve all heroes available for player
    categories = collections.defaultdict(list)
    for hero in player.heroes.values():
        categories[hero.category].append(hero)

    menu.clear()

    # Construct menu from categories
    for category in categories:
        option = menus.PagedOption(category, (category, categories[category]))
        menu.append(option)


def _owned_categories_menu_select(menu, index, choice):
    category, heroes = choice.value
    owned_heroes_menu.heroes = heroes
    owned_heroes_menu.title = strings.CATEGORIES_ENTITY_MENU['Title'].format(
        category=category)
    owned_heroes_menu.previous_menu = menu
    return owned_heroes_menu


owned_categories_menu = PagedMenu(
    title=strings.CATEGORIES_MENU['Title'],
    build_callback=_owned_categories_menu_build,
    select_callback=_owned_categories_menu_select)


# Current hero menu instance

def _current_hero_menu_build(menu, index):
    player = Player(index)
    hero = player.hero

    # Construct menu ready for addition of items
    menu.title = strings.CURRENT_HERO_MENU['Title']
    menu.description = strings.CURRENT_HERO_MENU['Description'].format(
        hero=hero.name, levelinfo=_level_info(hero))
    can_use = player.gold >= cfg.reset_skills_cost
    menu.constants = {6: menus.PagedOption(
                strings.CURRENT_HERO_MENU['Reset'].format(gold=cfg.reset_skills_cost),
                None,
                highlight=can_use,
                selectable=can_use)}
    menu.clear()

    for skill in hero.skills:
        # Append the skill in iteration to the menu
        can_use = not skill.is_max_level() and player.hero.skill_points >= skill.cost
        option = menus.PagedOption(
            strings.CURRENT_HERO_MENU['Skill'].format(skill=skill.name, levelinfo=_level_info(skill)),
            skill,
            highlight=can_use,
            selectable=can_use)
        menu.append(option)

    lines_to_fill = 6 - len(hero.skills)
    while lines_to_fill > 1:
        menu.append(' \n')
        lines_to_fill -= 1


def _current_hero_menu_select(menu, index, choice):
    player = Player(index)
    if choice.value is None:
        for skill in player.hero.skills:
            skill.level = 0
        player.gold -= cfg.reset_skills_cost
        strings.message(index, 'Reset Skills Success')
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
