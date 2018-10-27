import discord, asyncio, time, datetime
from time import ctime
from discord.ext import commands

class UserManagement:
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(ban_members=True)   
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(aliases=['b'])
    async def ban(self, ctx, user : discord.Member, *, banReason=None):
        if ctx.author.id == 373256462211874836 or ctx.author == ctx.guild.owner or ctx.author.top_role > user.top_role:
            await user.ban(reason=banReason)
            if not banReason:
                await ctx.send(f"**<:tickYes:490607182010777620> I have banned {user} from the server**")
            else:
                await ctx.send(f"**<:tickYes:490607182010777620> I have banned {user} from the server because: {banReason}**")
            embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=discord.Color(value=0xBD5BFF))
            embed.set_author(name=f"Moderator Action: {ctx.command}")
            embed.add_field(name="Moderator: ", value=ctx.author, inline=False)
            embed.add_field(name="Accused User", value=user, inline=False)
            embed.add_field(name="Reason: ", value=banReason, inline=False)
            embed.set_footer(text=f"Moderator ID: {ctx.author.id}")
            modlog = discord.utils.get(ctx.guild.text_channels, name="mod-log")
            await modlog.send(embed=embed)

    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.command(aliases=['k'])
    async def kick(self, ctx, user : discord.Member, * ,kickReason=None):
        if ctx.author.id == 373256462211874836 or ctx.author == ctx.guild.owner or ctx.author.top_role > user.top_role:
            await user.kick(reason=kickReason)
            if not kickReason:
                await ctx.send(f"**<:tickYes:490607182010777620> I have kicked {user} from the server**")
            else:
                await ctx.send(f"**<:tickYes:490607182010777620> I have kicked {user} from the server because: {kickReason}**")
            try:
                embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=discord.Color(value=0xBD5BFF))
                embed.set_author(name=f"Moderator Action: {ctx.command}")
                embed.add_field(name="Moderator: ", value=ctx.author, inline=False)
                embed.add_field(name="Accused User", value=user, inline=False)
                embed.add_field(name="Reason: ", value=kickReason, inline=False)
                embed.set_footer(text=f"Moderator ID: {ctx.author.id}")
                modlog = discord.utils.get(ctx.guild.text_channels, name="mod-log")
                await modlog.send(embed=embed)
            except:
                pass
    @commands.has_permissions(ban_members=True, kick_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(aliases=['sb'])
    async def softban(self, ctx, user : discord.Member, *, softbanReason=None):
        if ctx.author.id == 373256462211874836 or ctx.author == ctx.guild.owner or ctx.author.top_role > user.top_role:
            await user.ban(reason=softbanReason)
            await user.unban()
            if not softbanReason:
                await ctx.send(f"**<:tickYes:490607182010777620> I have softbanned {user} from the server**")
            else:
                await ctx.send(f"**<:tickYes:490607182010777620> I have softbanned {user} from the server because: {softbanReason}**")
            try:
                embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=discord.Color(value=0xBD5BFF))
                embed.set_author(name=f"Moderator Action: {ctx.command}")
                embed.add_field(name="Moderator: ", value=ctx.author, inline=False)
                embed.add_field(name="Accused User", value=user, inline=False)
                embed.add_field(name="Reason: ", value=softbanReason, inline=False)
                embed.set_footer(text=f"Moderator ID: {ctx.author.id}")
                modlog = discord.utils.get(ctx.guild.text_channels, name="mod-log")
                await modlog.send(embed=embed)   
            except:
                pass

def setup(bot):
    bot.add_cog(UserManagement(bot))