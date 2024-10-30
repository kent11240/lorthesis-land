import importlib
import os

item_registry = {}


def register_item(item_type, item_class):
    item_registry[item_type] = item_class


def load_items():
    item_files = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('_item.py')]
    for item_file in item_files:
        importlib.import_module(f'items.{item_file}')


def create_item(item):
    item_type = item['type']
    item_class = item_registry.get(item_type)
    if not item_class:
        raise ValueError(f'Unknown item type: {item_type}')
    return item_class(**item)
