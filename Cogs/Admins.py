import discord
from discord.ext import commands
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../Class"))
import FileReading  # noqa


class Admins(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Admin cog loading")
        self.File = FileReading.File()

    @commands.command(
        help="Add a user as an bot admin.",
        usage="Ping a member as well to add them as admin",
        aliases=["addadmin", "AddAdmin", "MkAdmin", "mkadmin"]
    )
    async def addAdmin(self, ctx, member: discord.Member):
        if self.File.CheckForFile(f"Files/{ctx.guild.id}/Admins.txt"):
            if await self.File.CheckForAdmin(f"Files/{ctx.guild.id}/Admins.txt", ctx.author.mention) or ctx.author == ctx.guild.owner:  # noqa
                if await self.File.CheckForAdmin(f"Files/{ctx.guild.id}/Admins.txt", member.mention):  # noqa
                    await ctx.reply(f"{member.mention} is already a trusted admin")  # noqa
                else:
                    await self.File.AppendFile(f"Files/{ctx.guild.id}/Admins.txt", str(member.mention) + ",")  # noqa
                    await ctx.reply(f"Added {member.mention} as an admin")  # noqa
            else:
                await ctx.reply(f"{ctx.author.mention}! You are not a trusted admin")  # noqa
        else:
            self.File.MakeFile(f"Files/{ctx.guild.id}/Admins.txt", str(ctx.guild.owner.mention) + ",")  # noqa

    @commands.command(
        help="Remove a user as an bot admin",
        usage="Ping a member as well to remove them as admin",
        aliases=["RemoveAdmin", "removeadmin", "RmAdmin", "rmadmin"]
    )
    async def removeAdmin(self, ctx, member: discord.Member):
        if self.File.CheckForFile(f"Files/{ctx.guild.id}/Admins.txt"):
            if await self.File.CheckForAdmin(f"Files/{ctx.guild.id}/Admins.txt", ctx.author.mention) or ctx.author.mention == ctx.guild.owner:  # noqa
                Pos = await self.File.GetPositionInFile(f"Files/{ctx.guild.id}/Admins.txt", member.mention)  # noqa
                list = self.File.RemoveValueFromList(await self.File.GetList(f"Files/{ctx.guild.id}/Admins.txt"), Pos)  # noqa
                string = self.File.MakeListString(list)
                await self.File.WriteFile(f"Files/{ctx.guild.id}/Admins.txt", string)  # noqa
                await ctx.reply(f"Removed {member.mention} as an admin")
            else:
                await ctx.reply(f"{ctx.author.mention}! You are not a trusted admin")  # noqa
        else:
            await ctx.reply("File not found! please reinvite me or ping my owner")  # noqa

    @commands.command(
        help="Lists all admins in file",
        usage="",
        aliases=["listadmins", "ListAdmins", "Admins", "admins"]
    )
    async def listAdmins(self, ctx):
        if self.File.CheckForFile(f"Files/{ctx.guild.id}/Admins.txt"):
            embed = discord.Embed()
            embed.add_field(
                name="Bot Admin",
                value=await self.File.ReadFile(f"Files/{ctx.guild.id}/Admins.txt"),  # noqa
                inline=False
            )
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("No admins file. Please setup using the `AdminSetup` command")  # noqa

    @commands.command(
        help="Setup the admin.txt file",
        usage="",
        aliases=["adminsetup", "adsetup", "AdminSetup", "AdSetup"]
    )
    async def Adminsetup(self, ctx):
        if ctx.author == ctx.guild.owner:
            self.File.MakeFile(f"Files/{ctx.guild.id}", "Admins.txt", str(ctx.guild.owner.mention) + ",")  # noqa
            await ctx.reply("Setup completed for admin stuff.")
        else:
            await ctx.reply("Only the owner of the server can run this command")

    @addAdmin.error
    async def addAdmin_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Missing argument: {error.param}")
        else:
            await ctx.reply(f"Error: {error}")

    @removeAdmin.error
    async def removeAdmin_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Missing argument: {error.param}")
        else:
            await ctx.reply(f"Error: {error}")


def setup(client):
    client.add_cog(Admins(client))
