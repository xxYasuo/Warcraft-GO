"""Package for Wacraft: GO menu and admin systems."""

# Warcraft: GO
from wcgo.menus.main import main_menu
from wcgo.menus.heroes import current_hero_menu

__all__ = (
    main_menu,
    current_hero_menu,
)