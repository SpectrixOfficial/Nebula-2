import discord, asyncio, datetime, json
from discord.ext import commands

with open('database/data.json') as file:
    config = json.load(file)

class Support:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        try:
            return ctx.guild.id == 490591987477643264
        except:
            return

    @commands.guild_only()
    @commands.command()
    async def reportbug(self, ctx, *, bug: str=None):
        if not bug:
            try:
                await ctx.author.send("You Need To Specify What the Bug is...\n\nExample:\n`.reportbug the kick command isnt working`")
            except:
                pass
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=discord.Color.red(), title=f"New Bug Report From {ctx.author.name} | ({ctx.author.id})")
        embed.add_field(name="Bug Report Complaint:", value='\n' + bug)
        await self.bot.get_channel(495417184877674499).send(embed=embed)
        if ctx.channel.id != 495417184877674499:
            await ctx.send(f"***{config['tickyes']} Your Report Has Been Successfully Sent***")
        else:
            await ctx.author.send(f"***{config['tickyes']} Your Report Has Been Successfully Sent***")

    @commands.guild_only() 
    @commands.command()
    async def suggest(self, ctx, * , suggestion : str=None):
        if not suggestion:
            try:
                await ctx.author.send("You Need To Specify What To Suggest...\n\nExample:\n`.suggest add a fn cmd`")
            except:
                pass
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=discord.Color.green(), title=f"New Suggestion From {ctx.author.name} | ({ctx.author.id})")
        embed.add_field(name="Suggestion", value='\n' + suggestion)
        await self.bot.get_channel(495417184877674499).send(embed=embed)
        if ctx.channel.id != 495417184877674499:
            await ctx.send(f"***{config['tickyes']} Your Suggestion Has Been Successfully Sent***")
        else:
            try:
                await ctx.author.send(f"***{config['tickyes']} Your Suggestion Has Been Successfully Sent***")
            except:
                pass

def setup(bot):
    bot.add_cog(Support(bot))