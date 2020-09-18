import discord
import os
from discord.ext import commands
import sys, asyncio
from utils.constants import GITHUB
from utils.functions import PrepareCollaboratorWelcomePackage, GetMention, GetDiscordMemberObject, PrepareHiddenFiles
from utils.db import UserIsCollaborator, CollaboratorHasTopLevelPerms, AddNewCollaborator, SetNewCollaboratorPin



class DeveloperCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def info(self, ctx):
        title = '**MopBot INFORMATION**'
        info  = '*Created by **Bop#1308 & Marruk#1000***\n\n'
        info += '×  **version:** 1.0.0 **BETA**\n'
        info += '×  **prefix:** "."\n'
        info += '×  **help command:** `*Coming Soon*`\n'
        info += '×  **github:** {}\n'.format(GITHUB)
        footerText = 'Message Bop#1308 with feedback, questions, if you wish to become a collaborator, or anything else'

        embed = discord.Embed(title=title, description=info, color=1234123)
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)



    @commands.command()
    async def developer(self, ctx, *args):

     
        #ERROR CHECK - dm bot commands not allowed
        try:
            ctx.guild.id # if no guild id then this is a dm
        except:
            error = "**You cannot run bot commands in a DM** "
            error += "Please retry your command in a bot friendly channel in your server where I reside."
            await ctx.message.author.send('{}'.format(error))
            return

        #PERMISSION CHECK
        # is user a current developer
        res = UserIsCollaborator(ctx.message.author)
        if not res:
            error = ":x: **You must be a Collaborator to use this command.\n** "
            error += "If you believe you should have access, please contact Bop or Marruk"
            await ctx.send('{}'.format(error))
            return



        # HELP COMMAND INVOKED
        if args[0].lower() == 'help':
            await ctx.invoke(self.bot.get_command('help'), option='developer')



        # ADD OPTION
        #--------------------------------------
        if args[0].lower() == 'add':

            #PERMISSION CHECK
            # does user have top level perms?
            res = CollaboratorHasTopLevelPerms(ctx.message.author)
            if not res:
                error = ":x: **You do not have permission to add additional Collaborators.\n** "
                error += "If you believe you should have access to this command, please contact Bop or Marruk"
                await ctx.send('{}'.format(error))
                return

            #ERROR CHECK - should have exactly 2 args
            if len(args) != 2:
                error = ":x: **This command sequence requires exactly 2 arguments, `add` and the players discord username.** "
                error += "e.g. `.developer add MopBot`"
                await ctx.send('{}'.format(error))
                return

            #add new collaborator to database
            newCollaboratorID, pin = AddNewCollaborator(args[1])
            if not newCollaboratorID:
                error = ':x: **The user "{}" was not found. Collaborators must come from the clan and already be registered with me.**\n'
                error += "If user is not registered, have them run the `.register`"
                await ctx.send(error)
                return
            
            # get member discord object, need those for DM
            member = GetDiscordMemberObject(ctx.guild.members, newCollaboratorID)

            # prepare the zip file and send it to new collaborator in DM, 
            # then we will delete the zip and txt file, and notify command author
            PrepareCollaboratorWelcomePackage(member.name, pin)
            zipFile = discord.File('devWelcomePkg.zip')
            await member.send('{} Has added you as a collaborator for **MopBot**! Below is a zip file to get you started!'.format(ctx.message.author.mention), file=zipFile)
            os.remove('devWelcomePkg.zip')
            os.remove('./utils/PLEASE_READ')

            await ctx.send('{}, the welcome package was sent to {}!'.format(ctx.message.author.mention, GetMention(newCollaboratorID)))



        # GET OPTION
        #--------------------------------------
        if args[0].lower() == 'get':

            #ERROR CHECK - need to have exactly 3 args
            if len(args) != 3:
                error = ":x: **This command sequence requires exactly 3 arguments, `get` `hidden` `files`.**\n"
                error += "e.g. `.developer get hidden files`"
                await ctx.send('{}'.format(error))
                return

            #ERROR CHECK - second param should be 'hidden'
            if args[1].lower() != 'hidden':
                error = ":x: **argument '{}' not understood. Expected `hidden` in this position.**\n".format(args[1])
                error += "e.g. `.developer get hidden files`"
                await ctx.send('{}'.format(error))
                return                

            #ERROR CHECK - second param should be 'files'
            if args[2].lower() != 'files':
                error = ":x: **argument '{}' not understood. Expected `files` in this position.**\n".format(args[2])
                error += "e.g. `.developer get hidden files`"
                await ctx.send('{}'.format(error))
                return   

            # prepare the zip file and send it to collaborator in DM, 
            # then we will delete the zip
            message = await ctx.send('`preparing files...`')          

            PrepareHiddenFiles()
            zipFile = discord.File('hiddenfiles.zip')
            await ctx.message.author.send('Below is a zip file containing the requested hidden files from prod', file=zipFile)
            os.remove('hiddenfiles.zip')   
            await message.edit(content="**Complete!**\n `Files have been sent, check your DM'S` {}".format(ctx.message.author.mention))             



        #SET OPTION     
        #--------------------------------------
        if args[0].lower() == 'set':

            #ERROR CHECK - need to have exactly 3 args
            if len(args) != 2:
                error = ":x: **This command sequence requires exactly 2 arguments, `set` `pin`.**\n"
                error += "e.g. `.developer set pin 0000`"
                await ctx.send('{}'.format(error))
                return

            #ERROR CHECK - second param should be 'pin'
            if args[1].lower() != 'pin':
                error = ":x: **argument '{}' not understood. Expected `pin` in this position.**\n".format(args[1])
                error += "e.g. `.developer set pin`"
                await ctx.send('{}'.format(error))
                return                

            
            # dm collaborator, have them send you their desired new pin privately.
            await ctx.send('{}, I have sent you a DM with instructions on how to reset your pin, please speak with me there'.format(ctx.message.author.mention))
            dm = await ctx.message.author.send('Hello there.\nI am here to help you mop up that old pin, and set a new one.\n\n**What would you like your new pin to be?**')

            def checkUser(message):
                return (message.author == ctx.message.author) and (dm.channel.id == message.channel.id)

            pin = await self.bot.wait_for('message', timeout=180, check=checkUser)
            response = SetNewCollaboratorPin(pin.content, ctx.message.author.id)

            # if there was an error with the user input, send error and re-prompt collaborator for new pin.
            while response['error']:
                error = ":x:\nThere was an issue with the pin you provided '{}'. More information below:**\n".format(response['pin'])
                error += "\n`{}`\n".format(response['errorMessage'])
                error += "\n**Please try again. **What would you like your new pin to be?**"
                dm = await ctx.message.author.send(error)

                pin = await self.bot.wait_for('message', timeout=180, check=checkUser)
                response = SetNewCollaboratorPin(pin.content, ctx.message.author.id)

            #successful reset. delete current devsession, msg collaborator letting them know their changes have committed
            os.remove('devsession') 
            msg = '\n**Pin reset successful.**\nYour new pin will now be `{}`.\n\nI have removed your current "devsession" so the new pin '.format(response['pin'])
            msg += 'can take effect. Next time you run the program, you will need to manually authenticate with this new pin.'
            await  ctx.message.author.send(msg)


            # TIME RAN OUT        
            # except asyncio.TimeoutError:
            #     msg = '**[EXCEEDED TIME LIMIT] I cannot maintain a secure line of communication...**\n '
            #     msg += 'Closing this channel. Information was not saved... **Please try the command again in the public discord** ... **goodbye**\n[CLOSED]\n'
            #     await user.send(msg)    


# set the cog up
def setup(bot):
    bot.add_cog(DeveloperCog(bot))







