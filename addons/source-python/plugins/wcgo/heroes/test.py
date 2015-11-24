"""Hero test."""

# Warcraft: GO
import wcgo.entities

class Test(wcgo.entities.Hero):
    name = 'Test Hero'
    description = 'Hero test for menus.'
    max_level = 10

    restricted_items = tuple()

    _register = True

@Test.skill
class Speed(wcgo.entities.Skill):
    name = 'Test Speed'
    description = 'Skill test which increases speed.'
    max_level = 2

    def player_spawn(self, player, **eargs):
        player.speed += 0.5