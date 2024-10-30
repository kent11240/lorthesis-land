import discord

from commands import register_command
from commands.command import Command
from items import create_item
from storage import load_player, save_player


class UseCommand(Command):
    def description(self) -> str:
        return '使用包包內的道具。用法：`!use <道具索引>`'

    async def execute(self, message: discord.Message):
        user_id = str(message.author.id)

        player = load_player(user_id)
        if not player:
            await message.channel.send(f'<@{user_id}>\n冒險從角色開始！快去創個角色吧，不然我該怎麼稱呼你呢？')
            return

        try:
            item_index = int(message.content[len('!use '):].strip()) - 1
        except ValueError:
            await message.channel.send(f'<@{user_id}>\n想要用道具？得輸入數字才行，其他東西可不行喔！')
            return

        if item_index < 0 or item_index >= len(player['backpack']):
            await message.channel.send(f'<@{user_id}>\n抱歉，你的包包裡沒有這麼多道具，可能需要去撿點新的。')
            return

        item = player['backpack'][item_index]
        try:
            create_item(item).use(player)
        except ValueError as e:
            await message.channel.send(f'<@{user_id}>\n{str(e)}')
            return

        player['backpack'].pop(item_index)
        save_player(user_id, player)
        await message.channel.send(f'<@{user_id}>\n你已成功使用 **{item["name"]}**，快看看你的狀態吧！')


register_command('!use', UseCommand)
