import discord
from discord.ext import commands
import os
from bardapi import Bard
from dotenv import load_dotenv
from load_game import *


load_dotenv()


BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN') 
BARDAPI_KEY = os.getenv('BARDAPI_KEY')
WEATHER_KEY = os.getenv('OPENWEATHERMAP_KEY')


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
CHANNEL_ID = int(os.getenv('CHANNEL_DISCORD_ID'))


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"{bot.user.name} has connected to channel!")


@bot.command()
async def clear(ctx, ammount=""):
    ''' Clear messages '''
    if ammount == "" or ammount == "all":
        await ctx.channel.purge(limit=None)
    else:
        await ctx.channel.purge(limit=int(ammount))


@bot.command()
async def games(ctx):
    ''' List all games '''
    await ctx.send("Loading games...")
    await load_game(ctx, bot=bot)


bot.run(BOT_TOKEN)