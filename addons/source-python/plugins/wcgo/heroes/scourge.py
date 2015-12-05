"""Default hero from wcgo core."""

# Python3
from random import randint

# Source.Python
from effects import temp_entities
from engines.trace import engine_trace
from engines.trace import ContentMasks
from engines.trace import GameTrace
from engines.trace import MAX_TRACE_LENGTH
from engines.trace import Ray
from engines.trace import TraceFilterSimple
from filters.recipients import RecipientFilter
from filters.players import PlayerIter
from listeners.tick import tick_delays
from mathlib import Vector

# Warcraft: GO
from wcgo import strings
from wcgo.effects import models
from wcgo.entities import Hero, Skill
from wcgo.player import Player

# Hero class

class Undead_Scourge(Hero):
    'Redesigned Warcraft Scourge.'

    max_level = 40
    category = 'DEFAULT'


@Undead_Scourge.passive
class Undead_Rage(Skill):
    'Obtain increased speed due to your auras.'

    def player_spawn(self, player, **eargs):
        player.speed = 1.18

@Undead_Scourge.skill
class Vampirism(Skill):
    'You have an aura which causes you to steal life. Max HP (100+15*LEVEL)'

    max_level = 8

    @property
    def _max(self):
        return 100 + 15*self.level

    @property
    def _percent(self):
        return 0.1 + 0.05*self.level

    @property
    def _chance(self):
        return 30 + 5*self.level

    def player_pre_attack(self, attacker, victim, info, weapon, **eargs):
        if randint(1, 100) <= self._chance:
            damage = info.damage
            life = int(damage*self._percent)
            if attacker.health+life > self._max:
                attacker.health = self._max
            else:
                attacker.health += life

@Undead_Scourge.skill
class Unholy_Aura(Skill):
    'Release an aura which increases allied speed.'

    max_level = 8

    model = models['sprites/laser.vmt']

    @property
    def _recipients(self):
        return RecipientFilter()

    @property
    def _speed(self):
        return 0.02*self.level

    def player_spawn(self, player, **eargs):
        if not player.playerinfo.is_fake_client():
            team = ['t', 'ct'][player.team-2]
            temp_entities.beam_ring_point(self._recipients, 0, player.origin,
                20, 800, self.model.index, self.model.index, 0, 255, 2, 8, 1, 1,
                255, 100, 100, 255, 1, 0)
            for ally in PlayerIter(is_filters=team):
                if not ally.userid == player.userid:
                    ally.speed += self._speed
                    temp_entities.beam_ring_point(self._recipients, 2, ally.origin,
                        200, 20, self.model.index, self.model.index, 0, 255, 0.3, 8, 1,
                        1, 100, 100, 255, 255, 1, 0)
            player.speed += self._speed

@Undead_Scourge.skill
class Levitation(Skill):
    'Reduce your current gravity and damage taken when jumping.'

    max_level = 8

    @property
    def _gravity(self):
        return 1 - 0.08*self.level

    @property
    def _reduction(self):
        return 1 - 0.06*self.level

    def _get_trace(self, start, end, mask, index, trace):
        engine_trace.trace_ray(Ray(start, end),
            ContentMasks.ALL, TraceFilterSimple((index, )), trace)
        return trace

    def player_spawn(self, player, **eargs):
        player.gravity = self._gravity

    def player_pre_victim(self, attacker, victim, info, **eargs):
        start = victim.eye_location
        end = victim.eye_location
        end.z -= MAX_TRACE_LENGTH
        trace = self._get_trace(start, end, ContentMasks.ALL, victim.index,
            GameTrace())
        if trace.did_hit():
            floor = trace.end_position
            if start.get_distance(floor) > 100:
                info.damage *= self._reduction
                strings.message(victim.index,
                    'Levitation',
                    reduced=100-self._reduction*100,
                    damage=info.damage)

@Undead_Scourge.skill
class Suicide_Bomber(Skill):
    'Explode upon death or on ultimate causing enemies to bleed.'

    max_level = 8

    _index = None

    @property
    def _range(self):
        return 300 + 50*self.level

    @property
    def _magnitude(self):
        return 50 + 5*self.level

    @property
    def _recipients(self):
        return RecipientFilter()

    def player_spawn(self, player, **eargs):
        self._index = None

    def player_pre_victim(self, victim, **eargs):
        if not self._index:
            for index in victim.weapon_indexes():
                self._index = index
                break

    def player_death(self, victim, **eargs):
        players_hit = []
        team = ['ct', 't'][victim.team-2]

        for target in PlayerIter(is_filters=team):
            if victim.origin.get_distance(target.origin) <= self._range:
                target.take_damage(self._magnitude,
                    attacker_index=victim.index, weapon_index=self._index)
                players_hit.append(target.name)

        if len(players_hit) > 0:
            strings.message(victim.index, 'Suicide Bomber', names=', '.join(players_hit))

        temp_entities.explosion(self._recipients, 0.0, victim.origin, 0,
            1.0, 255, 0, 600, 2, Vector(), 67)

    def player_ultimate(self, player, **eargs):
        if not player.isdead:
            players_hit = []
            team = ['ct', 't'][player.team-2]

            for index in player.weapon_indexes():
                break
            else:
                index = None

            for target in PlayerIter(is_filters=team):
                if player.origin.get_distance(target.origin) <= self._range:
                    target.take_damage(self._magnitude,
                        attacker_index=player.index, weapon_index=index)
                    players_hit.append(target.name)

            if len(players_hit) > 0:
                strings.message(victim.index, 'Suicide Bomber', names=', '.join(players_hit))
            
            player.client_command('kill', True)

            temp_entities.explosion(self._recipients, 0.0, player.origin, 0,
                1.0, 255, 0, 600, 2, Vector(), 67)