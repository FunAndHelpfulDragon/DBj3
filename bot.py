import discord
import os
from discord.ext import commands
import aiofiles

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_guild_join(guild):
    print(f"Joined guild: {guild.name}")
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                name="Welcome",
                title="Welcome",
                description="Thank you for inviting me",
                colour=discord.Colour.random()
            )
            embed.add_field(
                name="Information about me!",
                value="I am a bot made for the discord bot jam 3 (itch.io/jam/dbj3) along the theme of security." +  # noqa
                      "\n All of my commands are found in !help and the developers of me are found in !credit"  # noqa
            )
            embed.add_field(
                name="How to get started?",
                value="No setup is required, the nessecary things have already been setup"  # noqa
            )
            embed.set_footer(
                value="Want to invite me? Do so here: https://discord.com/api/oauth2/authorize?client_id=893794121905471499&permissions=8&scope=bot"  # noqa
            )
            await channel.send(embed=embed)
            break
    if not os.path.exists(f"Files/{guild.id}"):
        os.system(f"mkdir Files/{guild.id}")
        async with aiofiles.open(f"Files/{guild.id}/Admins.txt", 'a') as a:  # noqa
            await a.write(str(guild.owner.mention) + ",")


@client.event
async def on_guild_remove(guild):
    print(f"Left guild: {guild.name}")
    # cleanup, the bot left why do we need the files?
    os.system(f"rm Files/{guild.id}/Admins.txt")
    os.system(f"rmdir Files/{guild.id}")


# Commands for cogs
@client.command(
    description="Loads a cog (limited to developers)",
    aliases=['Load', 'load'],
    hidden=True
)
@commands.is_owner()
async def _Load(ctx, extension):
    client.load_extension(f'Cogs.{extension}')  # loads a cog
    print(f'Cog: {extension} Loaded')


@client.command(
    description="Unloads a cog (limited to developers)",
    aliases=['UnLoad', 'unload', 'Unload'],
    hidden=True
)
@commands.is_owner()
async def _UnLoad(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')  # unloads a cog
    print(f'Cog: {extension} Unloaded')


@client.command(
    description="Reload a cog (limited to developers)",
    aliases=['Reload', 'reload'],
    hidden=True
)
@commands.is_owner()
async def _Reload(ctx, extension=None):
    if extension is not None:
        client.unload_extension(f'Cogs.{extension}')
        client.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Reloaded {extension}")
    else:
        for Cog in os.listdir("./Cogs"):
            if Cog != "__pycache__" and Cog != ".DS_Store":  # add no cogs here
                client.unload_extension(f'Cogs.{Cog[:-3]}')
                client.load_extension(f'Cogs.{Cog[:-3]}')
        await ctx.send("Reloaded cogs")


@client.command(
    description="List all cogs (not limited)",
    aliases=['ListCogs', 'List'],
    hidden=True
)
@commands.is_owner()
async def _ListCogs(ctx):  # no need to check as it can't do anything.
    await ctx.send("Cogs in folder: ")
    for filename in os.listdir("./Cogs"):
        if filename != "__pycache__" or filename == ".DS_Store":  # add no cogs
            await ctx.send(filename[:-3])


# error checking
# XXX: make it so that we know the cog that failed to load.
@_Load.error
async def Load_Fail_Error(ctx, error):
    print(error)


@_UnLoad.error
async def UnLoad_Fail_Error(ctx, error):
    print(error)


@_Reload.error
async def Reload_Fail_Error(ctx, error):
    print(error)


@_ListCogs.error
async def ListCogs_Fail_Error(ctx, error):
    print(error)


# loads all cogs on startup
if __name__ == '__main__':
    for cog in os.listdir("./Cogs"):
        if cog != "__pycache__" and cog != ".DS_Store":
            client.load_extension(f"Cogs.{cog[:-3]}")

    # Loads and runs bot
    with open("Token.txt") as f:
        Token = f.read()
    client.run(Token)
