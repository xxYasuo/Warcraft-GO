"""Debug heroes for WCGO testing."""

# Python 3
import random

# Source.Python
from messages import SayText2
from translations.strings import LangStrings

# Warcraft: GO
from wcgo.cooldown import cooldown, cooldownf
from wcgo.entities import Hero, Skill
from wcgo.info import info

# Globals
_debug_messages = LangStrings(info.basename + '/heroes/debug')


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
    _msg = SayText2(_debug_messages['Lifesteal'])

    def player_pre_attack(self, player, victim, info, **eargs):
        if player.team == victim.team:
            return
        chance = 20 + (5 * self.level)
        if random.randint(0, 100) <= chance:
            health = int(info.damage * 0.6)
            player.health += health
            self._msg.send(player.index, health=health)


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
    _msg = SayText2(_debug_messages['Burst_of_Speed'])
    _cd_msg = SayText2(_debug_messages['Burst_of_Speed:Cooldown'])

    def round_start(self, player, **eargs):
        self.player_ultimate.remaining_cooldown = 0

    @cooldown(10, message=_cd_msg)
    def player_ultimate(self, player, **eargs):
        speed = 0.1 * self.level * player.speed
        player.shift_property('speed', speed, 3)
        self._msg.send(player.index, speed=self.level * 10)


# =====================================================================
# >> Mahi's Debug Hero
# =====================================================================
class Mahi_Debug_Hero(Hero):
    "Mahi's hero for debugging Warcraft: GO."
    authors = 'Mahi',
    category = 'DEBUG'
    cost = 10


@Mahi_Debug_Hero.skill
class Burn_Until_Hit(Skill):
    "Burn your victims until you're hit."
    max_level = 1
    _msg_burn = SayText2(_debug_messages['Burn_Until_Hit:Burn'])
    _msg_hit = SayText2(_debug_messages['Burn_Until_Hit:Hit'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._burns = {}

    def player_attack(self, player, victim, **eargs):
        if player.team == victim.team:
            return
        if victim.userid not in self._burns:
            self._burns[victim.userid] = victim.burn()
            self._msg_burn.send(player.index, name=victim.name)

    def player_victim(self, player, **eargs):
        for burn in self._burns.values():
            try:
                burn.cancel()
            except ValueError:  # If the person has died or disconnected
                continue
        self._burns.clear()
        self._msg_hit.send(player.index)


@Mahi_Debug_Hero.skill
class Enrage(Skill):
    "Gain bonus damage when hit."
    max_level = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enrage = 0

    def player_spawn(self, **eargs):
        self._enrage = 0

    def player_victim(self, player, **eargs):
        self._enrage += 1

    def player_pre_attack(self, info, **eargs):
        info.damage += self._enrage * self.level


@Mahi_Debug_Hero.skill
class Movement_Speed_Stack(Skill):
    "Gain movement speed on attack, release on ultimate."
    max_level = 3
    _cd_msg = SayText2(_debug_messages['Movement_Speed_Stack:Cooldown'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stack = 0

    def player_spawn(self, **eargs):
        self._stack = 0

    def player_attack(self, player, **eargs):
        speed = 0.1 * self.level
        player.speed += speed
        self._stack += speed

    def round_start(self, player, **eargs):
        self.player_ultimate.remaining_cooldown = 0

    def _cooldownf(self, **eargs):
        return 2 + self._stack * 10

    @cooldownf(_cooldownf, message=_cd_msg)
    def player_ultimate(self, player, **eargs):
        player.speed -= self._stack
        self._stack = 0
