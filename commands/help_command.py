import discord

from commands import commands_registry, register_command
from commands.command import Command


class HelpCommand(Command):
    def description(self) -> str:
        return '顯示所有可用的指令及其描述。'

    async def execute(self, message: discord.Message):
        user_id = str(message.author.id)

        help_message = '可用指令：\n'
        for command_prefix, command in commands_registry.items():
            help_message += f'{command_prefix}：{command().description()}\n'
        await message.channel.send(f'<@{user_id}>\n{help_message}')


register_command('!help', HelpCommand)
