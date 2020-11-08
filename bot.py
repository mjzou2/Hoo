# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Lounge!'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'who' == message.content.lower() or 'who?' == message.content.lower():
        await message.channel.send('cares? no one')
    elif message.content == 'raise-exception':
        raise discord.DiscordException
    await bot.process_commands(message)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.command(name='test', help='test command')
async def t(ctx):
    response = "test command"
    await ctx.send(response)

bot.run(TOKEN)
