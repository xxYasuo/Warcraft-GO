"""Debug hero for wcgo testing."""

# Python3
from random import randint

# Source.Python
from messages import SayText2
from listeners.tick import tick_delays

# Warcraft: GO
from wcgo.cooldown import cooldown
from wcgo.configs import message_template
from wcgo.entities import Hero
from wcgo.entities import Skill

# Message function
def message(index, message, template=message_template):
    instance = SayText2(template.format(message))
    instance.send(index)

# Create hero
class Debug_Hero(Hero):
    'Hero for debugging Warcraft: GO.'

    authors = 'Predz', 'Mahi'
    category = 'DEBUG'
    cost = 0
    max_level = 10

# Create passive
@Debug_Hero.passive
class Health_Increase(Skill):
    'Gain a health increase upon spawning.'

    def player_spawn(self, player, **eargs):
        player.health += 40

# Create chance skill
@Debug_Hero.skill
class Lifesteal(Skill):
    'Retrieve 60% of damage back as health, on chance.'

    max_level = 8

    def player_pre_attack(self, player, info, **eargs):
        chance = 20 + (5 * self.level)
        if randint(0, 100) <= chance:
            health = int(info.damage * 0.6)
            player.health += health
            message(player.index,
                '\x02Stole {health} health from enemy'.format(health=health))

# Create cooldown skill
@Debug_Hero.skill
class Longjump(Skill):
    'Jump much further than normal.'

    max_level = 8

    @cooldown(3)
    def player_jump(self, player, **eargs):
        player.push(200 + (10 * self.level), 1, 150)

# Create ultimate skill
@Debug_Hero.skill
class Burst_of_Speed(Skill):
    'On ultimate you gain massive speed.'

    max_level = 8

    @cooldown(10)
    def player_ultimate(self, player, **eargs):
        speed = (0.1 * self.level) * player.speed
        player.shift_property('speed', speed, 3)
        message(player.index,
                '\x03You gained {speed}% more speed.'.format(speed=self.level*10))
