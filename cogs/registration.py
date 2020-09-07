import discord
from discord.ext import commands
import sys, asyncio


configFile = open('config')
configs = configFile.readlines()
config = {
    'OWNER': {
        'ids': configs[3].split()[1].split('\n')[0].split(',')
    }
}

class RegistrationCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('yes {}, I am here'.format(ctx.message.author.mention))


# set the cog up
def setup(bot):
    bot.add_cog(RegistrationCog(bot))







