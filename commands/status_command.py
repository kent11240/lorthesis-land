import discord

from commands import register_command
from commands.command import Command
from storage import load_player, load_map


class StatusCommand(Command):
    def description(self) -> str:
        return '顯示玩家的當前狀態。'

    async def execute(self, message: discord.Message):
        user_id = str(message.author.id)

        player = load_player(user_id)
        if not player:
            await message.channel.send(f'<@{user_id}>\n冒險從角色開始！快去創個角色吧，不然我該怎麼稱呼你呢？')
            return

        status_message = (
            f"玩家名稱：{player['name']}\n"
            f"等級：{player['level']}\n"
            f"經驗值：{player['experience']['current']} / {player['experience']['max']}\n"
            f"生命值：{player['attributes']['health']['current']} / {player['attributes']['health']['max']}\n"
            f"攻擊力：{player['attributes']['attack']}\n"
            f"防禦力：{player['attributes']['defense']}\n"
            f"武器：{player['equipment']['weapon']['name']}（武器攻擊力：{player['equipment']['weapon']['attack']}）\n"
            f"防具：{player['equipment']['armor']['name']}（防具防禦力：{player['equipment']['armor']['defense']}）\n"
            f"金幣：{player['gold']}\n"
            f"位置：{load_map(**player['coordinate'])['name']}"
        )

        await message.channel.send(f'<@{user_id}>\n{status_message}')


register_command('!status', StatusCommand)
