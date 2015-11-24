"""Module for containing Wacraft: GO menu extensions."""

# Source.Python
from menus import PagedMenu as Menu

# Warcraft: GO
from wcgo.menus.strings import separator

class PagedMenu(Menu):
    """Subclassed PagedMenu to add previous menu support."""

    def __init__(
            self, data=None, select_callback=None, build_callback=None,
            description=None, title=None,
            top_seperator=separator, bottom_seperator=separator, fill=False, previous_menu=None):

        super().__init__(
            data, select_callback, build_callback,
            description, title, top_seperator, bottom_seperator, fill
        )
        self.previous_menu = previous_menu

    def _select(self, player_index, choice_index):
        if choice_index == 7:
            if self.previous_menu and page.index == 0:
                return self.previous_menu

        return super()._select(player_index, choice_index)