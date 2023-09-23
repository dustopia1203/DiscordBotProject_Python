import discord
import os
import asyncio

from discord.ext import commands
from dotenv import load_dotenv
from bardapi import Bard


load_dotenv()
BARDAPI_KEY = os.getenv('BARDAPI_KEY')
CHANNEL_ID = int(os.getenv('CHANNEL_DISCORD_ID'))


bard = Bard(token=BARDAPI_KEY)


class BardAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def ask(self, ctx, *, question):
        ''' Ask BARD AI a question '''
        try:
            check = False
            channel = self.bot.get_channel(CHANNEL_ID)
            await channel.send(f"Sure 😊! Waiting for a moment...")
            response = bard.get_answer(question)["content"]
            if len(response) < 2000:
                await ctx.send(response)
            else:
                answer = response.split("\n")
                images = list(bard.get_answer(question)["images"])
                for paragraph in answer:
                    if paragraph == "":
                        continue
                    elif paragraph.startswith("[Image"):
                        check = True
                    await ctx.send(paragraph)
                if check:
                    await ctx.send("Some images I can find: ")
                    for image in images:
                        await ctx.send(image)
        except Exception as e:
            error_message = (
                f"**Error 😣:**\n\n"
                f"```\n"
                f"{str(e)}\n"
                f"```\n"
            )
            await ctx.send(error_message)


async def setup(bot):
    await bot.add_cog(BardAI(bot))
