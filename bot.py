import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    print("Bot is ready")


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
