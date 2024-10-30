from openai_client import chat_with_gpt


async def describe_map(from_map, to_map):
    map_description_data = [
        f'[map_description]',
        f"from_map: {from_map['name']}",
        f"to_map: {to_map['name']}"
    ]

    return await chat_with_gpt('\n'.join(map_description_data))


async def describe_reincarnation(player, current_map):
    born_message_data = [
        f'[reincarnation_description]',
        f"player_name: {player['name']}",
        f"map_name: {current_map['name']}"
    ]

    return await chat_with_gpt('\n'.join(born_message_data))
