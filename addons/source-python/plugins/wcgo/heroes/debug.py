
"""Debug hero for wcgo testing."""

# Python 3
import random

# Source.Python
from messages import SayText2

# Warcraft: GO
from wcgo.cooldown import cooldown, cooldownf
from wcgo.entities import Hero, Skill


# =====================================================================
# >> Predz's Debug Hero
# =====================================================================
class Predz_Debug_Hero(Hero):
    "Predz's hero for debugging Warcraft: GO."
    authors = 'Predz',
    category = 'DEBUG'
    cost = 0
    max_level = 10


@Predz_Debug_Hero.passive
class Health_Increase(Skill):
    "Gain a health increase upon spawning."

    def player_spawn(self, player, **eargs):
        player.health += 40


@Predz_Debug_Hero.skill
class Lifesteal(Skill):
    "Retrieve 60% of damage back as health, on chance."
    max_level = 8
    _msg = '>> \x04Lifesteal: \x02Stole {health} health from enemy'

    def player_pre_attack(self, player, info, **eargs):
        chance = 20 + (5 * self.level)
        if random.randint(0, 100) <= chance:
            health = int(info.damage * 0.6)
            player.health += health
            SayText2(self._msg.format(health=health)).send(player.index)


@Predz_Debug_Hero.skill
class Longjump(Skill):
    "Jump much further than normal."
    max_level = 8

    @cooldown(3)
    def player_jump(self, player, **eargs):
        horizontal_mul = 200 + 10 * self.level
        player.push(horizontal_mul, 1, 150)


@Predz_Debug_Hero.skill
class Burst_of_Speed(Skill):
    "On ultimate you gain massive speed."
    max_level = 8
    _msg = '>> \x04Burst of Speed: \x03You gained {speed}% more speed.'

    @cooldown(10)
    def player_ultimate(self, player, **eargs):
        speed = 0.1 * self.level * player.speed
        player.shift_property('speed', speed, 3)
        SayText2(self._msg.format(speed=self.level * 10)).send(player.index)
