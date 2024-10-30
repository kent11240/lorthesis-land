import discord

from commands import register_command
from commands.command import Command
from map_describer import describe_map
from storage import load_player, save_player, load_map


class MoveCommand(Command):
    def description(self) -> str:
        return '將玩家移動到指定方向。用法：`!move <方向>`，方向可以是北方 `n`、南方 `s`、東方 `e`或西方 `w`。'

    async def execute(self, message: discord.Message):
        user_id = str(message.author.id)

        player = load_player(user_id)
        if not player:
            await message.channel.send(f'<@{user_id}>\n冒險從角色開始！快去創個角色吧，不然我該怎麼稱呼你呢？')
            return

        direction = message.content[len('!move '):].strip()
        if direction not in ['n', 's', 'e', 'w']:
            await message.channel.send(
                f'<@{user_id}>\n你的路只有四個選擇：北方`n`、南方`s`、東方`e`、西方`w`！其他方向？嗯…還沒解鎖呢！')
            return

        current_coords = player['coordinate']
        from_map = load_map(**current_coords)
        new_coords = {
            'n': (current_coords['x'], current_coords['y'] + 1, current_coords['z']),
            's': (current_coords['x'], current_coords['y'] - 1, current_coords['z']),
            'e': (current_coords['x'] + 1, current_coords['y'], current_coords['z']),
            'w': (current_coords['x'] - 1, current_coords['y'], current_coords['z']),
        }[direction]

        to_map = load_map(*new_coords)
        if not to_map:
            await message.channel.send(f'<@{user_id}>\n你凝視遠方，卻只看到一片空白…也許換個方向會有收穫。')
            return

        player['coordinate'] = {
            'x': new_coords[0],
            'y': new_coords[1],
            'z': new_coords[2]
        }
        save_player(user_id, player)

        map_description = await describe_map(from_map, to_map)
        await message.channel.send(f'<@{user_id}>\n{map_description}')


register_command('!move', MoveCommand)
