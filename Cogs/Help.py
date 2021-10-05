import discord
import asyncio
from discord.ext import commands
from dislash import SelectMenu, SelectOption


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("help cog loaded")

    @commands.command(
        help="Help?",
        usage="",
        aliases=["Help"]
    )
    async def help(self, ctx):  # noqa
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

        options = []
        for x in range(0, len(pages)):
            options.append(SelectOption(pages[x].title, f"Help for {pages[x].title}"))  # noqa
        options.append(SelectOption("Quit", "Stop this help function"))

        menuOptions = SelectMenu(
            custom_id="helpMenu",
            placeholder="ChooseNextPage",
            max_values=1,
            options=options
        )
        print(pages)

        msg = await ctx.send(embed=pages[self.Page], components=[menuOptions])

        while self.Page != -1:  # while not close
            try:
                response = await msg.wait_for_dropdown(timeout=600)
                label = [option.label for option in response.select_menu.selected_options][0]  # noqa
                if label == "Quit":
                    self.Page = -1
                # await response.reply("You can dismiss this response, this is to make sure you don't get an interaction failed error", ephemeral=True)  # noqa
                await response.reply("", ephemeral=True)  # noqa
                pageNo = 0
                for page in pages:
                    if page.title == label:
                        self.Page = pageNo
                    pageNo = pageNo + 1
                await msg.edit(embed=pages[self.Page], components=[menuOptions])  # edits with new  # noqa
            except asyncio.exceptions.TimeoutError:
                self.Page = -1
        if self.Page == -1:
            await msg.delete()

    @commands.command(
        help="makers of the bot",
        usage="",
        aliases=["credit"]
    )
    async def Credit(self, ctx):
        embed = discord.Embed(
            title="Credits",
            colour=discord.Colour.random()
        )
        embed.add_field(
            name="Dragmine149#5048",
            value="Maker of the bot"
        )
        # embed.add_field(
        #     name="Dqrkxz#8752",
        #     value="Bot tester"
        # )
        embed.set_footer(text="Thank you for usingthis bot that was made in a week for dbj3")  # noqa
        await ctx.send(embed=embed)

    @commands.command(
        help="Invite me",
        usage="",
        aliases=["invite"],
        enabled=False,
        hidden=True
    )
    async def Invite(self, ctx):
        await ctx.send("This has been disabled for the moment")
        # await ctx.send("Invite me here: https://discord.com/api/oauth2/authorize?client_id=893794121905471499&permissions=8&scope=bot")  # noqa


def setup(client):
    client.add_cog(Help(client))
