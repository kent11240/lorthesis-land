from items import register_item
from items.item import Item


class Armor(Item):
    def __init__(self, type: str, name: str, description: str, price: int, defense: int):
        super().__init__(type, name, description, price)
        self.defense = defense

    def use(self, player):
        player['backpack'].append(player['equipment']['armor'])
        player['equipment']['armor'] = {
            'type': 'armor',
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'defense': self.defense
        }


register_item('armor', Armor)
