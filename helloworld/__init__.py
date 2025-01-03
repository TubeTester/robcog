from .helloworld import helloworld_cog

def setup(bot):
    await bot.add_cog(helloworld_cog(bot))
