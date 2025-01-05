import discord
import datetime
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
        await ctx.send(datetime.date)

    @commands.command()
    async def listm(self, ctx): 
        guild = ctx.guild
        ###cut_date = datetime.utcnow() - timedelta(days=15)
        members = []  
        members.append('```')
        get_members = ([member for member in guild.members if not member.bot])  
        for member in get_members:
            id = member.id
            mmessage = ''
            async for message in member.history(limit=1, oldest_first=True):
                m = await member.fetch_message(message.id)
                if(len(m.content) > 0):
                    await ctx.send(m.content)
                    mmessage = m.content
                    
                ###if message.author == member:                    
                    ###mmessage = message.content
               
            members.append(member.name + ',' + str(id) + ', '+ mmessage + ' \r')
            last_message = [message async for message in member.history(limit=1, oldest_first=True)]
            ###await ctx.send(f'{member}')

        members.append(f'``` DONE! \r');
        await ctx.send('' .join(members))
        await ctx.send(last_message)
        
def setup(bot):
    bot.add_cog(helloworld_cog(bot))
