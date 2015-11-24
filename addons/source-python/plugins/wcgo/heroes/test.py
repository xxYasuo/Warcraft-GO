"""Hero test."""

# Warcraft: GO
import wcgo.entities


class Test_Hero(wcgo.entities.Hero):
    'Just a test hero.'
    max_level = 10
    restricted_items = tuple()


@Test_Hero.skill
class Speed(wcgo.entities.Skill):
    'Skill test which increases speed.'
    max_level = 2

    def player_spawn(self, player, **eargs):
        player.speed += self.level * 0.5