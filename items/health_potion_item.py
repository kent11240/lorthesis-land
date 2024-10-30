from items import register_item
from items.item import Item


class HealthPotion(Item):
    def __init__(self, type: str, name: str, description: str, price: int, heal_amount: int):
        super().__init__(type, name, description, price)
        self.heal_amount = heal_amount

    def use(self, player):
        player['attributes']['health']['current'] = min(
            player['attributes']['health']['max'],
            player['attributes']['health']['current'] + self.heal_amount
        )


register_item('health_potion', HealthPotion)
