import asyncio
import os

import discord

from commands import commands_registry

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

player_locks = {}


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print('Registered commands:', ', '.join(commands_registry.keys()))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.channel.name == os.getenv('CHANNEL_NAME'):
        return

    user_id = str(message.author.id)
    if user_id not in player_locks:
        player_locks[user_id] = asyncio.Lock()

    if player_locks[user_id].locked():
        await message.channel.send(f'<@{user_id}>\n嘿，別貪心！你還在忙上一次的任務，等一下再說吧！')
        return

    async with player_locks[user_id]:
        for command_prefix, command in commands_registry.items():
            if message.content.startswith(command_prefix):
                print(f'{message.author.display_name} execute command: {command_prefix}')
                await command().execute(message)
                break


def run_discord_bot():
    client.run(os.getenv('DISCORD_TOKEN'))
