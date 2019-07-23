import discord
from redbot.core import Config, commands, checks

BaseCog = getattr(commands, "Cog", object)

class Robcog(BaseCog):
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rob(self):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("I can do stuff!")

def setup(bot):
    bot.add_cog(Robcog(bot))
