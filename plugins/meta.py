import dapp

import datetime
import io
import textwrap
import time
import traceback

from contextlib import redirect_stdout


class Meta(dapp.DiscordPlugin):

    def __init__(self, bot):
        super(Meta, self).__init__(bot)
        self.last_result = None

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

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
        e = dapp.Embed(colour=self.bot.default_colour, title='GridcoinPriceBot')
        e.set_footer(text="Made by jorkermc#3727", icon_url='https://cdn.discordapp.com/attachments/381963689470984203/452757349657083904/jorkermc.png')
        commands = [('help', 'Shows help about a command or the bot.'),
                    ('source', 'Links you to the source code of the bot.'),
                    ('uptime', 'Shows how long the bot has been up.'),
                    ('ping', 'Calculates the ping between the bot and the discord servers.'),
                    ('price', 'Returns the price and a little more data for a cryptocurrency'),
                    ('usd', 'Returns the price of a cryptocurrency in USD'),
                    ('eur', 'Returns the price of a cryptocurrency in EUR')]
        for command in commands:
            e.add_field(name=command[0], value=command[1])
        await ctx.send(embed=e)

    @dapp.command(name='eval')
    @dapp.is_owner()
    async def _eval(self, ctx, *, body: str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self.last_result
        }
        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    bot.add_cog(Meta(bot))
