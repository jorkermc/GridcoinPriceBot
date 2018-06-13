import dapp

import datetime
import sys
import time

with open('help.md') as f:
    help_text = f.read()


class Meta(dapp.DiscordPlugin):
    @dapp.command()
    async def ping(self, ctx):
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        time_delta = round((t2-t1)*1000)
        await self.bot.send(":ping_pong: | `{}ms`".format(time_delta), ctx)

    @dapp.command()
    @dapp.is_owner()
    async def exit(self, ctx):
        await self.bot.send(":wave: | Goodbye!", ctx, 0xFF0000)
        raise SystemExit(await self.bot.logout())

    @dapp.command()
    async def uptime(self, ctx):
        td = datetime.datetime.now() - self.bot.start_time
        days, hours, minutes = td.days, td.seconds // 3600, td.seconds // 60 % 60
        await self.bot.send(":clock1: | {} day(s) {} hour(s) {} minute(s).".format(days, hours, minutes), ctx)

    @dapp.command()
    async def source(self, ctx):
        await ctx.send('<https://bitbucket.org/jorkermc/gridcoinpricebot/src/master/>')

    @dapp.command()
    async def help(self, ctx):
        await self.bot.send(help_text, ctx)


def setup(bot):
    bot.add_cog(Meta(bot))
