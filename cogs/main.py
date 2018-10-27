import discord, asyncio, json, time, datetime 
from time import ctime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

with open('database/data.json') as file:
    config = json.load(file)

class MainCommands:
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        with open("database/uptime.json", "w+") as file:
            json.dump({"uptimestats" : str(datetime.datetime.utcnow())}, file)
        print("Posted Uptime")

    @commands.command()
    async def help(self, ctx):
        if not ctx.guild:
            return await ctx.send("**Here's my website**\nhttps://enternewname.me/nebula/commands")
        else:
            try:
                await ctx.author.send("**Here's my website**\nhttps://enternewname.me/nebula/commands")
                await ctx.send("***Check Your DMs For Help***")
            except:
                await ctx.send("**Here's my website**\nhttps://enternewname.me/nebula/commands")

    @commands.command()
    async def prefix(self, ctx):
        await ctx.send("My Prefix is `.` and Cannot Be Changed")
        
    @commands.cooldown(1, 20, BucketType.channel)
    @commands.command()
    async def ping(self, ctx):
        counter = 0
        msg = await ctx.send("`Pinging 0/4...`")
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=discord.Color(value=0xBD5BFF))
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        average = []
        for _ in range(4):
            counter += 1
            ping1 = time.perf_counter()
            await msg.edit(content=f"`Pinging {counter}/4...`")
            ping2 = time.perf_counter()
            result = round((ping2 - ping1) * 1000)
            embed.add_field(name=f"Ping {counter}", value=f"{result}ms")
            average.append(result)
        embed.add_field(name="Bot Latency:", value=f"{round(self.bot.latency* 1000)}ms")
        embed.add_field(name="Ping Average:", value=f"{round(sum(average) / 4)}ms")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
        await msg.edit(content=None, embed=embed)

    @commands.command(aliases=['server'])
    async def support(self, ctx):
        if not ctx.guild:
            return await ctx.send("**Here's My Support Server**\nhttps://links.enternewname.me/server")
        else:
            try:
                await ctx.author.send("**Here's My Support Server**\nhttps://links.enternewname.me/server")
                await ctx.send("***:mailbox_with_mail: Check DMs For Official Support Server***")
            except:
                await ctx.send("Here's My Support Server\nhttps://links.enternewname.me/server")
            
    @commands.command()
    async def invite(self, ctx):
        if not ctx.guild:
            return await ctx.send("**Here's my invite**\nhttps://links.enternewname.me/nebula")
        else:
            try:
                await ctx.author.send("**Here's my invite**\nhttps://links.enternewname.me/nebula")
                await ctx.send("***:mailbox_with_mail: Check DMs For The Invite Link***")
            except:
                await ctx.send("**Here's my invite**\nhttps://links.enternewname.me/nebula")

    @commands.guild_only()
    @commands.command()
    async def feedback(self, ctx, *, body : str):
        try:
            feedback = self.bot.get_channel(490608601950322702)
            embed = discord.Embed(color=discord.Color(value=0xBD5BF))
            embed.set_author(name="Feedback")
            embed.add_field(name="Guild ID And Name: ", value=f"ID: {ctx.guild.id}, Name: {ctx.guild}", inline=False)
            embed.add_field(name="User", value=f"Name: {ctx.author}, ID: {ctx.author.id}", inline=False)
            embed.add_field(name="Channel ID And Name", value=f"ID: {ctx.channel.id}, Name: #{ctx.channel}", inline=False)
            embed.add_field(name="Response: ", value=body, inline=True)
            await feedback.send(embed=embed)
            await ctx.send("**Your Response Has Been Sent, You Might Recieve A Response Later On**")
        except Exception as e:
            await ctx.send(f"***Your Feedback Could Not Be Sent {config['tickno']}, Notifying Owner***")
            owner = self.bot.get_user(373256462211874836)
            await owner.send(f"{owner}, We Have A Problem With The Feedback Command,\nAuthor Profile: {ctx.author.id}\nName: {ctx.author}\nHeres The Error:\n```fix\n{e}\n```")

    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    @commands.command(aliases=['a'])
    async def annouce(self, ctx, channel : discord.TextChannel, * ,body : str):
        embed = discord.Embed(color=ctx.author.color)
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author)
        embed.add_field(name="Update:\n\n", value=body)
        await channel.send(embed=embed)
        try:
            await ctx.message.delete()
        except:
            pass

    @commands.command()
    async def uptime(self, ctx):
        file = open('database/uptime.json', "r")
        time = json.load(file)['uptimestats']
        uptimeraw = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        uptime = datetime.datetime.utcnow() - uptimeraw
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"I've been on for **{days}** days, **{hours}** hours, **{minutes}** minutes, **{seconds}** seconds")

def setup(bot):
    bot.add_cog(MainCommands(bot))