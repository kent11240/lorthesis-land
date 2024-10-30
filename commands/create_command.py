import re

import discord

from commands import register_command
from commands.command import Command
from map_describer import describe_reincarnation
from storage import load_player, save_player, load_map


class CreateCommand(Command):
    def description(self) -> str:
        return '創建一個新玩家。用法：`!create <玩家名稱>`'

    async def execute(self, message: discord.Message):
        user_id = str(message.author.id)

        player_name = message.content[len('!create '):].strip()
        if not player_name:
            await message.channel.send(
                f'<@{user_id}>\n呃...你該不會想當無名氏吧？快給自己取個名字！\n用法：`!create 玩家名稱`')
            return

        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9]+$', player_name):
            await message.channel.send(
                f'<@{user_id}>\n這名字有點超凡脫俗！不過中文、英文和數字才是我們的範圍喔！')
            return

        player = load_player(user_id)
        if player:
            await message.channel.send(f'<@{user_id}>\n嘿，勇士！你已經閃亮登場了，不用再刷存在感了！')
            return

        player = {
            'id': user_id,
            'name': player_name,
            'level': 1,
            'experience': {
                'current': 0,
                'max': 100
            },
            'attributes': {
                'health': {
                    'current': 100,
                    'max': 100
                },
                'attack': 10,
                'defense': 0
            },
            'gold': 0,
            'backpack': [],
            'equipment': {
                'weapon': {
                    'name': '空手',
                    'type': 'weapon',
                    'description': '不靠武器，全憑膽識！不過…小心手疼。',
                    'price': 0,
                    'attack': 0
                },
                'armor': {
                    'name': '布衣',
                    'type': 'armor',
                    'description': '新手冒險者的標配，1 點防禦力，讓你感受到微風的保護！',
                    'price': 5,
                    'defense': 1
                }
            },
            'coordinate': {
                'x': -1,
                'y': 1,
                'z': 0
            }
        }

        save_player(user_id, player)

        reincarnation_message = await describe_reincarnation(player, load_map(**player['coordinate']))
        await message.channel.send(f'<@{user_id}>\n{reincarnation_message}')


register_command('!create', CreateCommand)
