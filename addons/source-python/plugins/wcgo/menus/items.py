"""Provides the item menu instances."""

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

# Count items in list

def count_items(items_list, item_clsid):
    return sum(item.clsid == item_clsid for item in items_list)

# Sell items selection menu instance

def _item_sell_menu_build(menu, index):
    player = Player(index)
    menu.clear()
    for item in player.hero.items:
        option = menus.PagedOption(strings.CATEGORIES_ENTITY_MENU['Entity'].format(
            entity=item.name, cost='${}'.format(item.sell_value)),
            item)
        menu.append(option)

def _item_sell_menu_select(menu, index, choice):
    player = Player(index)
    item = choice.value
    player.cash += item.sell_value
    player.hero.execute_skills('item_sold', item=item, player=player)
    player.hero.items.remove(item)
    strings.message(index, 'Sell Item Success', item=item.name, cost=item.sell_value)

item_sell_menu = PagedMenu(
    title=strings.SELL_ITEM_MENU['Title'],
    build_callback=_item_sell_menu_build,
    select_callback=_item_sell_menu_select)

# Buy items selection menu instance

def _item_buy_menu_build(menu, index):
    menu.clear()
    for item in menu.items:
        option = menus.PagedOption(strings.CATEGORIES_ENTITY_MENU['Entity'].format(
            entity=item.name, cost='${}'.format(item.cost)),
            item)
        menu.append(option)

def _item_buy_menu_select(menu, index, choice):
    player = Player(index)
    item = choice.value
    if player.cash >= item.cost:
        player.hero.items.append(item())
        player.hero.execute_skills('item_purchased', item=item, player=player)
        player.cash -= item.cost
        strings.message(index, 'Buy Item Success', item=item.name, cost=item.cost)
    else:
        strings.message(index, 'Buy Item Failed', item=item.name, cost=item.cost)
    return item_categories_menu

item_buy_menu = PagedMenu(
    build_callback=_item_buy_menu_build,
    select_callback=_item_buy_menu_select)

# Buy items category menu instance

def _item_categories_menu_build(menu, index):
    player = Player(index)

    # Retrieve all items available for player
    categories = collections.defaultdict(list)
    items = wcgo.entities.Item.get_subclass_dict()
    for item in items:
        if not count_items(player.hero.items, item) >= items[item].limit:
            categories[items[item].category].append(items[item])

    menu.clear()

    # Construct menu from categories
    for category in categories:
        option = menus.PagedOption(category, (category, categories[category]))
        menu.append(option)

def _item_categories_menu_select(menu, index, choice):
    category, items = choice.value
    item_buy_menu.items = items
    item_buy_menu.title = strings.CATEGORIES_ENTITY_MENU['Title'].format(
        category=category)
    item_buy_menu.previous_menu = menu
    return item_buy_menu

item_categories_menu = PagedMenu(
    title=strings.CATEGORIES_MENU['Title'],
    build_callback=_item_categories_menu_build,
    select_callback=_item_categories_menu_select)