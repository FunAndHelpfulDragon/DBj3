import discord
import aiofiles
from discord.ext import commands
from discord.ext.commands import has_permissions
from os import path
import os


class Admins(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Admin cog loading")

    @commands.command(
        help="Add a user as an bot admin.",
        usage="Ping a member as well to add them as admin",
        aliases=["addadmin", "AddAdmin", "MkAdmin", "mkadmin"]
    )
    async def addAdmin(self, ctx, member: discord.Member):
        if path.exists(f"Files/{ctx.guild.id}/Admins.txt"):
            async with aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt", 'r') as r, aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt", 'a') as w:  # noqa
                lines = await r.read()
                lines = lines.split(",")
                added = False
                for line in lines:
                    if line.strip() == str(ctx.author.mention) or ctx.author == ctx.guild.owner:  # check if the author of the message is in there.  # noqa
                        if line == (str(member.mention)):
                            await ctx.send(f"{member.mention} is already a trusted admin")  # noqa
                            added = True
                        else:
                            await w.write(str(member.mention) + ",")
                            await ctx.send(f"Added {member.mention} as an admin")  # noqa
                            added = True
                        break
                if not added:
                    await ctx.send(f"{ctx.author.mention}! You are not a trusted admin")  # noqa
        else:
            await ctx.send("File not found! please reinvite me or ping my owner")  # noqa

    @commands.command(
        help="Remove a user as an bot admin",
        usage="Ping a member as well to remove them as admin",
        aliases=["RemoveAdmin", "removeadmin", "RmAdmin", "rmadmin"]
    )
    async def removeAdmin(self, ctx, member: discord.Member):
        if path.exists(f"Files/{ctx.guild.id}/Admins.txt"):
            async with aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt") as r:
                lines = await r.read()
                lines = lines.split(",")
                x = 0
                remove = False
                for line in lines:
                    if line.strip() == str(ctx.author.mention):
                        remove = True
                    if line.strip() == str(member.mention):
                        break
                    x = x + 1
                if ctx.author == ctx.guild.owner:
                    remove = True
                if remove:
                    lines[x] = ""
                    async with aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt", 'w') as w:  # noqa
                        writeLine = ""
                        for line in lines:
                            if line != "":
                                writeLine = writeLine + line.strip() + ","
                        await w.write(writeLine)

                        await ctx.send(f"Removed {member.mention} from Admins.txt")  # noqa
                else:
                    await ctx.send(f"{ctx.author.mention}! You are not a trusted admin")  # noqa
        else:
            await ctx.send("File not found! please reinvite me or ping my owner")  # noqa

    @commands.command(
        help="Lists all admins in file",
        usage="",
        aliases=["listadmins", "ListAdmins", "Admins", "admins"]
    )
    async def listAdmins(self, ctx):
        embed = discord.Embed()
        async with aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt") as f:
            line = await f.read()
            embed.add_field(
                name="Bot Admin",
                value=line,
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(
        help="Setup the admin.txt file",
        usage="",
        aliases=["setup"]
    )
    async def Setup(self, ctx):
        os.system(f"mkdir Files/{ctx.guild.id}")
        async with aiofiles.open(f"Files/{guild.id}/Admins.txt", 'w') as w:  # noqa
            await w.write(str(ctx.guild.owner.mention) + ",")

    @addAdmin.error
    async def addAdmin_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing argument: {error.param}")
        else:
            await ctx.send(f"Error: {error}")

    @removeAdmin.error
    async def removeAdmin_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing argument: {error.param}")
        else:
            await ctx.send(f"Error: {error}")


def setup(client):
    print("setup?")
    client.add_cog(Admins(client))
