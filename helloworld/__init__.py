from .helloworld import helloworld_cog

async def setup(bot):
    await bot.add_cog(helloworld_cog(bot))
