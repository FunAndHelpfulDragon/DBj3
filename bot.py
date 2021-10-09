import discord
import os
from discord.ext import commands
from dislash import InteractionClient

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="+", intents=intents)
client.remove_command('help')

inter_client = InteractionClient(client, test_guilds=[686177483430952970])


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
            # embed.set_footer(
            #     text="Want to invite me? Do so here: https://discord.com/api/oauth2/authorize?client_id=893794121905471499&permissions=8&scope=bot"  # noqa
            # )
            await channel.send(embed=embed)
            break
    if not os.path.exists(f"Files/{guild.id}"):
        # automatically setups guild
        os.system(f"mkdir Files/{guild.id}")
        os.system(f"echo '{str(guild.owner.mention)},' > Files/{guild.id}/Admins.txt")  # noqa
        os.system(f"echo 'True' > Files/{guild.id}/Settings.txt")


@client.event
async def on_guild_remove(guild):
    print(f"Left guild: {guild.name}")
    # cleanup, the bot left why do we need the files?
    os.system(f"rm -r Files/{guild.id}")


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


# loads all cogs on startup
if __name__ == '__main__':
    for cog in os.listdir("./Cogs"):
        if cog != "__pycache__" and cog != ".DS_Store":
            client.load_extension(f"Cogs.{cog[:-3]}")

    # Loads and runs bot
    with open("Token.txt") as f:
        Token = f.read()
    client.run(Token)
