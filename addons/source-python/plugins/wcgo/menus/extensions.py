"""Module for extended Source.Python's menus with more features."""

# Source.Python
import menus

# Warcraft: GO
import wcsgo.menus.strings as strings


class PagedMenu(menus.PagedMenu):
    """PagedMenu with previous menu support."""

    def __init__(
            self, data=None, select_callback=None, build_callback=None,
            description=None, title=None, fill=False, previous_menu=None,
            top_seperator=strings.SEPARATOR, bottom_seperator=strings.SEPARATOR):
        """Initialize a paged menu."""
        super().__init__(
            data, select_callback, build_callback,
            description, title, top_seperator, bottom_seperator, fill)
        self.previous_menu = previous_menu

    def _select(self, player_index, choice_index):
        """Return to previous menu if on page 0 and Back was clicked."""
        page = self._player_pages[player_index]
        if choice_index == 7 and self.previous_menu is not None and page.index == 0:
            return self.previous_menu
        return super()._select(player_index, choice_index)