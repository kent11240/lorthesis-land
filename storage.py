import json
import os

PLAYER_DIR = 'data/players'
MAPS_FILE = 'data/maps.json'
BASE_MONSTER_ATTRIBUTES_FILE = 'data/base_monster_attributes.json'
SHOP_FILE = 'data/shops.json'


def load_player(user_id):
    player_file = os.path.join(PLAYER_DIR, f'{user_id}.json')
    if os.path.exists(player_file):
        with open(player_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None


def save_player(user_id, player):
    os.makedirs(PLAYER_DIR, exist_ok=True)
    player_file = os.path.join(PLAYER_DIR, f'{user_id}.json')
    with open(player_file, 'w', encoding='utf-8') as file:
        json.dump(player, file, indent=4, ensure_ascii=False)


def load_map(x, y, z):
    if os.path.exists(MAPS_FILE):
        with open(MAPS_FILE, 'r', encoding='utf-8') as file:
            maps = json.load(file)

    for map_entry in maps:
        if (map_entry['coordinate']['x'] == x and
                map_entry['coordinate']['y'] == y and
                map_entry['coordinate']['z'] == z):
            return map_entry
    return None


def load_base_monster_attributes():
    if os.path.exists(BASE_MONSTER_ATTRIBUTES_FILE):
        with open(BASE_MONSTER_ATTRIBUTES_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}


def load_shop():
    if os.path.exists(SHOP_FILE):
        with open(SHOP_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}
