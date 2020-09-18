import discord
from discord.ext import commands
import sys, traceback, platform
from utils.configsloader import loadBotConfigs


# COGS
initial_extensions = [
    'cogs.developer',
    'cogs.registration',
    'cogs.member',
    'cogs.help'
]

# Get bot from config
config = loadBotConfigs()
bot = commands.Bot(command_prefix = config['prefix'])
bot.remove_command('help')


@bot.event
async def on_ready():
    print('\n\n\nLogged in as {} (ID: {}) | Connected to {} servers'.format(bot.user, bot.user.id, len(bot.guilds)))
    print('-------'*18)
    print('Discord.py Version: {} | Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('-------'*18)
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('-------'*18)
    print('Support Discord Server: https://discord.gg/FNNNgqb')
    print('-------'*18)

    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
                print('{} loaded'.format(extension))
            except Exception:
                print('issue with',extension)
                traceback.print_exc()
        print('Successfully logged in and booted...! Use prefix: "'+config['prefix']+'".\n\n')

# Start your engines~~
bot.run(config['token'], bot=True, reconnect=True)
