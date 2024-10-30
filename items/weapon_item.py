from items import register_item
from items.item import Item


class Weapon(Item):
    def __init__(self, type: str, name: str, description: str, price: int, attack: int):
        super().__init__(type, name, description, price)
        self.attack = attack

    def use(self, player):
        player['backpack'].append(player['equipment']['weapon'])
        player['equipment']['weapon'] = {
            'type': 'weapon',
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'attack': self.attack
        }


register_item('weapon', Weapon)
