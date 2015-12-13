"""Provides the hero menu instances."""

# Python 3
import collections

# Source.Python
from menus import PagedOption

# Warcraft: GO
import wcgo.configs
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


# Buy hero display instance

def _buy_hero_menu_build(menu, index):
    player = wcgo.player.Player(index)
    hero_cls = menu.hero_cls

    # Construct menu ready for addition of items
    menu.title = _tr['buy_hero']['Title'].get_string(hero=hero_cls.name)
    menu.description = _tr['buy_hero']['Description'].get_string(
        description=hero_cls.description)
    can_use = player.gold >= hero_cls.cost
    buy_option = PagedOption(
        _tr['buy_hero']['Buy'], hero_cls, highlight=can_use, selectable=can_use)
    menu.constants = {6: buy_option}
    menu.clear()

    for passive_cls in hero_cls._passive_classes:
        menu.append(_tr['buy_hero']['Passive'].get_string(
            passive=passive_cls.name, description=passive_cls.description))

    for skill_cls in hero_cls._skill_classes:
        # Append the skill in iteration to the menu
        option = PagedOption(
            _tr['buy_hero']['Skill'].get_string(
                skill=skill_cls.name,
                levelinfo='Levels: {0}'.format(skill_cls.max_level),
                description=skill_cls.description),
            None)
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
        wcgo.strings.menu_messages['Buy Hero Success'].send(index, hero=hero_cls)
    else:
        wcgo.strings.menu_messages['Buy Hero Failed'].send(index, hero=hero_cls)


buy_hero_menu = PagedMenu(
    build_callback=_buy_hero_menu_build,
    select_callback=_buy_hero_menu_select)


# Buy heroes selection menu instance

def _buy_heroes_menu_build(menu, index):
    menu.clear()
    for hero_cls in menu.hero_classes:
        option = PagedOption(_tr['categories']['Entity'].get_string(
            entity=hero_cls.name, cost='{0} Gold'.format(hero_cls.cost)),
            hero_cls)
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

    # Retrieve all buyable heroes available for player
    categories = collections.defaultdict(list)
    hero_classes = wcgo.entities.Hero.get_subclass_dict()
    for clsid, hero_cls in hero_classes.items():
        if clsid not in player.heroes:
            categories[hero_cls.category].append(hero_cls)

    menu.clear()

    # Construct menu from categories
    for category in categories:
        option = PagedOption(category, (category, categories[category]))
        menu.append(option)


def _buy_categories_menu_select(menu, index, choice):
    category, buy_heroes_menu.hero_classes = choice.value
    buy_heroes_menu.title = _tr['categories']['Title'].get_string(category=category)
    buy_heroes_menu.previous_menu = menu
    return buy_heroes_menu


buy_categories_menu = PagedMenu(
    title=_tr['categories']['Title'],
    build_callback=_buy_categories_menu_build,
    select_callback=_buy_categories_menu_select)


# Owned hero display instance.

def _owned_hero_menu_build(menu, index):
    hero = menu.hero

    # Construct menu ready for addition of items
    menu.title = _tr['owned_hero']['Title'].get_string(hero=hero.name)
    menu.description = _tr['owned_hero']['Description'].get_string(
        description=hero.description)
    menu.constants = {6: PagedOption(_tr['owned_hero']['Change'], hero)}
    menu.clear()

    for passive in hero.passives:
        menu.append(_tr['owned_hero']['Passive'].get_string(
            passive=passive.name, description=passive.description))

    for skill in hero.skills:
        # Append the skill in iteration to the menu
        option = PagedOption(
            _tr['owned_hero']['Skill'].get_string(
                skill=skill.name, levelinfo=_level_info(skill), description=skill.description),
            None)
        menu.append(option)

    menu.append(' \n')


def _owned_hero_menu_select(menu, index, choice):
    player = wcgo.player.Player(index)
    hero = choice.value
    if hero is None:
        return menu
    elif player.hero.clsid != hero.clsid:
        wcgo.strings.menu_messages['Change Hero Success'].send(index, hero=hero.name)
        player.hero = choice.value
    else:
        wcgo.strings.menu_messages['Change Hero Failed'].send(index, hero=hero.name)


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

    # Retrieve all heroes available for player
    categories = collections.defaultdict(list)
    for hero in player.heroes.values():
        categories[hero.category].append(hero)

    menu.clear()

    # Construct menu from categories
    for category in categories:
        option = PagedOption(category, (category, categories[category]))
        menu.append(option)


def _owned_categories_menu_select(menu, index, choice):
    category, heroes = choice.value
    owned_heroes_menu.heroes = heroes
    owned_heroes_menu.title = _tr['categories']['Title'].get_string(category=category)
    owned_heroes_menu.previous_menu = menu
    return owned_heroes_menu


owned_categories_menu = PagedMenu(
    title=_tr['categories']['Title'],
    build_callback=_owned_categories_menu_build,
    select_callback=_owned_categories_menu_select)


# Current hero menu instance

def _current_hero_menu_build(menu, index):
    player = wcgo.player.Player(index)
    hero = player.hero

    # Construct menu ready for addition of items
    menu.title = _tr['current_hero']['Title']
    menu.description = _tr['current_hero']['Description'].get_string(
        hero=hero.name, levelinfo=_level_info(hero))
    cost = wcgo.configs.reset_skills_cost.get_int()
    can_use = player.gold >= cost
    menu.constants = {6: PagedOption(
                _tr['current_hero']['Reset'].get_string(gold=cost),
                None,
                highlight=can_use,
                selectable=can_use)}
    menu.clear()

    for skill in hero.skills:
        # Append the skill in iteration to the menu
        can_use = not skill.is_max_level() and player.hero.skill_points >= skill.cost
        option = PagedOption(
            _tr['current_hero']['Skill'].get_string(
                skill=skill.name, levelinfo=_level_info(skill)),
            skill,
            highlight=can_use,
            selectable=can_use)
        menu.append(option)

    lines_to_fill = 6 - len(hero.skills)
    while lines_to_fill > 1:
        menu.append(' \n')
        lines_to_fill -= 1


def _current_hero_menu_select(menu, index, choice):
    player = wcgo.player.Player(index)
    if choice.value is None:
        for skill in player.hero.skills:
            skill.level = 0
        player.gold -= wcgo.configs.reset_skills_cost.get_int()
        wcgo.strings.menu_messages['Reset Skills Success'].send(index)
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
