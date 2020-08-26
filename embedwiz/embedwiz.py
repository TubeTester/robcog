"""
"Embed wizard" cog by GrumpiestVulcan
Commissioned 2018-01-15 by Aeternum Studios
POC: Aeternum#7967 (#173291729192091649)
Ported to Redbot V3 by Rob Brown
"""

__author__ = "Caleb Johnson <me@calebj.io> (calebj#0001), Ported to Redbot V3 by Rob Brown"
__copyright__ = "Copyright 2018, Holocor LLC"
__version__ = '1.5.2'

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


def color_converter(color):
    if type(color) is int:
        if color < 0 or color > 0xffffff:
            raise ValueError('Color value is outside of valid range')
        return '%06x' % color
    color = color.strip('#')
    if color.startswith('0x'):
        color = color[2:]
    if len(color) != 6 or set(color) - set(string.hexdigits):
        raise ValueError('Invalid color hex value')
    return color


def is_valid_color(color):
    try:
        color_converter(color)
        return True
    except Exception:
        return False


def is_valid_url(url: str):
    if not url:
        return False

    token = urlparse(url)
    scheme_ok = token.scheme.lower() in {'http', 'https'}
    netloc_split = token.netloc.split('.')
    netloc_ok = len(list(filter(None, netloc_split))) > 1
    return scheme_ok and netloc_ok


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


