# bot.py
import os
import random
import discord
import asyncio
import json

from collections import Counter

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(intents=intents, command_prefix="!")
bot.remove_command("help")

amounts = {}

@bot.event
async def on_ready():
    global amounts
    try:
        with open("amounts.json") as f:
            amounts = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        amounts = {}
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
async def help(ctx, page: int=1):
    embed=discord.Embed(description="A dumb bot by Qwacker.", color=0x0096ff)
    embed.set_author(name="Hoo", url="https://github.com/mjzou2/Hoo", icon_url="https://cdn.discordapp.com/attachments/610953799120715776/774945651355942932/boticon.png")
    if (page == 1 or page > 3 or page < 1):
        page = 1
        embed.add_field(name="!help -page", value="This help panel.", inline=False)
        embed.add_field(name="!roles", value="Displays the server\'s roles.", inline=False)
        embed.add_field(name="!tempmute -person -duration", value="Temporarily server mutes a person for the given duration in seconds. Requires moderator privileges.", inline=False)
        embed.add_field(name="!unmute -person", value="Unmutes a person.", inline=False)
        embed.add_field(name="!invite", value="Gives an invite link to the server.", inline=False)
    elif (page == 2):
        embed.add_field(name="!register", value="Register an account for the server currency system.", inline=False)
        embed.add_field(name="!balance", value="View your current balance of server currency.", inline=False)
        embed.add_field(name="!balanceof -person", value="View the person's current balance of server currecy.", inline=False)
        embed.add_field(name="!transfer -amount -person", value="Transfer the amount of currency to the given person from your own balance.", inline=False)
        embed.add_field(name="!give -amount -person", value="Gives the person the amount of currency. Requires administrator privileges.", inline=False)
        embed.add_field(name="!reset", value="Resets your currency balance to $100.", inline=False)
        embed.add_field(name="!roll -amount -outcome", value="Rolls a six-sided die. Bet currency on the result.", inline=False)
        embed.add_field(name="!flip -amount -outcome", value="Flips a coin. Bet currency on the result.", inline=False)
        embed.add_field(name="!leaderboard", value="Shows the people with the most currency.", inline=False)
        embed.add_field(name="!save", value="Saves the current database of server currency to Qwacker's hard drive.", inline=False)
    elif (page == 3):
        embed.add_field(name="!magic8ball -arg", value="Consult the magic 8-ball.", inline=False)
        embed.add_field(name="!choose -args", value="For when you wanna settle the score some other way.", inline=False)
        embed.add_field(name="!brag", value="Brag to the bot and he'll give you some support.", inline=False)
    embed.set_footer(text="Page " + str(page) + " out of 3")
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
async def roll(ctx, amount: int, outcome: str):
    user_id = str(ctx.message.author.id)
    if user_id not in amounts:
        await ctx.send("You do not have an account.")
        return
    elif amounts[user_id] < amount:
        await ctx.send("You cannot afford this bet.")
        return
    if (outcome.lower() == "one" or outcome == "1"):
        choice = 1
    elif (outcome.lower() == "two" or outcome == "2"):
        choice = 2
    elif (outcome.lower() == "three" or outcome == "3"):
        choice = 3
    elif (outcome.lower() == "four" or outcome == "4"):
        choice = 4
    elif (outcome.lower() == "five" or outcome == "5"):
        choice = 5
    elif (outcome.lower() == "six" or outcome == "6"):
        choice = 6
    else:
        await ctx.send("Outcome not recognized. Please try again.")
        return
    result = random.choice([1, 2, 3, 4, 5, 6])
    if (choice == result):
        await ctx.send("The die rolled a " + str(result) + ". You won $" + str(6 * amount) + "!")
        amounts[user_id] += 6 * amount
    else:
        await ctx.send("The die rolled a " + str(result) + ". You lost $" + str(amount) + "!")
        amounts[user_id] -= amount
    _save()

