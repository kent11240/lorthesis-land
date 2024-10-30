import discord

from commands import register_command
from commands.command import Command
from storage import load_player, save_player, load_map, load_shop


class BuyCommand(Command):
    def description(self) -> str:
        return '購買商店內的商品。用法：`!buy <商品索引>`'

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

        try:
            item_index = int(message.content[len('!buy '):].strip()) - 1
        except ValueError:
            await message.channel.send(f'<@{user_id}>\n商店小精靈不認識這種奇怪的符號，再試一次吧！')
            return

        if item_index < 0 or item_index >= len(shop_items):
            await message.channel.send(f'<@{user_id}>\n你似乎瞄準了傳說中的隱藏商品…但可惜商店裡沒有呢。')
            return

        item = shop_items[item_index]
        item_price = item['price']

        if player['gold'] < item_price:
            await message.channel.send(f'<@{user_id}>\n嗯？你的錢袋有點輕喔，還差一些金幣才能買到這個。')
            return

        player['gold'] -= item_price
        player['backpack'].append(item)
        save_player(user_id, player)

        await message.channel.send(f"<@{user_id}>\n你已成功購買 **{item['name']}**，快看看你的包包吧！")


register_command('!buy', BuyCommand)
