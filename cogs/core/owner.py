import discord, asyncio, json, time, io, traceback, inspect, textwrap, datetime, os, sys
from time import ctime
from contextlib import redirect_stdout
from discord.ext import commands

with open("database/data.json") as f:
    config = json.load(f)

class Developers:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, message):
        if message.startswith('```') and message.startswith("```"):
            return "\n".join(message.split('\n')[1:-1])
        return message.strip(' \n')
    
    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(hidden=True)
    async def eval(self, ctx, *, body : str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}```')
            try:
                await ctx.message.add_reaction(config['ticknoreact'])
            except:
                pass
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction(config['tickyesreact'])
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command()
    async def bash(self, ctx, * , cmd : str):
        import subprocess
        process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.stdout.decode('utf-8') == '':
            return
        await ctx.send(f"```bash\n{process.stdout.decode('utf-8')}\n```")


    @commands.command(aliases=['rl'])
    async def reload(self, ctx, cog=None):
        cogs = config['cogs']
        if not cog:
            try:
                for module in cogs:
                    self.bot.unload_extension(module)
                    self.bot.load_extension(module)
                return await ctx.send(embed=discord.Embed(color=discord.Color.green(), description=f"Successfully Reloaded {len(cogs)} Cogs {config['tickyes']}"))            
            except Exception as e:
                return await ctx.send(embed=discord.Embed(description=f"Could Not Reload {len(module)} Cogs {config['tickno']}\n```bash\n{e}\n```", color=discord.Color.red()))

        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(embed=discord.Embed(color=discord.Color.green(), description=f"Successfully Reloaded `cogs.{cog}` {config['tickyes']}"))            
        except Exception as e:
            await ctx.send(embed=discord.Embed(description=f"Could Not Reload `cogs.{cog}` {config['tickno']}\n```bash\n{e}\n```", color=discord.Color.red()))

    
    @commands.command(aliases=['l'])
    async def load(self, ctx, cog):
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(embed=discord.Embed(description=f"Loaded Extension `cogs.{cog}` {config['tickyes']}", color=discord.Color.green()))
        except Exception as e:
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=f"Could Not Load Extension: `cogs.{cog}` {config['tickno']}\n```fix\n{e}\n```"))

    @commands.command(aliases=['ul'])
    async def unload(self, ctx, cog):
        self.bot.unload_extension(f"cogs.{cog}")
        await ctx.send(embed=discord.Embed(description=f"Unloaded Extension `cogs.{cog}` <:tickYes:490607182010777620>"))

    @commands.group(invoke_without_command=True)
    async def dt(self, ctx):
        await ctx.send("Developer Tools For Use Of the Bot In General")

    @dt.command(aliases=['p'])
    async def presence(self, ctx, typ : int, *, presencegame=None):
        if presencegame is None:
            await self.bot.change_presence(activity=discord.Activity(name=f".help in {len(self.bot.guilds)} Servers", url="https://www.twitch.tv/Enter%20New%20Name", type=1))
            await ctx.send(f"Changed Presence to `Default Presence`")
        else:
            await self.bot.change_presence(activity=discord.Activity(name=f"{presencegame} | {len(self.bot.guilds)} Guilds!", type=typ, url="https://www.twitch.tv/Enter%20New%20Name"))
            if typ == 0:
                typtype = "Playing"
            elif typ == 1:
                typtype = "Streaming"
            elif typ == 2:
                typtype = "Listening to"
            elif typ == 3:
                typtype = "Watching"
            else:
                typtype = "Unknown Type"
            await ctx.send(f"Changed Presence To `{typtype}` | `{typ}`\nGame Status: `{presencegame} | {len(self.bot.guilds)} Guilds!`")

    @dt.command(aliases=['logout'])
    async def logoff(self, ctx):
        await ctx.send("Logged Out")
        sys.exit(0)
        await self.bot.logout()

    @commands.command()
    async def send(self, ctx, user : discord.User, *, body : str):
        await user.send(body)
        await ctx.message.add_reaction(str(config['tickyesreact']))
        await asyncio.sleep(.125)
        try:
            await ctx.message.delete()
        except:
            pass

    @commands.command()
    async def test(self, ctx):
        embed = discord.Embed(color=discord.Color(value=0x1c407a))
        embed.set_author(name="Thanks For Inviting Nebula")
        embed.add_field(name="My Prefix is `.`", value=f"[Support](https://enternewname.me/redirects/support)", inline=False)
        embed.add_field(name="Need Help?", value="[Click here](https://enternewname.me/nebula/commands)", inline=False)
        embed.add_field(name="Logging Channel Requirement", value="***#mod-log***", inline=False)
        embed.add_field(name="Other Requirements:", value="Make Sure I have `external_emojis` so i can use my emojis\nfrom my [Support Server](https://enternewname.me/redirects/support)")
        await ctx.guild.system_channel.send(embed=embed)    
        
def setup(bot):
    bot.add_cog(Developers(bot))