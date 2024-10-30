class Item:
    def __init__(self, item_type: str, name: str, description: str, price: int):
        self.type = item_type
        self.name = name
        self.description = description
        self.price = price

    def use(self, player):
        raise NotImplementedError('This method should be overridden by subclasses')
