"""Module for supplying a level up effect."""

# Source.Python
from entities.entity import Entity
from entities.helpers import index_from_pointer
from listeners.tick import tick_delays

# Warcraft: GO
from wcgo.effects import models

# Globals
_tick_model = models['effects/yellowflare.vmt']


def level_up(player):
    """Display the level up effect on a player."""
    pointer = player.give_named_item('env_smokestack', 0, None, False)
    entity = Entity(index_from_pointer(pointer))
    entity.add_output('basespread 10')
    entity.add_output('spreadspeed 60')
    entity.add_output('initial 0')
    entity.add_output('speed 105')
    entity.add_output('rate 50')
    entity.add_output('startsize 7')
    entity.add_output('endsize 2')
    entity.add_output('twist 0')
    entity.add_output('jetlength 100')
    entity.add_output('angles 0 0 0')
    entity.add_output('rendermode 18')
    entity.add_output('renderamt 100')
    entity.add_output('rendercolor 255 255 3')
    entity.add_output('SmokeMaterial effects/yellowflare.vmt')
    entity.call_input('TurnOn')
    entity.set_parent(player.pointer, -1)
    tick_delays.delay(2, entity.call_input, 'TurnOff')
    tick_delays.delay(2.1, entity.call_input, 'Kill')
