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
        ### get_members = ([m for m in guild.members])  
        ### for bot in get_members:  
            ###members.append(m.name)  
        await for member in guild.fetch_members(limit=150):
            print(member.name)
            
      ###await ctx.send(', ' + str(guild.members))

    @client.command(name='members')
    async def _members(ctx, guild_id: int):
        members = []
        guild = client.get_guild(guild_id)
        for m in guild.members():
            members.append(m.name)
            await ctx.send(f'{m}')
            await ctx.send('DONE!')
        
def setup(bot):
    bot.add_cog(helloworld_cog(bot))
