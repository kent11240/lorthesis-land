from openai_client import chat_with_gpt


async def shop_owner_talk(current_map, shop_items):
    shop_items_data = [
        f"{item['name']} - {item['description']} (價格: {item['price']} 金幣)"
        for item in shop_items
    ]

    shop_owner_talk_data = [
        f'[shop_owner_talk]',
        f"map_name: {current_map['name']}",
        f'shop_items:',
        *shop_items_data
    ]

    return await chat_with_gpt('\n'.join(shop_owner_talk_data))
