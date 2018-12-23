import aiohttp

import dapp

API_ENDPOINT = "https://api.coincap.io/v2"
# MAP_ENDPOINT = "/map"
COIN_ENDPOINT = "assets"
MARKET_ENDPOINT = 'markets'


def url_join(*parts):
    return '/'.join(parts)


class Price(dapp.DiscordPlugin):
    def __init__(self, bot):
        super(Price, self).__init__(bot)
        self.sc = aiohttp.ClientSession()
        self.tickers = {}

    async def ainit(self):
        pass

    def __unload(self):
        self.bot.loop.run_until_complete(self.sc.close())

    async def get_coin(self, coin):
        async with self.sc.get(url_join(API_ENDPOINT, COIN_ENDPOINT, coin)) as res:
            try:
                return await res.json()
            except Exception:
                print(await res.text())

    async def get_markets(self, coin, limit=5):
        async with self.sc.get(url_join(API_ENDPOINT, COIN_ENDPOINT,
                                        coin, MARKET_ENDPOINT), data={'limit': limit}) as res:
            return await res.json()

    @dapp.command()
    async def price(self, ctx, coin="gridcoin"):
        c = await self.get_coin(coin)
        url = url_join('https://coincap.io/assets', coin)
        if not c['data']:
            self.log_warning("Couldn't find currency: {}".format(coin))
            return await ctx.message.add_reaction('\u274C')
        c = c['data']
        e = dapp.Embed(title="{} ({})".format(c['name'], c['symbol']), colour=self.bot.default_colour, url=url)
        data = [' '.join(["Price:", str(c['priceUsd']), 'USD']), ' '.join(["Rank:", str(c['rank'])]),
                ' '.join(["Market Cap:", str(c['marketCapUsd']), "USD"]),
                ' '.join(["Total Supply:", str(c['supply']), c['symbol']]),
                ' '.join(["Max Supply:", str(c['maxSupply'] or '∞'), c['symbol']]),
                ' '.join(["24HR Trading Volume:", str(c['volumeUsd24Hr']), "USD"]),
                ' '.join(["Cap Change:", "{0:+02.2f}".format(float(c['changePercent24Hr'])) + '%']),
                ' '.join(["24H VWAP:", '{:.8f}'.format(round(float(c['vwap24Hr']), 8)), "USD"])]
        e.add_field(name="Data", value='\n'.join(data))
        await ctx.send(embed=e)

    @dapp.command()
    async def usd(self, ctx, coin="gridcoin"):
        c = await self.get_coin(coin)
        if not c['data']:
            self.log_warning("Couldn't find currency: {}".format(coin))
            return await ctx.message.add_reaction('\u274C')
        c = c['data']
        await ctx.send(str(c['priceUsd']))

    @dapp.command()
    async def markets(self, ctx, coin='gridcoin'):
        c = await self.get_markets(coin, limit=2000)
        url = url_join('https://coincap.io/assets', coin)
        if not c['data']:
            self.log_warning("Couldn't find currency: {}".format(coin))
            return await ctx.message.add_reaction('\u274C')
        c = c['data']
        data = []
        for market in sorted(c, key=lambda x: float(x['volumeUsd24Hr'] or 0), reverse=True)[:10]:
            data.append(['{} {}-{}'.format(market['exchangeId'], market['baseSymbol'], market['quoteSymbol']),
                         ' '.join(["Price:", str(market['priceUsd']), 'USD']),
                         ' '.join(["24HR Trading Volume:", str(market['volumeUsd24Hr']),
                                   "USD", '({:.2f}%)'.format(float(market['volumePercent'] or 0))])])
        e = dapp.Embed(title=coin.title() + ' Markets', colour=self.bot.default_colour, url=url)
        for market in data:
            e.add_field(name=market.pop(0), value='\n'.join(market))
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Price(bot))