class EmbedWizard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            #self.bot.logger.exception(error)
            self.analytics = None

    @commands.group(pass_context=True, invoke_without_command=True)
    async def embedwiz(self, ctx, *, specification):
        """
        Posts an embed according to the given specification:
        title;color;footer;footer_icon;image;thumbnail;body
        All values can be seperated by newlines, spaces, or other whitespace.
        Only the first six semicolons are used, the rest are ignored. To
        use semicolons in any of the first six fields, escape it like so: \\;
        To include a backslash before a semicolon without escaping, do: \\\\;
        Color can be a #HEXVAL, "random", or a name that discord.Color knows.
        Options: https://discordpy.readthedocs.io/en/async/api.html#discord.Colour
        All URLs (footer_icon, image, thumbnail) can be empty or "none".
        Use a body of "prompt" to use your next message as the content.
        Timestamp must be an ISO8601 timestamp, UNIX timestamp or 'now'.
        An ISO8601 timestamp looks like this: 2017-12-11T01:15:03.449371-0500.
        Start the specification with -noauthor to skip the author header.
        Note: only mods, admins and the bot owner can edit authorless embeds.
        Keyword-based expressions can be built by starting it with '-kw'
        Each parameter above can be specified as param1=value1;param2=value2;...
        This method allows two more parameters: url and timestamp (see above).
        WARNING: embeds are hidden to anyone with 'link previews' disabled.
        """
        if ctx.invoked_subcommand is None:
            embed = await self._parse_embed(ctx, specification)
            if embed:
                await ctx.send(embed=embed)

    @checks.mod_or_permissions(manage_messages=True)
    @embedwiz.command(name='channel', pass_context=True)
    async def embedwiz_channel(self, ctx, *, specification):
        """
        Posts an embed in another channel according to the spec.
        See [p]help embedwiz for more information.
        """
        channel = ctx.channel
        member = channel.server and channel.server.get_member(ctx.message.author.id)
        override = self._check_override(member)

        if channel != ctx.message.channel and not member:
            await ctx.send(error("Channel is private or you aren't in the server that channel belongs to."))
            return
        elif not channel.permissions_for(member).send_messages:
            msg = error("You don't have permissions to post there!")
            await ctx.send(msg)
            return

        embed = await self._parse_embed(ctx, specification, force_author=not override)

        if embed:
            channel = ctx.channel
            await channel.send(embed=embed)

            if channel != ctx.message.channel:
                await ctx.send("Embed sent to %s." % channel.mention)

    @checks.mod_or_permissions(manage_messages=True)
    @embedwiz.command(name='delete', pass_context=True, no_pm=True)
    async def embedwiz_delete(self, ctx, discord.Message):
        """
        Posts an embed according to the spec after deleting the original message.
        See [p]help embedwiz for more information.
        """
        #channel = ctx.channel
        #msg = await channel.get_message(channel, message_id)
        #await self.bot.delete_message(msg)
        await Message.delete()
        return
        
        #perms = ctx.channel.permissions_for(discord.Member)
        #can_delete = perms.manage_messages

        #if not can_delete:
            #msg = "I can't delete your command message! Posting anyway..."
            #await ctx.send(warning(msg))

        tup = await self._parse_embed(ctx, specification, return_todelete=True)

        if tup:
            embed, to_delete = tup
            #await ctx.send(embed=embed)

            #if not can_delete:
                #return

            for msg in [ctx.message, *to_delete]:
                try:
                    await self.bot.delete_message(msg)
                except discord.HTTPException:
                    continue

    @embedwiz.command(name='edit', pass_context=True)
    async def embedwiz_edit(self, ctx, *, message_id: int, specification):
        """
        Edits an existing embed according to the spec.
        See [p]help embedwiz for more information.
        """
        channel = ctx.channel
        member = channel.server and channel.server.get_member(ctx.message.author.id)

        if channel != ctx.message.channel and not member:
            await ctx.send(error("Channel is private or you aren't in the server that channel belongs to."))
            return

        try:
            msg = await self.bot.get_message(channel, str(message_id))
        except discord.errors.NotFound:
            await ctx.send(error('Message not found.'))
            return
        except discord.errors.Forbidden:
            await ctx.send(error('No permissions to read that channel.'))
            return

        if msg.author.id != self.bot.user.id:
            await ctx.send(error("That message isn't mine."))
            return
        elif not msg.embeds:
            await ctx.send(error("That message doesn't have an embed."))
            return

        old_embed = msg.embeds[0]
        override = self._check_override(member)

        if override:
            pass
        elif 'author' not in old_embed or 'name' not in old_embed['author']:
            await ctx.send(error("That embed doesn't have an author set, and you aren't a mod or admin."))
            return
        elif old_embed['author']['name'].split('(')[-1][:-1] != ctx.message.author.id:
            await ctx.send(error("That embed isn't yours."))
            return

        new_embed = await self._parse_embed(ctx, specification, force_author=not override)
        await self.bot.edit_message(msg, embed=new_embed)
        await ctx.send('Embed edited successfully.')

    def _check_override(self, member):
        server = isinstance(member, discord.Member) and member.server

        if member and server:
            admin_role = self.bot.settings.get_server_admin(server)
            mod_role = self.bot.settings.get_server_mod(server)

            return any((member.id == self.bot.settings.owner,
                        member.id in self.bot.settings.co_owners,
                        member == server.owner,
                        discord.utils.get(member.roles, name=admin_role),
                        discord.utils.get(member.roles, name=mod_role)))
        else:
            return False

    async def _parse_embed(self, ctx, specification, *, return_todelete=False, force_author=False):
        to_delete = []
        author = ctx.message.author
        specification = specification.strip()
        set_author = True
        use_keywords = False

        while specification.startswith(('-noauthor', '-kw')):
            if specification.startswith('-noauthor'):
                if force_author:
                    await ctx.send(error("You cannot post using -noauthor."))
                    return

                set_author = False
                specification = specification[9:]

            if specification.startswith('-kw'):
                use_keywords = True
                specification = specification[3:]

            specification = specification.strip()

        maxsplit = 0 if use_keywords else 6
        split = re.split(r'(?<!(?<!\\)\\);', specification, maxsplit)

        if use_keywords:
            params = {}

            for param in split:
                match = extract_param(param)

                if param and not match:
                    await ctx.send(error('Invalid key=value expression: `%s`' % param))
                    return
                elif not param:
                    continue

                param, value = match
                if param in params:
                    await ctx.send(error('Duplicate `%s` field!' % param))
                    return
                elif param not in VALID_FIELDS:
                    await ctx.send(error('Unknown field: `%s`' % param))
                    return

                params[param] = value

            title = params.get('title', Embed.Empty)
            url = params.get('url', Embed.Empty)
            color = params.get('color', Embed.Empty)
            footer = params.get('footer', Embed.Empty)
            footer_icon = params.get('footer_icon', Embed.Empty)
            image = params.get('image', Embed.Empty)
            thumbnail = params.get('thumbnail', Embed.Empty)
            body = params.get('body', Embed.Empty)
            timestamp = params.get('timestamp', Embed.Empty)
        else:
            # If user used double backslash to avoid escape, replace with a single one
            for i, s in enumerate(split[:-1]):
                if s.endswith(r'\\'):
                    split[i] = s[:-1]

            nfields = len(split)

            if nfields != 7:
                op = 'many' if nfields > 7 else 'few'
                msg = 'Invalid specification: got too {} fields ({}, expected 7)'
                await ctx.send(error(msg.format(op, nfields)))
                return

            timestamp = Embed.Empty
            url = Embed.Empty
            title, color, footer, footer_icon, image, thumbnail, body = map(str.strip, split)

        if title:
            url_split = extract_md_link(title)

            if url_split:
                if url:
                    await ctx.send(error('Duplicate `url` in markdown format title!'))
                    return
                else:
                    title, url = url_split

        try:
            if color:
                color = int(color_converter(color), 16)
            else:
                color = Embed.Empty
        except ValueError as e:
            colorstr = color.lower().strip().replace(' ', '_')

            if colorstr == 'random':
                color = discord.Color(random.randrange(0x1000000))
            elif colorstr == 'none':
                color = Embed.Empty
            elif colorstr.strip() == 'black':
                color = discord.Color.default()
            elif hasattr(discord.Color, colorstr):
                color = getattr(discord.Color, colorstr)()
            else:
                await ctx.send(error(e.args[0]))
                return

        if url and not is_valid_url(url):
            await ctx.send(error('Invalid title URL!'))
            return

        if not footer or footer.lower() in ('none', ''):
            footer = Embed.Empty

        if not footer_icon or footer_icon.lower() in ('none', ''):
            footer_icon = Embed.Empty
        elif not is_valid_url(footer_icon):
            await ctx.send(error('Invalid footer icon URL!'))
            return

        if not image or image.lower() in ('none', ''):
            image = Embed.Empty
        elif not is_valid_url(image):
            await ctx.send(error('Invalid image URL!'))
            return

        if not thumbnail or thumbnail.lower() in ('none', ''):
            thumbnail = Embed.Empty
        elif not is_valid_url(thumbnail):
            await ctx.send(error('Invalid thumbnail URL!'))
            return

        if timestamp:
            try:
                timestamp = parse_timestamp(timestamp)
            except ValueError:
                await ctx.send(error('Invalid timestamp!'))
                return

        if body and body.lower() == 'prompt':
            msg = await ctx.send('Post the desired content of your embed, or "cancel" to '
                                     'cancel. Will wait up to one minute.')
            to_delete.append(msg)

            msg = await self.bot.wait_for_message(author=author, timeout=60,
                                                  channel=ctx.message.channel)
            if msg is None:
                await ctx.send(error('Timed out waiting for a reply.'))
                return
            else:
                to_delete.append(msg)

            if msg.content.lower().strip() == 'cancel':
                await ctx.send(info('Cancelled.'))
                return
            else:
                body = msg.content

        embed = Embed(title=title, color=color, description=body, url=url, timestamp=timestamp)

        if set_author:
            embed.set_author(name='%s (%s)' % (author.display_name, author.id),
                             icon_url=author.avatar_url or discord.Embed.Empty)

        if image:
            embed.set_image(url=image)
        if footer or footer_icon:
            embed.set_footer(text=footer, icon_url=footer_icon)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if return_todelete:
            return embed, to_delete

        return embed

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)


def setup(bot):
    bot.add_cog(EmbedWizard(bot))
