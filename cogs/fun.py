import discord, asyncio, json, random, math, os, aiohttp, time, datetime
from time import ctime
from discord.ext import commands
from discord.ext.commands import clean_content

with open("database/data.json") as file:
    config = json.load(file)

tickYes = config['tickyes']
tickNo = config['tickno']
reactno = config['ticknoreact']
reactyes = config['tickyesreact']

async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as jsonresp:
            return await jsonresp.json()

async def activitytype(activitytype):
    if str(activitytype) == "ActivityType.playing":
        return "Playing"
    elif str(activitytype) == "ActivityType.streaming":
        return "Streaming"
    elif str(activitytype) ==  "ActivityType.listening":
        return "Listening To"
    elif str(activitytype) == 'ActivityType.watching':
        return "Watching"
    else:
        pass

class FunCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx, *, choice):
        botChoice = random.choice(['rock', 'paper', 'scissors'])

        async def userWins():
            await ctx.send(f"I choose... **{botChoice}**.  You win! ***{choice} beats {botChoice}!***")

        async def botWins():
            await ctx.send(f"I choose... **{botChoice}**.  I win! ***{botChoice} beats {choice}!***")

        if choice == botChoice:
            await ctx.send(f"***Tie!***  We both used {botChoice}!")

        elif choice == "rock":
            if botChoice == "paper":
                await botWins()
            else:
                await userWins()
        elif choice == "paper":
            if botChoice == "scissors":
                await botWins()
            else:
                await userWins()    
        elif choice == "scissors":
            if botChoice == "paper":
                await userWins()
            else:
                await botWins()

    @commands.command()
    async def poll(self, ctx, * , PollMessage : str):
        embed = discord.Embed(color=ctx.author.color)
        embed.set_author(icon_url=ctx.author.avatar_url, name=f"Poll Made By {ctx.author}")
        embed.add_field(name="\uFEFF", value=PollMessage)
        pollmsg = await ctx.send(embed=embed)
        await ctx.message.delete()
        try:
            await pollmsg.add_reaction(emoji=reactyes)
            await pollmsg.add_reaction(emoji=reactno)
        except:
            await ctx.send("***Make Sure I have `add_reactions` so I can make the poll***")

    @commands.guild_only()
    @commands.command()
    async def perms(self, ctx, *, user : discord.Member=None):
        if not user:
            user = ctx.author
        permissions = '\n'.join(permission for permission, value in user.guild_permissions if value)
        embed = discord.Embed(color=user.color)
        embed.set_author(name=str(user))
        embed.add_field(name="\uFEFF", value=permissions)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(icon_url=ctx.guild.icon_url, text=ctx.guild)
        await ctx.send(embed=embed, content=None)
    

    @commands.group(aliases=['gh'])
    async def github(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(color=discord.Color(value=0x1c407a))
            embed.set_author(icon_url=config['urls']['transparentgithubimg'], name="GitHub Commands")
            embed.add_field(name="Search User", value="e.g `.github user <user>`", inline=False)
            embed.add_field(name="Search Repository", value="e.g `.github repo <owner/org>/<reponame>`", inline=False)
            embed.set_footer(text="GitHub Commands In Testing")
            await ctx.send(embed=embed)

    @github.command(aliases=['u'])
    async def user(self, ctx, *, githubacct):
        msg = await ctx.send("`Fetching Information..`")
        request = await get("https://api.github.com/users/" + githubacct)
        try:           
            embed = discord.Embed(description=f"{request['bio']}\uFEFF", color=discord.Color(value=0x1c407a))
            embed.set_author(name=f"{request['login']} ({request['name']})", url=request["html_url"])
            embed.set_thumbnail(url=request['avatar_url'])
            embed.add_field(name=f"\uFEFF", value=f"Followers: {request['followers']}\nFollowing: {request['following']}\nPublic Gists: {request['public_gists']}\nPublic Repos: {request['public_repos']}")
            await msg.edit(content=None, embed=embed)       
        except:
            await msg.edit(content=None, embed=discord.Embed(description=f"*** {tickNo}`{githubacct}` isn't a Valid Account, if So, Try Again Later***", color=discord.Color(value=0x1c407a)))

    @github.command(aliases=['repository'])
    async def repo(self, ctx, * , reqresult):
        request = await get(f"https://api.github.com/repos/{reqresult}")
        try:
            emb = discord.Embed(color=discord.Color(value=0x1c407a))
            emb.set_author(icon_url=config['urls']['transparentgithubimg'],name=f"{request['full_name']}", url=request['html_url'])
            emb.add_field(name="Description:", value=request['description'], inline=False)
            emb.add_field(name="Mostly Used Language:", value=request['language'], inline=False)
            emb.add_field(name="Stargazers:", value=request['stargazers_count'], inline=False)
            emb.add_field(name="Forks:", value=request['forks_count'], inline=False)
            emb.add_field(name="Watching:", value=request['watchers_count'], inline=False)
            await ctx.send(embed=emb)
        except:
            await ctx.send(embed=discord.Embed(description=f"***{tickNo} `{reqresult}` isn't a Valid Repo, if So, Try Again Later***", color=discord.Color(value=0x1c407a)))

    @commands.command()
    async def userinfo(self, ctx, * , user : discord.Member=None):
        if user is None:
            user = ctx.author
        joined_server = user.joined_at.strftime("%B %e, %Y %I:%M%p")
        joined_discord = user.created_at.strftime("%B %e, %Y %I:%M%p")
        server_stay_length = (ctx.message.created_at - user.joined_at).days
        created_account_length = (ctx.message.created_at - user.created_at).days
        if user.id == self.bot.owner_id:
            username = f"{user} (My Owner)"
        elif user.bot:
            username = f"{user} (Bot)"
        else:
            username = user
        if len(user.roles) > 1:
            roles = '\n'.join(list(reversed(sorted([a.name for a in user.roles if a.name != "@everyone"]))))
        else:
            roles = "None"
        
        try:
            authoracttype = await activitytype(user.activity.type)
            activity = f"{authoracttype} {user.activity.name}"
        except:
            activity = f"{user.name} isn't playing anything"
           
        embed = discord.Embed(description=activity, color=discord.Color(value=0xBD5BFF))
        if user.nick:
            embed.set_author(name=f"{username} ({user.nick})")
        else:
            embed.set_author(name=username)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined Server", value=f"{joined_server}, {server_stay_length} Days ago", inline=False)
        embed.add_field(name="Joined Discord", value=f"{joined_discord}, {created_account_length} Days ago", inline=False)
        embed.add_field(name="Roles", value=roles)
        embed.set_footer(text=f"User ID: {user.id}")
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(FunCommands(bot))