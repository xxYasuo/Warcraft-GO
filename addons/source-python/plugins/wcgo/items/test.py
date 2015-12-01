"""Item test."""

# Warcraft: GO
import wcgo.entities


class Test_Item(wcgo.entities.Item):

    cost = 300
    limit = 1

    def item_purchased(self, player, **eargs):
        player.speed += 0.5

    def item_sold(self, player, **eargs):
        player.speed -= 0.5

    def player_spawn(self, player, **eargs):
        player.speed += 0.5