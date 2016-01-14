"""Module for supplying a level up effect."""

# Source.Python
from colors import Color
from entities.entity import Entity
from listeners.tick import Delay
from mathlib import NULL_VECTOR

# Warcraft: GO
from wcgo.effects import models

# Globals
_tick_model = models['effects/yellowflare.vmt']


def level_up(player):
    """Display the level up effect on a player."""
    entity = Entity.create('env_smokestack')

    # This might be completely unnecessary.
    # The only time I can think that this might be necessary is
    #   if the max entity limit is reached, but I am not sure this would
    #   catch that, or if there would be another error that would occur.
    if not entity.basehandle.is_valid():
        return

    entity.teleport(player.origin, None, None)
    entity.base_spread = 10
    entity.spread_speed = 60
    entity.initial_state = 0
    entity.speed = 105
    entity.rate = 50
    entity.start_size = 7
    entity.end_size = 2
    entity.twist = 0
    entity.jet_length = 100
    entity.angles = NULL_VECTOR
    entity.render_mode = 18
    entity.render_amt = 100
    entity.render_color = Color(255, 255, 3)
    entity.add_output('SmokeMaterial effects/yellowflare.vmt')
    entity.turn_on()
    entity.set_parent(player.pointer, -1)
    Delay(2, _remove_smoke, entity)


def _remove_smoke(entity):
    """Remove the env_smokestack entity."""
    # This check should be necessary as the 2 second delay could have caused
    #   the entity to be removed by some other means (including round restart).
    if not entity.basehandle.is_valid():
        return
    entity.turn_off()
    entity.remove()
