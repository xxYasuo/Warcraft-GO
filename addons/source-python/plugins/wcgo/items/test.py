"""Item test."""

# Warcraft: GO
import wcgo.entities


class Test_Item(wcgo.entities.Item):
    'Just a test item.'

    cost = 300
    limit = 1

    def item_purchased(self, player, **eargs):
        player.speed += 0.5