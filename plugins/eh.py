import asyncio

from discord.ext import commands

import dapp

NOT_OWNER = "\U0001f1fa \U0001f1f4 \U0001f1fc \U0001f1f3 \U0001f1ea \U0001f1f7 \U00002753".split()


class CommandErrorHandler(dapp.DiscordPlugin):

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(error, commands.errors.NotOwner):
            for emoji in NOT_OWNER:
                await ctx.message.add_reaction(emoji)
            except asyncio.TimeoutError:
                pass


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
