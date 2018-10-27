import discord, asyncio, logging, time, datetime, json
from discord.ext import commands

with open('database/data.json') as file:
    config = json.load(file)

class MessageManagement:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=["purge", "c"])
    async def clear(self, ctx, *, number : int):
        msg = "message"
        if number > 1000:
            number = 1000
        if number > 1:
          msg += 's'
        num = await ctx.channel.purge(limit=(number + 1))
        await asyncio.sleep(.7)
        await ctx.send(f"**Deleted `{len(num) - 1}` {msg} {config['tickyes']}**", delete_after=1)

    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['slowmo'])
    async def slowmode(self, ctx, seconds: int=0):
        if seconds > 120:
            return await ctx.send(f"*{config['tickno']} Slowmode Rate Cannot Be Over 120 Seconds*")
        if seconds == 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(f"**Slowmode is off for this channel! {config['tickyes']}**")
        else:
            numofmessages = "second"
            if seconds > 1:
                numofmessages+='s'

            await ctx.channel.edit(slowmode_delay=(seconds))
            await ctx.send(f"**Channel is On Slowmode for `{seconds}` {numofmessages} {config['tickyes']}\nTo Turn Off, Just Do `.slowmode`**")

    @commands.is_owner()
    @commands.command()
    async def say(self, ctx, * , body :str):
        await ctx.message.delete()
        await ctx.send(body)

def setup(bot):
    bot.add_cog(MessageManagement(bot))