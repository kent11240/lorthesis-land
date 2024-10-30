import discord

from commands import register_command
from commands.command import Command
from shop_owner import shop_owner_talk
from storage import load_player, load_map, load_shop


class ShopCommand(Command):
    def description(self) -> str:
        return '查看當前城鎮商店的商品。'

    async def execute(self, message: discord.Message):
        user_id = str(message.author.id)

        player = load_player(user_id)
        if not player:
            await message.channel.send(f'<@{user_id}>\n冒險從角色開始！快去創個角色吧，不然我該怎麼稱呼你呢？')
            return

        current_map = load_map(**player['coordinate'])
        if not current_map or current_map.get('type') != 'town':
            await message.channel.send(f'<@{user_id}>\n這裡荒郊野外，連個小販的影子都沒有呢！還是回城再看看吧。')
            return

        shop_items = load_shop()[current_map['shop']]
        if not shop_items:
            await message.channel.send(f'<@{user_id}>\n老闆出門旅遊了，店裡空空如也！等他回來再來看看吧！')
            return

        shop_owner_message = await shop_owner_talk(current_map, shop_items)
        shop_message = f"{current_map['name']}商店老闆：{shop_owner_message}\n"
        for index, item in enumerate(shop_items, start=1):
            shop_message += f"{index}. {item['name']} - {item['description']} (價格: {item['price']} 金幣)\n"

        await message.channel.send(f'<@{user_id}>\n{shop_message}')


register_command('!shop', ShopCommand)
