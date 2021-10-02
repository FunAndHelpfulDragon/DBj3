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
        usage="Ping a member as well to add them as admin"
    )
    async def addAdmin(self, ctx, member: discord.Member):
        if path.exists(f"Files/{ctx.guild.id}/Admins.txt"):
            async with aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt", 'r') as r, aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt", 'a') as w:  # noqa
                lines = await r.readlines()
                added = False
                for line in lines:
                    if line.strip() == str(ctx.author.mention):  # check if the author of the message is in there.  # noqa
                        if line.strip() == (str(member.mention)):
                            await ctx.send(f"{member.mention} is already a trusted admin")  # noqa
                            added = True
                        else:
                            await w.write(str(member.mention)+"\n")
                            await ctx.send(f"Added {member.mention} as an admin")  # noqa
                            added = True
                        break
                if not added:
                    await ctx.send(f"{ctx.author.mention}! You are not a trusted admin")  # noqa
        else:
            async with aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt", 'a') as a:  # noqa
                await a.write(str(ctx.guild.owner.mention))
                await ctx.send("Made Admins.txt file")
                if member.mention != ctx.guild.owner.mention:
                    await a.write("\n"+str(member.mention))
                    await ctx.send(f"Added {member.mention} as an admin")

    @commands.command(
        help="Remove a user as an bot admin",
        usage="Ping a member as well to remove them as admin"
    )
    async def removeAdmin(self, ctx, member: discord.Member):
        if path.exists(f"Files/{ctx.guild.id}/Admins.txt"):
            async with aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt") as r:
                lines = await r.readlines()
                if lines == []:
                    await ctx.send("Nothing in admin file, please add an admin")  # noqa
                    # os.system(f"rm Files/{ctx.guild.id}/Admins.txt")
                else:
                    x = 0
                    remove = False
                    for line in lines:
                        if line.strip() == str(ctx.author.mention):
                            remove = True
                        if line.strip() == str(member.mention):
                            break
                        x = x + 1
                    if remove:
                        lines[x] = ""
                        async with aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt", 'w') as w:  # noqa
                            writeLine = ""
                            for line in lines:
                                writeLine = writeLine + line
                            await w.write(writeLine)
                            print(lines)
                            await ctx.send(f"Removed {member.mention} from Admins.txt")  # noqa
                    else:
                        await ctx.send(f"{ctx.author.mention}! You are not a trusted admin")  # noqa
        else:
            async with aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt", 'a') as a:  # noqa
                await a.write(str(ctx.guild.owner.mention))
            await ctx.send("Made Admins.txt file")

    @commands.command(
        help="Lists all admins in file",
        usage=""
    )
    async def listAdmins(self, ctx):
        embed = discord.Embed()
        async with aiofiles.open(f"Files/{ctx.guild.id}/Admins.txt") as f:
            lines = await f.readlines()
            for line in lines:
                embed.add_field(
                    name="Bot Admin",
                    value=line,
                    inline=False
                )
        await ctx.send(embed=embed)


def setup(client):
    print("setup?")
    client.add_cog(Admins(client))
