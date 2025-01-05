import discord
from redbot.core import Config, commands, checks

class helloworld_cog(getattr(commands, "Cog", object)):
    """Hello World V3 cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """This is a Hello World V3 cog!"""

        #Your code will go here
        await ctx.send("Hello World!")

    @commands.command()
    async def list_members(self, ctx):  
      guild = ctx.guild
       
      await ctx.send(', ' + str(guild.members))
        
def setup(bot):
    bot.add_cog(helloworld_cog(bot))
