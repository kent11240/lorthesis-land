import discord

from commands import register_command
from commands.command import Command
from storage import load_player


class BagCommand(Command):
    def description(self) -> str:
        return '查看包包內的所有物品。'

    async def execute(self, message: discord.Message):
        user_id = str(message.author.id)

        player = load_player(user_id)
        if not player:
            await message.channel.send(f'<@{user_id}>\n冒險從角色開始！快去創個角色吧，不然我該怎麼稱呼你呢？')
            return

        if not player or not player.get('backpack'):
            await message.channel.send(f'<@{user_id}>\n包包裡連根羽毛都沒有，是時候去冒險收集些東西了！')
            return

        backpack_contents = '\n'.join(
            [f"{index}. {item['name']} - {item['description']}" for index, item in enumerate(player['backpack'])])
        await message.channel.send(f'<@{user_id}>\n你的包包內有以下物品：\n{backpack_contents}')


register_command('!bag', BagCommand)
