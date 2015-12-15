"""Provides the item menu instances."""

# Python 3
import collections

# Source.Python
from menus import PagedOption

# Warcraft: GO
import wcgo.entities
import wcgo.player
from wcgo.menus.extensions import PagedMenu
from wcgo.strings import menu_messages
from wcgo.strings import menu_options


# Sell items selection menu instance

def _item_sell_menu_build(menu, index):
    player = wcgo.player.Player(index)
    menu.clear()
    text = '{item.name} ({item.sell_value})'
    for item in player.hero.items:
        option = PagedOption(text.format(item=item), item)
        menu.append(option)


def _item_sell_menu_select(menu, index, choice):
    player = wcgo.player.Player(index)
    item = choice.value
    player.cash += item.sell_value
    item.execute_method('item_sell', item=item, player=player)
    player.hero.items.remove(item)
    menu_messages['Sell Item Success'].send(index, item=item)


item_sell_menu = PagedMenu(
    title=menu_options['Sell Items'],
    build_callback=_item_sell_menu_build,
    select_callback=_item_sell_menu_select)


# Buy items selection menu instance

def _item_buy_menu_build(menu, index):
    player = wcgo.player.Player(index)
    menu.clear()
    text = '{item.name} ({item.cost})'
    for item in menu.items:
        highlight = player.cash >= item.cost
        option = PagedOption(text.format(item=item), item, highlight=highlight)
        menu.append(option)


def _item_buy_menu_select(menu, index, choice):
    player = wcgo.player.Player(index)
    item = choice.value
    if player.cash >= item.cost:
        item = item(owner=player)
        player.hero.items.append(item)
        item.execute_method('item_purchase', item=item, player=player)
        player.cash -= item.cost
        menu_messages['Buy Item Success'].send(index, item=item)
    else:
        menu_messages['Buy Item Failed'].send(index, item=item)
    return item_categories_menu


item_buy_menu = PagedMenu(
    build_callback=_item_buy_menu_build,
    select_callback=_item_buy_menu_select)


# Buy items category menu instance

def _item_categories_menu_build(menu, index):
    player = wcgo.player.Player(index)
    menu.clear()

    categories = collections.defaultdict(list)
    item_classes = wcgo.entities.Item.get_subclass_dict()
    item_counter = collections.Counter(item.clsid for item in player.hero.items)
    for clsid, item_cls in item_classes.items():
        if item_counter[clsid] < item_cls.limit:
            categories[item_cls.category].append(item_cls)

    for category, items in categories.items():
        option = PagedOption(category, (category, items))
        menu.append(option)


def _item_categories_menu_select(menu, index, choice):
    category, items = choice.value
    item_buy_menu.items = items
    item_buy_menu.title = category
    item_buy_menu.previous_menu = menu
    return item_buy_menu


item_categories_menu = PagedMenu(
    build_callback=_item_categories_menu_build,
    select_callback=_item_categories_menu_select)
