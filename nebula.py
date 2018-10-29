import discord, asyncio
import json
import pkg_resources 
import time 
import datetime 
import aiohttp 
import sys
import asyncpg
from discord.ext import commands
from time import ctime

with open("database/data.json") as f:
    config = json.load(f)

class Nebula_Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(config['prefix']), case_insensitive=True, owner_id=373256462211874836)

    async def presencehandler(self):
        try:
            await self.change_presence(activity=discord.Activity(name=f".help in {len(self.guilds)} Servers!", url="https://www.twitch.tv/EnterNewName",type=1))
            # bot listing server count updates
            async with aiohttp.ClientSession() as session:
                dblheader = {"Authorization" : config["dbltoken"]}
                dblpayload = {"server_count"  : len(self.guilds)}
                dblurl = "https://discordbots.org/api/bots/" + str(self.user.id) + "/stats"
                await session.post(dblurl, data=dblpayload, headers=dblheader)
                dbgheader = {"Authorization" : config['dbgtoken']}
                dbgpayload = {'count' : len(self.guilds)}
                dbgurl ="https://discordbots.group/api/bot/" + str(self.user.id)
                await session.post(dbgurl, data=dbgpayload, headers=dbgheader)
            print("Posted Server Count")
        except Exception as e:
            print(e)

    async def db(self):
        print("Performing")
        credentials =  {"user" : config['dbuser'], "password" : config['dbpw'], "database" : config['dbname'], "host": "127.0.0.1"}
        return await asyncpg.create_pool(**credentials)

    async def on_guild_remove(self, guild):
        await self.presencehandler()

    async def on_ready(self):
        await self.presencehandler()
        print("Bot Is Successfully Connected")
        print("Discord.py Version : {}".format(pkg_resources.get_distribution("discord.py").version))
        print(f"{self.user} Is Online")
        print(f"Guild Count : {len(self.guilds)}\n")

    async def on_guild_join(self, guild):
        await self.presencehandler()         
        try:
            embed = discord.Embed(color=discord.Color(value=0x1c407a))
            embed.set_author(name="Thanks For Inviting Nebula")
            embed.add_field(name="My Prefix is `.`", value=f"[Support](https://links.enternewname.me/nebula)", inline=False)
            embed.add_field(name="Need Help?", value="[Click here](https://enternewname.me/nebula/commands)", inline=False)
            embed.add_field(name="Logging Channel Requirement", value="***#mod-log***", inline=False)
            embed.set_footer(text=f"Thanks to you, I am now on {len(self.guilds)} servers, HYPE!", icon_url=self.user.avatar_url)
            await guild.system_channel.send(embed=embed)
        except:
            pass
           

    def intiate_startup(self):
        self.remove_command('help')
        cogs = config["cogs"]
        try:
            for module in cogs:
                self.load_extension(module)
                print(f"\nLoading Extension {module}")
            print("\nConnecting To The API\n")
            super().run(config["bottoken"])
        except Exception as e:
            print(f"\nInternal Error While Booting Bot:\n\n{e}\n")

if __name__ == "__main__":
    Nebula_Bot().intiate_startup()
