import discord
import asyncio
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        help="Help?",
        usage=""
    )
    async def Help(self, ctx):
        pages = []
        self.Page = 0
        # Make pages
        for cog in self.client.cogs:
            Embed = discord.Embed(
                title=cog,
                colour=discord.Colour.random()
            )
            for command in self.client.get_cog(cog).get_commands():
                if command.enabled and not command.hidden:
                    Embed.add_field(
                        name=f"{command.name} {command.aliases}",
                        value=f"Help: {command.help},\n" +
                             f"Usage: {command.usage}"
                    )
                    Embed.set_footer(
                        text="[] = aliases (other ways to use command)"
                    )
                    if str(Embed.fields) != str([]):
                        pages.append(Embed)

        msg = await ctx.send(embed=pages[self.Page])
        if self.Page > 0:
            await msg.add_reaction("⬅️")  # add reactions (if conditions meet)
        if self.Page < len(pages):
            await msg.add_reaction("➡️")

        await msg.add_reaction("❌")

        def check(reaction, user):  # check for reactions
            if not user.bot and reaction.message == msg:
                if str(reaction.emoji) == "⬅️":
                    self.Page -= 1
                elif str(reaction.emoji) == "➡️":
                    self.Page += 1
                elif str(reaction.emoji) == "❌":
                    self.Page = -1
                return True

        while self.Page != -1:  # while not close
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=600, check=check)  # 600 = 10mins # noqa
                await msg.remove_reaction(reaction, user)
                if self.Page != -1:
                    try:
                        await msg.edit(embed=pages[self.Page])  # edits with new  # noqa
                    except IndexError:
                        if self.Page > len(pages):
                            self.Page = len(pages)
                        elif self.Page < 0:
                            self.Page = 0
                        else:
                            await ctx.send("how? how did you break this?")
                        await msg.edit(embed=pages[self.Page])
                    if self.Page > 0:  # more reactions
                        await msg.add_reaction("⬅️")
                    else:
                        await msg.clear_reaction("⬅️")
                    if self.Page < len(pages):
                        await msg.add_reaction("➡️")
                    else:
                        await msg.clear_reaction("➡️")
                    await msg.add_reaction("❌")
            except asyncio.TimeoutError:  # timeout
                if msg is not None:
                    await msg.delete()
        else:  # delete but keep
            await msg.remove_reaction("⬅️", msg.author)
            await msg.remove_reaction("➡️", msg.author)
            await msg.remove_reaction("❌", msg.author)


def setup(client):
    client.add_cog(Help(client))
