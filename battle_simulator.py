import math
import random

from openai_client import chat_with_gpt


def __initialize_battle_data(player, monster, current_map):
    return [
        f'[battle]',
        f"map_name: {current_map['name']}",
        f"player: {player['name']}",
        f"player_weapon: {player['equipment']['weapon']['name']}",
        f"enemy: {monster['name']}"
    ]


def __attack(attacker, defender, battle_data, is_attacker_player=False):
    base_attack = attacker['attributes']['attack']
    if is_attacker_player:
        base_attack += attacker['equipment']['weapon']['attack']
    damage = round(base_attack * random.uniform(0.8, 1.0))

    armor = defender['attributes']['defense']
    if not is_attacker_player:
        armor += defender['equipment']['armor']['defense']
    effective_damage = max(0, damage - armor)

    defender['attributes']['health']['current'] -= effective_damage
    if defender['attributes']['health']['current'] < 0:
        defender['attributes']['health']['current'] = 0

    battle_data.append(f"{attacker['name']} -> {defender['name']}: {effective_damage} dmg")

    return defender['attributes']['health']['current'] <= 0


def __reward_player(player, monster, battle_data):
    player['experience']['current'] += monster['experience']
    player['gold'] += monster['gold']
    battle_data.append(f"{player['name']} gained {monster['experience']} experience and {monster['gold']} gold")
    if player['experience']['current'] >= player['experience']['max']:
        __level_up(player, battle_data)


def __level_up(player, battle_data):
    player['level'] += 1
    player['experience']['current'] = 0
    player['experience']['max'] = int(player['experience']['max'] * (1 + 0.2 * math.log(player['level'] + 1)))
    player['attributes']['health']['max'] = int(
        player['attributes']['health']['max'] * (1 + 0.15 * math.log(player['level'] + 1)))
    player['attributes']['health']['current'] = player['attributes']['health']['max']
    player['attributes']['attack'] = int(player['attributes']['attack'] * (1 + 0.1 * math.log(player['level'] + 1)))
    battle_data.append(f"{player['name']} leveled up to level {player['level']}!")


async def simulate_battle(player, monster, current_map):
    battle_data = __initialize_battle_data(player, monster, current_map)
    player_health = player['attributes']['health']['current']
    monster_health = monster['attributes']['health']['current']

    while player_health > 0 and monster_health > 0:
        if __attack(player, monster, battle_data, is_attacker_player=True):
            battle_data.append(f"{monster['name']} defeated")
            __reward_player(player, monster, battle_data)
            break

        if __attack(monster, player, battle_data):
            battle_data.append(f"{player['name']} defeated")
            break

    return await chat_with_gpt('\n'.join(battle_data))
