"""Module for supplying a level up effect."""

# Source.Python
from listeners.tick import tick_delays

# Warcraft: GO
from wcgo.effects import models
from wcgo.effects.entity import Entity

# Globals
_tick_model = models['effects/yellowflare.vmt']


def level_up(player):
    """Display the level up effect on a player."""
    entity = Entity.create('env_smokestack')
    entity.teleport(player.origin, None, None)
    entity.add_output_safe('basespread 10')
    entity.add_output_safe('spreadspeed 60')
    entity.add_output_safe('initial 0')
    entity.add_output_safe('speed 105')
    entity.add_output_safe('rate 50')
    entity.add_output_safe('startsize 7')
    entity.add_output_safe('endsize 2')
    entity.add_output_safe('twist 0')
    entity.add_output_safe('jetlength 100')
    entity.add_output_safe('angles 0 0 0')
    entity.add_output_safe('rendermode 18')
    entity.add_output_safe('renderamt 100')
    entity.add_output_safe('rendercolor 255 255 3')
    entity.add_output_safe('SmokeMaterial effects/yellowflare.vmt')
    entity.call_input_safe('TurnOn')
    entity.set_parent(player.pointer, -1)
    tick_delays.delay(2, entity.call_input_safe, 'TurnOff')
    tick_delays.delay(2.1, entity.call_input_safe, 'Kill')
