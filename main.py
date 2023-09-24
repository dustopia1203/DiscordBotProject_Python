import nextcord
import os
import asyncio

from nextcord.ext import commands
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN') 
CHANNEL_ID = int(os.getenv('CHANNEL_DISCORD_ID'))


intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"{bot.user.name} has connected to channel!")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Welcome {member.name} to my channel!")


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Goodbye {member.name}. See you later!")


@bot.command()
async def cls(ctx, ammount=""):
    ''' Clear messages '''
    if ammount == "" or ammount == "all":
        await ctx.channel.purge(limit=None)
    else:
        await ctx.channel.purge(limit=int(ammount))


for fileName in os.listdir("./cogs"):
    if fileName.endswith(".py"):
        bot.load_extension(f"cogs.{fileName[:-3]}")


bot.run(BOT_TOKEN)