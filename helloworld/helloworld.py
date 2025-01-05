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
        for member in get_members:  
            members.append(member.name)
            await ctx.send(f'{m}')
            await ctx.send('DONE!')
        ###for member in guild.fetch_members(limit=150):
           ### print(member.name)
            
      ###await ctx.send(', ' + str(guild.members))

    @commands.command(name='members')
    async def _members(self, ctx):
        members = []
        guild = ctx.guild
        for m in guild.members():
            members.append(m.name)
            await ctx.send(f'{m}')
            await ctx.send('DONE!')
        
def setup(bot):
    bot.add_cog(helloworld_cog(bot))
