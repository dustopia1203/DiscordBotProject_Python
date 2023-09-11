import discord
from discord.ext import commands
import os
from bardapi import Bard
from dotenv import load_dotenv
from load_game import *
import requests


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


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Welcome {member.name} to my channel!")


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Goodbye {member.name}. See you later!")


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


@bot.command()
async def weather(ctx, *, location):
    ''' Get weather information '''
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + location + "&appid=" + WEATHER_KEY
    response = requests.get(URL)
    data = response.json()
    if data["cod"] != "404":
        main_data = data["main"]
        temperature_avg = main_data["temp"] - 273.15
        temperature_min = main_data["temp_min"] - 273.15
        temperature_max = main_data["temp_max"] - 273.15
        pressure = main_data["pressure"]
        humidity = main_data["humidity"]
        visibility = data["visibility"] / 1000
        weather_data = data["weather"]
        weather_description = weather_data[0]["description"]
        weather_report = (
            f"Location: {location}\n"
            f"Temperature: {temperature_avg:.2f}°C ({temperature_min:.2f} - {temperature_max:.2f}°C)\n"
            f"Pressure: {pressure} hPa\n"
            f"Humidity: {humidity}%\n"
            f"Visibility: {visibility} km\n"
            f"Description: {weather_description}\n"
        )
        await ctx.send(weather_report)
    else:
        await ctx.send(f"Could not find weather information for {location}")


bot.run(BOT_TOKEN)