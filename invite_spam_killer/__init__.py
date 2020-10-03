
from .invitespamkiller import InviteSpamKiller

def setup(bot):
    bot.add_cog(InviteSpamKiller(bot))
