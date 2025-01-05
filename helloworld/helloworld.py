import discord
import datetime
from redbot.core import Config, commands, checks

intents = discord.Intents.all()
client = discord.Client(intents=intents)

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
    async def lastMessage(self, ctx, users_id: int):
        oldestMessage = None
        for channel in ctx.guild.text_channels:
            fetchMessage = await channel.history().find(lambda m: m.author.id == users_id)
            if fetchMessage is None:
                continue


            if oldestMessage is None:
                oldestMessage = fetchMessage
            else:
                if fetchMessage.created_at > oldestMessage.created_at:
                    oldestMessage = fetchMessage

        if (oldestMessage is not None):
            await ctx.send(f"Oldest message is {oldestMessage.content}")
        else:
            await ctx.send("No message found.")

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
            for channel in ctx.guild.text_channels:
                if(len(mmessage) == 0):
                    mmessage = await channel.history(limit=1).flatten()
            ###async for message in member.history(limit=1, oldest_first=True):
                ###m = await member.fetch_message(message.id)
                ###if(len(m.content) > 0):
                    ###await ctx.send(m.content)
                    ###mmessage = m.content
                    
                ###if message.author == member:                    
                    ###mmessage = message.content
            
            members.append(member.name + ',' + str(id) + ', '+ mmessage + ' \r')
            ###last_message = [message async for message in member.history(limit=1, oldest_first=True)]
            ###await ctx.send(f'{member}')

        members.append(f'``` DONE! \r');
        await ctx.send('' .join(members))
        ###await ctx.send(last_message)

 
    async def on_raw_typing(channel, user, when):
        await ctx.send("{} is typing message in {} : {}".format(user.name, channel, when))

        
def setup(bot):
    bot.add_cog(helloworld_cog(bot))
