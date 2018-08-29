import asyncio

from discord.ext import commands

import dapp


class CommandErrorHandler(dapp.DiscordPlugin):
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(error, commands.errors.NotOwner):
            owner = self.bot.get_user(self.bot.owner_id)
            if owner.dm_channel is None:
                await owner.create_dm()
            await owner.dm_channel.send(f'User {ctx.author} tried to execute owner command "{ctx.command.name}"')
            await owner.dm_channel.send(f'in channel {ctx.channel.name} in guild {ctx.guild.name}')
        else:
            print(f'{error.__class__.name}: {error}')


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
