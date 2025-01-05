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
        members = []  
        get_members = ([member for member in guild.members if not member.bot])  
        ctx.send('```');
        for member in get_members:  
            members.append(member.name)
            await ctx.send(f'{member}')
            
        await ctx.send('``` DONE!')
        
def setup(bot):
    bot.add_cog(helloworld_cog(bot))
