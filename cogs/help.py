import discord
from discord.ext import commands
from utils.db import GetCommandHelpInformation



class HelpCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def help(self, ctx, option):

        # if not option:
        #     result = GetCommandHelpInformation(option)

        legend  = "\n\n**LEGEND**\n"
        legend += "**×** **<<**param**>>** is a required param in its position.\n"
        legend += "**×** **<**param**>** is a required param, position optional\n"
        legend += "**×** **[[**param**]]** is an optional param in its position\n"
        legend += "**×** **[**param**]** is an optional param, position optional\n"
        legend += "**×** ***bold & italic*** words describe the unknwon param\n"
        legend += "**×**\U0001F512 command sequence requires specific permissions\n\n."

        result = GetCommandHelpInformation(option)
        embed=discord.Embed(title="", description=bytes(result[0][0], "utf-8").decode("unicode_escape")+legend, color=0xd9d326)
        embed.set_author(name="{} command".format(option), icon_url=self.bot.user.avatar_url)

        for value in result:
            embed.add_field(name=bytes(value[1], "utf-8").decode("unicode_escape"), value=bytes(value[2], "utf-8").decode("unicode_escape").replace("Ã", "×"), inline=False)
        await ctx.message.author.send(embed=embed)
        

# set the cog up
def setup(bot):
    bot.add_cog(HelpCog(bot))
