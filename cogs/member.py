import discord
from discord.ext import commands
import sys, asyncio
from utils.db import RegisterMember, GetMember, GetMembers, UpdateMemberStatus
from utils.functions import GetQueryValues, GetMemberListRow
import math as m
from contextlib import suppress



configFile = open('config')
configs = configFile.readlines()
config = {
    'OWNER': {
        'ids': configs[3].split()[1].split('\n')[0].split(',')
    }
}


class MemberCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.next = '\N{BLACK RIGHTWARDS ARROW}'
        self.prev = '\N{LEFTWARDS BLACK ARROW}'


    @commands.command()
    async def member(self, ctx, *args):

        # variables for below
        pageMax = 15
        idx = 0
        page = 1
        information =  '\n*Below is a list of members that match your query.*\n'
        information += '- ***Username*** *will show* ***nickname*** *if one exists*\n'
        information += '- ***Date*** *represents the last Active status change*\n'
        information += '- :slight_smile: *is an* ***Active*** *user*\n'
        information += '- :sob: *is an* ***Inactive*** *user*\n\n'
        header = r'**__Username__\_\_\_\_\_\_\_\_\_\___Active__\_\_\_\_\___Date__**' + '\n'


        #ERROR CHECK - dm bot commands not allowed
        try:
            ctx.guild.id # if no guild id then this is a dm
        except:
            error = "**You cannot run bot commands in a DM** "
            error += "Please retry your command in a bot friendly channel in your server where I reside."
            await ctx.message.author.send('{}'.format(error))
            return

        # function to check that reaction is from user who called this command
        def checkUser(reaction, user):
            return user == ctx.message.author




        # get a n object of queryables. None value for missing
        # {username, userID, active, statusChange, userNickname, gamertag, sortByParam}
        result = GetQueryValues(args)

        # we have our query now set out footer and get our results
        footer = 'Params: '
        noParams = True
        for key in result['query']:
            if result['query'][key] != None:
                noParams = False
                footer += '{}:{}, '.format(key, result['query'][key])
        footer += 'None ' if noParams else ''
        members = GetMembers(result['query'])

        # no fancy embed needed, just display this members info in an embed
        if len(members) == 1:
            member = members[0]
            date = member[2].split('T')[0].split('-')
            description = '**Status**: {}\n**Username**: {}\n**Nickname**: {}\n**Gamertag**: {}\n**Last Status Change**: {}'.format(
                ':slight_smile:' if member[4] else ':sob:',
                member[0],
                member[5],
                member[3],
                '{}/{}/{}`\n'.format(date[1], date[2], date[0][2::])
            )
            embed = discord.Embed(description=description, color=000000)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_author(name=member[5] if member[5] else member[0])
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
            return


        # now that you have results, determine the actual number of pages we need to show (MAX PER PAGE = pageMax)
        pages = m.ceil(len(members) / pageMax)

        # finally, determine how many results to show on the upcoming embed page
        pageEnd = pageMax if len(members) >= pageMax else len(members)



        firstPass = True
        try:
            while True:

                # loop through results and format them in a user friendly way. 
                memberList = ''
                for i in range(idx, pageEnd):
                    memberList += GetMemberListRow(members[i])


                # prepare the embed
                embed = discord.Embed(title='**REDACTED Members**', description=information + header + memberList, color=000000)
                embed.set_footer(text=footer + ' | page: {}/{}'.format(page, pages))
                if firstPass:
                    msg = await ctx.send(embed=embed)
                else:
                    await msg.edit(embed=embed)

                # first pass complete, set this to false here on after
                firstPass = False

                # determine which emojis to add to interface, based on page number and current filters
                if page > 1:
                    await msg.add_reaction(emoji=self.prev)
                if page * pageMax < len(members):
                    await msg.add_reaction(emoji=self.next)

                # also add help icon
                await msg.add_reaction(emoji='❓')
                
                # we listen or "wait for" the user to do something with the embed reactions
                task_1 = asyncio.ensure_future(self.bot.wait_for('reaction_add', timeout=60.0, check=checkUser))
                task_2 = asyncio.ensure_future(self.bot.wait_for('reaction_remove', timeout=60.0, check=checkUser))

                # Wait for first of them done:
                tasks = (task_1, task_2)
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                reaction, user = done.pop().result()

                # Cancel others since they're still running, 
                # but we don't need them to be finished:
                for task in pending:
                    task.cancel()
                    with suppress(asyncio.CancelledError):
                        await task

                # page the results forward, reset page number, page end, and the index
                if reaction.emoji == self.next:
                    page += 1
                    idx = pageEnd
                    pageEnd = (page * pageMax) if len(members) >= (page * pageMax) else len(members)

                # page the results backwards, reset page number, page end, and the index
                elif reaction.emoji == self.prev:
                    page -= 1
                    pageEnd = idx
                    idx = pageEnd - pageMax


                # HELP EMOJI SELECTED
                # Show a new custom emoji with directions on how to use the interface. Stay on page until
                # the return emoji is selected
                elif reaction.emoji == '❓':
                    # prepare the embed
                    await msg.clear_reactions()
                    help = '**MEMBER COMMAND HELP**\n\n Currently a blank state'
                    embed = discord.Embed(title='**REDACTED Members**', description=help, color=000000)
                    embed.set_footer(text='MEMBERS HELP MENU | Select {} to return'.format('❌'))
                    await msg.edit(embed=embed)
                    await msg.add_reaction(emoji='❌')
                    while True:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=checkUser)
                        if reaction.emoji == '❌':
                            break
                        else:
                            await msg.remove_reaction(emoji=reaction.emoji, member=user)

                # remove any reactions the user may have added that arent specifically mentioned aboce
                else:
                    await msg.remove_reaction(emoji=reaction.emoji, member=user)
                
                # clear ALL reactions, reset state of interface.
                await msg.clear_reactions()

        # TIMES UP. Avoid error and clear all reactions. Give message in footer to rep state
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            footer = 'TRANSMISSION CLOSED -- SESSION ENDED'
            embed = discord.Embed(title='**REDACTED Members**', description=information + header + memberList, color=000000)
            embed.set_footer(text=footer + ' | page: {}/{}'.format(page, pages))
            await msg.edit(embed=embed)






# set the cog up
def setup(bot):
    bot.add_cog(MemberCog(bot))







