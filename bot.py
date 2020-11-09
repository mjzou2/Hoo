# bot.py
import os
import random
import discord
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(intents=intents, command_prefix="!")
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your mom"))
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        out = "Who joined? It\'s **" + member.display_name + "**!"
        await guild.system_channel.send(out)
    role = discord.utils.get(member.guild.roles, name="Guests")
    await member.add_roles(role)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await asyncio.sleep(0.5)

    if message.content == "WHO" or message.content == "WHO?":
        await message.channel.send("CARES? NO ONE")
    elif message.content.lower() == "who?" or message.content.lower() == "who":
        await message.channel.send("cares? no one")
    elif message.content.lower().endswith("ing") and not message.content.startswith("!") and not message.content.lower() == "fucking" and not " " in message.content:
        out = message.content[:-3]
        if (message.content[-3].isupper()):
            out += "O"
        else:
            out += "o"
        if (message.content[-2].isupper()):
            out += "N"
        else:
            out += "n"
        if (message.content[-1].isupper()):
            out += "G"
        else:
            out += "g"
        await message.channel.send(out)
    elif message.content.lower() == "aurora":
        out = "https://cdn.discordapp.com/attachments/610953429392818181/757659815559561467/unknown.png"
        await message.channel.send(out)
    elif message.content.lower() == "hoo":
        await message.channel.send("Who?")
    elif message.content.lower() == "hehe" or message.content.lower() == "heehee":
        await message.channel.send("hoohoo")
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("You do not have the permissions for this command.")
    if isinstance(error, commands.errors.MemberNotFound):
        await ctx.send("Member not found. Please @ the user for best accuracy.")

@bot.command(name="help", help="This help panel")
async def t(ctx):
    embed=discord.Embed(description="A dumb bot by Qwacker.", color=0x0096ff)
    embed.set_author(name="Hoo", url="https://github.com/mjzou2/Hoo", icon_url="https://cdn.discordapp.com/attachments/610953799120715776/774945651355942932/boticon.png")
    embed.add_field(name="!help", value="This help panel.", inline=False)
    embed.add_field(name="!roles", value="Displays the server\'s roles.", inline=False)
    embed.add_field(name="!tempmute -user -duration", value="Temporarily server mutes a user for the given duration in seconds. Requires moderator privileges.", inline=False)
    embed.add_field(name="!unmute -user", value="Unmutes a user.", inline=False)
    embed.add_field(name="!invite", value="Gives an invite link to the server.", inline=False)
    embed.add_field(name="!roll", value="Rolls a six-sided die.", inline=False)
    embed.add_field(name="!flip", value="Flips a coin.", inline=False)
    embed.add_field(name="!magic8ball -arg", value="Consult the magic 8-ball.", inline=False)
    embed.add_field(name="!choose -args", value="For when you wanna settle the score some other way.", inline=False)
    embed.add_field(name="!brag", value="Brag to the bot and he'll give you some support.", inline=False)
    embed.set_footer(text="I am an open source project. Check out my source code by clicking my name above.")
    await ctx.send(embed=embed)

@bot.command(name="roles", help="Displays the server\'s roles.")
async def roles(ctx):
    embed = discord.Embed(title="Roles", color=0x0096ff)
    embed.add_field(name="Staff", value="Server moderators. Have administrator privileges.", inline=False)
    embed.add_field(name="Bots", value="Bots. Help with the server.", inline=False)
    embed.add_field(name="Boosters", value="Discord Nitro boosters. Have a cool name color.", inline=False)
    embed.add_field(name="Members", value="Standard members. Have access to member-only channels.", inline=False)
    embed.add_field(name="Guests", value="Server guests. Have access to basic channels.", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="roll", help="Rolls a six-sided die")
async def roll(ctx):
    result = random.choice(range(1, 6))
    await ctx.send(result)

@bot.command(name="flip", help="Flips a coin")
async def flip(ctx):
    result = random.choice(range(1, 2))
    if (result == 1):
        out = "Heads"
    elif (result == 2):
        out = "Tails"
    await ctx.send(out)

@bot.command(name="magic8ball", help="Consult the magic 8-ball")
async def magic8ball(ctx):
    outcomes = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - Definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don\'t count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
    ]
    response = random.choice(outcomes)
    await ctx.send(response)

@bot.command(name="tempmute")
@commands.has_permissions(kick_members=True)
async def tempmute(ctx, member: discord.Member=None, duration: int=30):
    if not member:
        await ctx.send("Who do you want me to mute?")
        return
    await member.edit(mute=True)
    await ctx.send(member.display_name + " has been muted for " + str(duration) + " seconds.")
    await asyncio.sleep(duration)
    if (member.voice.mute):
        await member.edit(mute=False)
        await ctx.send(member.display_name + " is no longer muted.")

@bot.command(name="unmute")
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member=None):
    if not member:
        await ctx.send("Who do you want me to unmute?")
        return
    if (member.voice.mute):
        await member.edit(mute=False)
        await ctx.send(member.display_name + " is no longer muted.")
    else:
        await ctx.send(member.display_name + " is not currently muted.")
        return

@bot.command(name="invite")
async def invite(ctx):
    await ctx.send("https://discord.gg/3N64BDY")

@bot.command(name="choose")
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command(name="brag")
async def brag(ctx):
    openers = [
        "on god",
        "no cap",
        "deadass",
        "fo shizzle"
    ]
    middles = [
        " dats totes rad ",
        " dats cray cray ",
        " dats wack ",
        " dats da shit "
    ]
    closers = [
        "homie",
        "bro",
        "dude",
        "my nizzle"
    ]
    out = random.choice(openers) + random.choice(middles) + random.choice(closers)
    await ctx.send(out)

bot.run(TOKEN)
