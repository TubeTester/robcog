"""
"Invite Spam Killer" cog by Rob Brown
"""

__author__ = "Rob Brown"
__copyright__ = "MIT license"
__version__ = '0.0.1'

from datetime import datetime
import random
import re
import string
from urllib.parse import urlparse

import discord
from discord import Embed
#from discord.ext import commands

#from redbot.core.utils import checks
from redbot.core import checks, commands
from redbot.core.utils.chat_formatting import warning, error, info


VALID_FIELDS = {'url', 'title', 'color', 'timestamp', 'footer', 'footer_icon', 'image', 'thumbnail', 'body'}

def extract_md_link(inputstr: str):
    match = re.match(r'^\[([^\]]*)\]\(([^)]*)\)$', inputstr)
    if match:
        return match.groups()


def extract_param(inputstr: str):
    split = re.split(r'(?<!(?<!\\)\\)=', inputstr, 1)
    if len(split) == 2:
        return [s.strip() for s in split]


def convert_iso8601(input_string):
    tsre = r"[:]|([-](?!((\d{2}[:]\d{2})|(\d{4}))$))"
    ts = re.sub(tsre, '', input_string)

    if ts.endswith(('z', 'Z')):
        ts = ts[:-1] + '+0000'

    if '.' in ts:
        fmt = "%Y%m%dT%H%M%S.%f%z"
    else:
        fmt = "%Y%m%dT%H%M%S%z"

    return datetime.strptime(ts, fmt)


def parse_timestamp(inputstr: str):
    if inputstr.lower() == 'now':
        return datetime.utcnow()
    elif inputstr.count('.') <= 1 and inputstr.replace('.', '').isdigit():
        return datetime.utcfromtimestamp(float(inputstr))
    else:
        return convert_iso8601(inputstr)


class InviteSpamKiller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            #self.bot.logger.exception(error)
            self.analytics = None

    @checks.mod_or_permissions(manage_messages=True)
    @commands.group(pass_context=True, invoke_without_command=True)
    async def setup(self, ctx, *, specification):
        """
        Setup Invite Spam Killer
        """
        msg = error("Setup Stub.")
        await ctx.send(msg)


    def _check_override(self, ctx,  member):
        server = isinstance(member, discord.Member) and member.guild
        return True

        if member and server:
            guild_settings = ctx.bot.db.guild(ctx.guild)
            admin_role_id = guild_settings.admin_role()
            mod_role_id = guild_settings.mod_role()
            #admin_role = settings.get_server_admin(server)
            #mod_role = self.bot.settings.get_server_mod(server)

            return any((member.id == self.bot.settings.owner,
                        member.id in self.bot.settings.co_owners,
                        member == server.owner,
                        discord.utils.get(member.roles, name=admin_role),
                        discord.utils.get(member.roles, name=mod_role)))
        else:
            return False

    

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)
            
     async def on_invite_create(self, command, ctx):
        if ctx.cog is self
            msg = error("Setup Stub.")
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(InviteSpamKiller(bot))
