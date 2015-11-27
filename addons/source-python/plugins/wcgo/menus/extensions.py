"""Module for extended Source.Python's menus with more features."""

# Source.Python
import menus

# Warcraft: GO
from wcgo.menus import strings


class PagedMenu(menus.PagedMenu):
    """
    Extend's Source.Python's default menus package with new features
    and functionality, such as
    - constants: Display same option on all pages
    - previous_menu: presssing "Previous" on the first page
    - next_menu: pressing "Next" on the last page
    - display_page_info: Display the page number in top right corner
    """

    def __init__(
            self, data=None, select_callback=None, build_callback=None,
            description=None, title=None,
            top_seperator=strings.SEPARATOR, bottom_seperator=strings.SEPARATOR, fill=False,
            constants=None, previous_menu=None, next_menu=None,
            display_page_info=False):
        """Initializes a new PagedMenu instance."""

        super().__init__(
            data, select_callback, build_callback,
            description, title, top_seperator, bottom_seperator, fill
        )
        self.constants = constants or {}
        self.previous_menu = previous_menu
        self.next_menu = next_menu
        self.display_page_info = display_page_info

    def _get_max_item_count(self):
        """Returns the maximum possible item count per page."""

        return 6 - len(self.constants)

    def _format_header(self, player_index, page, slots):
        """Prepares the header for the menu."""

        # Create the page info string
        info = ''
        if self.display_page_info:
            info = ' [{0}/{1}]'.format(page.index + 1, self.page_count)

        if self.title:
            buffer = '{0}{1}\n'.format(
                menus.base._translate_text(self.title, player_index), info
            )
        elif info:
            buffer = '{0}\n'.format(info)
        else:
            buffer = ''

        # Set description if present
        if self.description is not None:
            buffer += menus.base._translate_text(self.description, player_index) + '\n'

        # Set the top seperator if present
        if self.top_seperator is not None:
            buffer += self.top_seperator + '\n'

        return buffer

    def _format_body(self, player_index, page, slots):
        """Prepares the body for the menu."""

        buffer = ''

        # Get all the options for the current page
        options = self._get_options(page.index)
        option_iter = iter(options)

        # Loop through numbers from 1 to 6
        choice_index = 0
        while choice_index < 7:

            # Increment the choice index
            choice_index += 1

            # See if there's a constant option for that number
            if choice_index in self.constants:
                option = self.constants[choice_index]

            # Else pick the next option from the page
            else:
                try:
                    option = next(option_iter)
                except StopIteration:
                    continue  # In case there are constants left

            # Add the option to page's options
            page.options[choice_index] = option

            # Add the option's text like SP's PagedMenu does
            if isinstance(option, menus.PagedOption):
                buffer += option._render(player_index, choice_index)
                if option.selectable:
                    slots.add(choice_index)
            else:
                choice_index -= 1
                if isinstance(option, menus.Text):
                    buffer += option._render(player_index, choice_index)
                else:
                    buffer += menus.Text(option)._render(player_index, choice_index)

        if self.fill:
            buffer += ' \n' * (6 - len(options) - len(self.constants))

        return buffer

    def _format_footer(self, player_index, page, slots):
        """Prepares the footer for the menu."""

        buffer = ''

        # Set the bottom seperator if present
        if self.bottom_seperator is not None:
            buffer += '{0}\n'.format(self.bottom_seperator)

        # Add "Previous" option
        option_previous = menus.PagedOption(
            strings.BACK,
            self.previous_menu,
            highlight=False,
            selectable=False
        )
        if page.index > 0 or self.previous_menu:
            option_previous.highlight = option_previous.selectable = True
            slots.add(7)
        buffer += option_previous._render(player_index, 7)

        # Add "Next" option
        option_next = menus.PagedOption(
            strings.NEXT,
            self.next_menu,
            highlight=False,
            selectable=False
        )
        if page.index < self.last_page_index or self.next_menu:
            option_next.highlight = option_next.selectable = True
            slots.add(8)
        buffer += option_next._render(player_index, 8)

        # Add "Close" option
        option_close = menus.PagedOption(
            strings.CLOSE,
            highlight=False
        )
        buffer += option_close._render(player_index, 9)
        slots.add(9)

        # Return the buffer
        return buffer

    def _select(self, player_index, choice_index):
        """Handles a menu selection."""

        # Do nothing if the menu is being closed
        if choice_index == 9:
            del self._player_pages[player_index]
            return None

        # Get the player's current page
        page = self._player_pages[player_index]

        # If "Previous" was clicked
        if choice_index == 7:

            # Display previous page?
            if page.index > 0:
                self.set_player_page(player_index, page.index - 1)
                return self

            # Move to previous menu?
            elif self.previous_menu:
                return self.previous_menu

        # If "Next" was clicked
        elif choice_index == 8:

            # Display Next page?
            if page.index < self.last_page_index:
                self.set_player_page(player_index, page.index + 1)
                return self

            # Move to next menu?
            elif self.next_menu:
                return self.next_menu

        # Let the super class handle the rest
        return super()._select(player_index, choice_index)