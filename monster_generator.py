import random

from openai_client import chat_with_gpt
from storage import load_base_monster_attributes


async def generate_monster(current_map):
    base_monster_attributes = load_base_monster_attributes()[current_map['base_monster_attribute']]

    monster_name_gen_data = [
        f'[monster_name_gen]',
        f"map_name: {current_map['name']}",
        f"difficulty: {base_monster_attributes['difficulty']} / 10",
    ]
    monster_name = await chat_with_gpt('\n'.join(monster_name_gen_data))

    odd = random.uniform(0.8, 1.2)
    monster = {
        'name': monster_name,
        'attributes': {
            'health': {
                'current': round(base_monster_attributes['health'] * odd),
                'max': round(base_monster_attributes['health'] * odd)
            },
            'attack': round(base_monster_attributes['attack'] * odd),
            'defense': round(base_monster_attributes['defense'] * odd)
        },
        'experience': round(base_monster_attributes['experience'] * odd),
        'gold': round(base_monster_attributes['gold'] * odd)
    }

    return monster
