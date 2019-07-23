from .helloworld import helloworld_cog

def setup(bot):
    bot.add_cog(helloworld_cog(bot))
