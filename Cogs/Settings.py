from discord.ext import commands
from os import path
import sys
sys.path.append(path.join(path.dirname(__file__), "../Class"))
import FileReading  # noqa


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.File = FileReading.File()

    @commands.command(
        help="Change if you see the hourly tip or not. (bot admin required)",
        aliases=['ChangeTip', 'Tipoff', 'Tipon', 'tipoff', 'tipon',
                 'changetip', 'enableTip', 'enabletip', 'disabletip',
                 'disableTip']
    )
    async def ChangeTipEnability(self, ctx):
        if await self.File.CheckForAdmin(f"Files/{ctx.guild.id}/Admins.txt", ctx.author.mention):  # noqa
            data = ""
            if not self.File.CheckForFile(f"Files/{ctx.guild.id}/Settings.txt"):  # noqa
                self.File.MakeFile(f"Files/{ctx.guild.id}", "Settings.txt", "False")  # noqa
            else:
                result = await self.File.ReadFile(f"Files/{ctx.guild.id}/Settings.txt")  # noqa
                print(result)
                if result == "False":
                    data = "True"
                elif result == "True":
                    data = "False"
                else:
                    await ctx.send("Error in saving data...")
                    await ctx.send("Turning tips back on")
                    data = "True"
                await self.File.WriteFile(f"Files/{ctx.guild.id}/Settings.txt", data)  # noqa
                if data == "False":
                    await ctx.reply("Turned off hourly tips.")
                elif data == "True":
                    await ctx.reply("Turned on hourly tips.")
        else:
            await ctx.send("Only a trusted bot admin can change data")

    @commands.command(
        help="View the current state of the hourly tip.",
        aliases=['viewtip', 'tipState', 'tipstate']
    )
    async def viewTip(self, ctx):
        result = await self.File.ReadFile(f"Files/{ctx.guild.id}/Settings.txt")
        if result == "False":
            await ctx.reply("Hourly tips are currently off")
        else:
            await ctx.reply("Hourly tips are currently on")


def setup(client):
    client.add_cog(Settings(client))
