import discord
from discord.ext import commands

import datetime


class DiscordPlugin:
    def __init__(self, bot):
        self.bot = bot

    async def ainit(self):
        pass


class DiscordBotFramework(commands.Bot):
    def __init__(self, command_prefix, default_colour, formatter=None, description=None, pm_help=False, **options):
        super(commands.Bot, self).__init__(command_prefix, formatter, description, pm_help, **options)
        self.default_colour = discord.Colour(default_colour)
        self.first_run = True
        self.start_time = datetime.datetime.now()

    async def on_ready(self):
        if self.first_run:
            self.remove_command('help')
            for plugin in self.plugins:
                self.load_extension(".".join([getattr(self, 'plugin_prefix', None), plugin]))
            for cog in self.cogs:
                await self.cogs[cog].ainit()
            self.first_run = False

    async def send(self, message, ctx, colour=None):
        await ctx.send(embed=discord.Embed(colour=colour or self.default_colour, description=message))

