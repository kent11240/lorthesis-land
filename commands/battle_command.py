import discord

from battle_simulator import simulate_battle
from commands import register_command
from commands.command import Command
from monster_generator import generate_monster
from storage import load_player, save_player, load_map


class BattleCommand(Command):
    def description(self) -> str:
        return '開始一場戰鬥。'

    async def execute(self, message: discord.Message):
        user_id = str(message.author.id)

        player = load_player(user_id)
        if not player:
            await message.channel.send(f'<@{user_id}>\n冒險從角色開始！快去創個角色吧，不然我該怎麼稱呼你呢？')
            return

        if player['attributes']['health']['current'] <= 0:
            await message.channel.send(f'<@{user_id}>\n欸欸欸！你這樣打下去根本是找虐，先回血再說吧！')
            return

        current_map = load_map(**player['coordinate'])
        if current_map and current_map.get('type') == 'town':
            await message.channel.send(f'<@{user_id}>\n嘿，這裡可是城鎮！難道你想揮劍對抗…賣蔬菜的大嬸？還是省省力氣吧！')
            return

        monster = await generate_monster(current_map)
        battle = await simulate_battle(player, monster, current_map)

        save_player(user_id, player)
        await message.channel.send(f'<@{user_id}>\n{battle}')


register_command('!battle', BattleCommand)
