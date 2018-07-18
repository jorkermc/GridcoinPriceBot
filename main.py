import auth
import dapp


class Bot(dapp.DiscordBotFramework):
    plugin_prefix = 'plugins'
    plugins = ['meta', 'price', 'eh']


Bot('$', 0x6800cb).run(auth.token)
