import discord
from discord.ext import commands
import sys, asyncio
from utils.db import RegisterMember, GetMember, UpdateMemberStatus



class RegistrationCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


    # Attempt to register the new user on join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not GetMember(member):
            RegisterMember(member)
            return
        
        #user is a returning member
        UpdateMemberStatus(member)


    @commands.command()
    async def register(self, ctx, *args):


        #ERROR CHECK - dm bot commands not allowed
        try:
            ctx.guild.id # if no guild id then this is a dm
        except:
            error = "**You cannot run bot commands in a DM** "
            error += "Please retry your command in a bot friendly channel in your server where I reside."
            await ctx.message.author.send('{}'.format(error))
            return


        # HELP COMMAND INVOKED
        if len(args) and args[0].lower() == 'help':
            await ctx.invoke(self.bot.get_command('help'), option='register')
            return


        updated = RegisterMember(ctx.message.author)
        if updated:
            await ctx.send('{}: You are already registered, but your information was updated if anythings changed'.format(ctx.message.author.mention))
            return
        
        await ctx.send('{}: Successfully registered'.format(ctx.message.author.mention))




    @commands.command()
    async def ping(self, ctx):
        await ctx.send('yes {}, I am here'.format(ctx.message.author.mention))


# set the cog up
def setup(bot):
    bot.add_cog(RegistrationCog(bot))







