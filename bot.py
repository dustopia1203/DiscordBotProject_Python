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


bot.run(BOT_TOKEN)