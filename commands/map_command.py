import discord

from commands import register_command
from commands.command import Command
from storage import load_player, load_map


class MapCommand(Command):
    def description(self) -> str:
        return '列出玩家當前地點可以前往的地圖。'

    async def execute(self, message: discord.Message):
        user_id = str(message.author.id)

        player = load_player(user_id)
        if not player:
            await message.channel.send(f'<@{user_id}>\n冒險從角色開始！快去創個角色吧，不然我該怎麼稱呼你呢？')
            return

        directions = {
            '北方': (player['coordinate']['x'], player['coordinate']['y'] + 1, player['coordinate']['z']),
            '南方': (player['coordinate']['x'], player['coordinate']['y'] - 1, player['coordinate']['z']),
            '東方': (player['coordinate']['x'] + 1, player['coordinate']['y'], player['coordinate']['z']),
            '西方': (player['coordinate']['x'] - 1, player['coordinate']['y'], player['coordinate']['z']),
        }

        available_maps = []
        for direction, coords in directions.items():
            map_entry = load_map(*coords)
            if map_entry:
                available_maps.append(f"{direction}：{map_entry['name']}")

        if not available_maps:
            await message.channel.send(f'<@{user_id}>\n這裡一片空白，暫時沒有可探索的地圖。')
            return

        map_list = '\n'.join(available_maps)
        await message.channel.send(f'<@{user_id}>\n你可以前往以下地點：\n{map_list}')


register_command('!map', MapCommand)