@bot.command(name="flip", help="Flips a coin")
async def flip(ctx, amount: int, outcome: str):
    user_id = str(ctx.message.author.id)
    if user_id not in amounts:
        await ctx.send("You do not have an account.")
        return
    elif amounts[user_id] < amount:
        await ctx.send("You cannot afford this bet.")
        return
    if (outcome.lower() == "heads" or outcome.lower() == "h" or outcome.lower() == "head"):
        choice = "Heads"
    elif (outcome.lower() == "tails" or outcome.lower() == "t" or outcome.lower() == "tail"):
        choice = "Tails"
    else:
        await ctx.send("Outcome not recognized. Please try again.")
        return
    result = random.choice([1, 2])
    if (result == 1):
        out = "Heads"
    elif (result == 2):
        out = "Tails"
    if (choice == out):
        await ctx.send("The coin came up " + out + ". You won $" + str(amount) + "!")
        amounts[user_id] += amount
    else:
        await ctx.send("The coin came up " + out + ". You lost $" + str(amount) + "!")
        amounts[user_id] -= amount
    _save()

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

@bot.command(name="balance", pass_context=True)
async def balance(ctx):
    id = str(ctx.message.author.id)
    if id in amounts:
        await ctx.send("You have ${}.".format(amounts[id]))
    else:
        await ctx.send("You do not have an account.")

@bot.command(name="balanceof", pass_context=True)
async def balanceof(ctx, user: discord.Member):
    user_id = str(user.id)
    if user_id in amounts:
        await ctx.send(user.display_name + " has $" + str(amounts[user_id]) + ".")
    else:
        await ctx.send(user.display_name + " does not have an account.")

@bot.command(name="register", pass_context=True)
async def register(ctx):
    id = str(ctx.message.author.id)
    if id not in amounts:
        amounts[id] = 100
        await ctx.send("You are now registered.")
        _save()
    else:
        await ctx.send("You already have an account.")

@bot.command(name="transfer", pass_context=True)
async def transfer(ctx, amount: int, other: discord.Member):
    primary_id = str(ctx.message.author.id)
    other_id = str(other.id)
    if primary_id not in amounts:
        await ctx.send("You do not have an account.")
    elif other_id not in amounts:
        await ctx.send(other.display_name + " does not have an account.")
    elif amounts[primary_id] < amount:
        await ctx.send("You cannot afford this transaction.")
    else:
        amounts[primary_id] -= amount
        amounts[other_id] += amount
        await ctx.send("Transaction complete.")
    _save()

@bot.command(name="give", pass_context=True)
@commands.has_permissions(administrator=True)
async def give(ctx, amount: int, user: discord.Member):
    user_id = str(user.id)
    if user_id in amounts:
        amounts[user_id] += amount
        await ctx.send("Transaction complete. " + user.display_name + " now has a balance of " + str(amounts[user_id]) + " dollars.")
    else:
        await ctx.send(user.display_name + " does not have an account.")
    _save()

@bot.command(name="reset", pass_context=True)
async def reset(ctx):
    id = str(ctx.message.author.id)
    if id not in amounts:
        await ctx.send("You do not have an account.")
    else:
        amounts[id] = 100
        await ctx.send("Balance reset to $100.")
    _save()

@bot.command(name="leaderboard", pass_context=True)
async def leaderboard(ctx):
    embed=discord.Embed(title="The Lounge Leaderboard", color=0x0096ff)
    k = Counter(amounts)
    high = k.most_common(3)
    for i in high:
        user_id = int(i[0])
        user = await bot.fetch_user(user_id)
        balance = i[1]
        embed.add_field(name=user.display_name, value="$" +     str(i[1]), inline=False)
    await ctx.send(embed=embed)

def _save():
    with open('amounts.json', 'w+') as f:
        json.dump(amounts, f)

@bot.command(name="save")
async def save(ctx):
    await ctx.send("Balances saved.")
    _save()

bot.run(TOKEN)
