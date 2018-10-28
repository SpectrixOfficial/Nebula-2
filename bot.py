import discord, asyncio, json, pkg_resources, time, datetime, aiohttp, sys
from discord.ext import commands
from time import ctime

with open("database/data.json") as f:
    config = json.load(f)

class Nebula_Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(config['prefix']),
                         case_insensitive=True,
                         owner_id=373256462211874836)

    async def presencehandler(self):
        if config['is_on_dbl'] is True:
            header = {"Authorization" : config["dbltoken"]}
            payload = {"server_count"  : len(self.guilds)}
            async with aiohttp.ClientSession() as session:
                await session.post("https://discordbots.org/bot/" + self.user.id + "/stats",
                                   data=payload, 
                                   headers=header)
                
        await self.change_presence(
            activity=discord.Activity(
                name=f".help in {len(self.guilds)} Servers!",
                url="https://www.twitch.tv/EnterNewName",
                type=1))

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
            embed.add_field(name="Other Requirements:", value="Make Sure I have `external_emojis` so i can use my emojis\n\
                                                               from my [Support Server](https://links.enternewname.me/server)")
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
            print("\nConnecting To The API")
            super().run(config["bottoken"])
        except Exception as e:
            print(f"Internal Error While Booting Bot:\n\n{e}\n")

if __name__ == "__main__":
    Nebula_Bot().intiate_startup()
