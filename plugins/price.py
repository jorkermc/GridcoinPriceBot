import aiohttp

import dapp

API_ENDPOINT = "http://coincap.io"
MAP_ENDPOINT = "/map"
COIN_ENDPOINT = "/page/{}"


class Price(dapp.DiscordPlugin):
    def __init__(self, bot):
        super(Price, self).__init__(bot)
        self.sc = aiohttp.ClientSession()
        self.tickers = {}

    async def ainit(self):
        coin_map = await self.get_map()
        for coin in coin_map:
            try:
                self.tickers[coin["name"].lower()] = coin["symbol"]
            except KeyError:
                pass

    def __unload(self):
        self.bot.loop.run_until_complete(self.sc.close())

    async def get_map(self):
        async with self.sc.get(API_ENDPOINT + MAP_ENDPOINT) as res:
            return await res.json()

    async def get_coin(self, coin):
        async with self.sc.get(API_ENDPOINT + COIN_ENDPOINT.format(coin)) as res:
            return await res.json()

    @dapp.command()
    async def price(self, ctx, coin="GRC"):
        c = await self.get_coin(self.tickers.get(coin.lower(), coin.upper()))
        u = '/'.join([API_ENDPOINT, self.tickers.get(coin.lower(), coin.upper())])
        if not c:
            self.log_warning("Couldn't find currency: {}".format(coin))
            return await ctx.message.add_reaction('\u274C')
        e = dapp.Embed(title="{} ({})".format(c['display_name'], c['id']), colour=self.bot.default_colour, url=u)
        price = []
        data = []
        general = []
        for i in c:
            if i.startswith('price_'):
                price.append(" ".join(['{:.8f}'.format(round(c[i], 8)), i.replace('price_', '').upper()]))
        general.append(' '.join(["Total Market Cap:", str(c['totalCap']), "USD"]))
        general.append(' '.join(["Bitcoin Market Cap:", str(c['btcCap']), "USD"]))
        general.append(' '.join(["Altcoin Market Cap:", str(c['altCap']), "USD"]))
        general.append(' '.join(["Bitcoin Price:", str(c['btcPrice']), "USD"]))
        general.append(' '.join(["Total Volume:", str(c['volumeTotal']), "USD"]))
        general.append(' '.join(["Bitcoin Volume:", str(c['volumeBtc']), "USD"]))
        general.append(' '.join(["Altcoin Volume:", str(c['volumeAlt']), "USD"]))
        data.append(' '.join(["Rank:", str(c['rank'])]))
        data.append(' '.join(["Market Cap:", str(c['market_cap']), "USD"]))
        data.append(' '.join(["Total Supply:", str(c['supply']), c['id']]))
        data.append(' '.join(["24HR Trading Volume:", str(c['volume']), "USD"]))
        data.append(' '.join(["Cap Change:", "{0:+02.2f}".format(c['cap24hrChange']) + '%']))
        data.append(' '.join(["24H VWAP:", '{:.8f}'.format(round(c['vwap_h24'], 8)), "USD"]))
        e.add_field(name="Price", value='\n'.join(price), inline=True)
        e.add_field(name="Data", value='\n'.join(data), inline=True)
        e.add_field(name="General", value='\n'.join(general))
        await ctx.send(embed=e)

    @dapp.command()
    async def usd(self, ctx, coin="GRC"):
        c = await self.get_coin(self.tickers.get(coin.lower(), coin.upper()))
        if not c:
            self.log_warning("Couldn't find currency: {}".format(coin))
            return await ctx.message.add_reaction('\u274C')
        await ctx.send(str(c['price_usd']))

    @dapp.command()
    async def eur(self, ctx, coin="GRC"):
        c = await self.get_coin(self.tickers.get(coin.lower(), coin.upper()))
        if not c:
            self.log_warning("Couldn't find currency: {}".format(coin))
            return await ctx.message.add_reaction('\u274C')
        await ctx.send(str(c['price_eur']))


def setup(bot):
    bot.add_cog(Price(bot))
