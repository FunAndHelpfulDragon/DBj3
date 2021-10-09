import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions  # noqa
import asyncio
import random
from os import path
import sys
from dislash import slash_command, Option, OptionType, ActionRow, Button, ButtonStyle  # noqa
sys.path.append(path.join(path.dirname(__file__), "../Class"))
import FileReading  # noqa


class Secuirty(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Securly loaded the security cog")
        self.PreSetup = False
        self.File = FileReading.File()
        self.send.start()

    @commands.command(
        help="Setup",
        usage="Setup the security that this bot gives",
        aliases=['setup']
    )
    async def Setup(self, ctx):
        if await self.File.CheckForAdmin("Files/{ctx.guild.id}/Admins.txt", ctx.author.mention):  # noqa
            # make a verified role.
            self.Setup = True
            for role in ctx.guild.roles:
                if role.name == "Verified":
                    self.Setup = False
                    break
            if self.Setup:
                await ctx.guild.create_role(name="Verified",
                                            colour=discord.Colour.random(),
                                            hoist=True,
                                            mentionable=False,
                                            reason=f"Created via setup command by {ctx.author}")  # noqa
                role = discord.utils.get(ctx.guild.roles, name="Verified")
                await ctx.author.add_roles(role, reason=f"Added via setup command by {ctx.author}")  # noqa
                await ctx.guild.me.add_roles(role, reason=f"Added via setup command by {ctx.author}")  # noqa

                # make a place to verify
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True),  # noqa
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True),  # noqa
                    discord.utils.get(ctx.guild.roles, name="Verified"): discord.PermissionOverwrite(read_messages=False)  # noqa
                }
                await ctx.guild.create_text_channel("Verify",
                                                    overwrites=overwrites,
                                                    topic="Verify here!",
                                                    reason=f"Added via setup command by {ctx.author}")  # noqa
                await ctx.reply("Finished setup of server. Please note that some permissions might need changing mainly")  # noqa
            else:
                await ctx.reply("Cannot setup server because there is already a role called 'Verified'")  # noqa
        else:
            await ctx.reply("You are not a bot admin!")

    @commands.command(
        hidden=True,
        enabled=True
    )
    async def Delete(self, ctx):
        if await self.File.CheckForAdmin("Files/{ctx.guild.id}/Admins.txt", ctx.author.mention):  # noqa
            try:
                role = discord.utils.get(ctx.guild.roles, name="Verified")
                await role.delete()
            except AttributeError:
                print("AttributeError in deleting role")
            for channel in ctx.guild.channels:
                if channel.name == "verify":
                    await channel.delete()
                    break
            await ctx.send("Deleted verifiecation things")
        else:
            await ctx.reply("You are not a bot admin!")

    @Setup.error
    async def Setup_Error(self, ctx, error):
        await ctx.send(f"Error whilst seting up server! Error: {error}")

    @commands.command(
        help="Verify",
        usage="Verify your account",
        aliases=['verify']
    )
    async def Verify(self, ctx):
        Questions = ["What is the server id?",
                     "What level (nitro boost) is the server at?",
                     "Who is the owner of the server (just name required)"]  # noqa
        answers = [str(ctx.guild.id),
                   str(ctx.guild.premium_tier),
                   str(ctx.guild.owner.name)]
        if discord.utils.get(ctx.guild.roles, name="Verified") is not None:
            verified = False
            for role in ctx.author.roles:
                if role.name == "Verified":
                    verified = True
                    await ctx.reply("You have already been verified!")
                    break
            if not verified:
                embed = discord.Embed(
                    title=f"Welcome to {ctx.guild}!",
                    description="Verification process inisated",
                    colour=discord.Colour.random()
                )
                embed.add_field(
                    name="Verification",
                    value="In order to verify, you need to pass a short quiz and solve this captura."  # noqa
                )
                embed.add_field(
                    name="Why?",
                    value="This is for security, the server owner has setup this bot for security"  # noqa
                )
                embed.add_field(
                    name="Start",
                    value="To start, react to this message"
                )
                msg = await ctx.author.send(embed=embed)

                def check(reaction, user):  # check for reactions
                    return not user.bot and reaction.message.id == msg.id and str(reaction.emoji) == "✅"  # noqa

                await msg.add_reaction("✅")
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=300, check=check)  # 600 = 10mins # noqa
                except asyncio.TimeoutError:
                    await msg.reply(f"Oops, you didn't react in time, don't worry you are still in the server. say {self.client.prefix}verify in that server again to verify.")  # noqa
                else:
                    await msg.reply("Thanks, now lets move on.")
                    String = ""
                    tempstring = ctx.author.name
                    for char in tempstring:
                        choiceChar = random.randint(0, len(tempstring) - 1)
                        String = String + tempstring[choiceChar]
                        tempstring = tempstring.replace(tempstring[choiceChar], "", 1)  # noqa

                    await ctx.author.send(f"Decrypt this message: {String}")

                    def Msgcheck(m):
                        return m.content == ctx.author.name

                    try:
                        msg2 = await self.client.wait_for('message', timeout=300, check=Msgcheck)  # noqa
                    except asyncio.TimeoutError:
                        await msg.reply(f"Oops, you didn't react in time, don't worry you are still in the server. say {self.client.prefix}verify in that server again to verify.")  # noqa
                    else:
                        await msg2.reply("Well done! now onto the next stage")
                        await ctx.author.send("You will be given a random question, if you get it correct you will be verified, if you get it incorrect you need to restart the verification process")  # noqa
                        Qno = random.randint(0, len(Questions) - 1)
                        await ctx.author.send(Questions[Qno])

                        def QuizCheck(m):
                            return m.content == answers[Qno] #and msg3.author == ctx.author  # noqa

                        try:
                            msg3 = await self.client.wait_for('message', timeout=600, check=QuizCheck)  # noqa
                        except asyncio.TimeoutError:
                            await msg3.reply("Oops, you didn't respond in time.")  # noqa
                        else:
                            await ctx.author.send("Well done! You are now verified!")  # noqa
                            role = discord.utils.get(ctx.guild.roles, name="Verified")  # noqa
                            await ctx.author.add_roles(role, reason="User Verified!")  # noqa
                            await ctx.message.delete()
        else:
            await ctx.send("No verification process setup! please contact a bot admin")  # noqa

    @slash_command(
        description="Send a encrypted message to someone",
        options=[
            Option("member", "Enter the user", OptionType.USER, required=True),
            Option("content", "Enter the content", OptionType.STRING, required=True)  # noqa
            ]
        )
    async def code(self, ctx, member, content):
        await ctx.reply(f"{content} -> {member.mention}", ephemeral=True)
        String = ""
        nconent = content
        for char in nconent:
            num = random.randint(0, len(nconent) - 1)
            String = String + str(num)
            nconent = nconent.replace(nconent[num], "", 1)

        Buttons = ActionRow(
            Button(
                style=ButtonStyle.blurple,
                label="Decrypt",
                custom_id="Decrypt"
            )
        )

        msg = await ctx.reply(f"{ctx.author.mention} used /code:\n {String}", components=[Buttons])  # noqa
        seen = False
        while not seen:
            inter = await msg.wait_for_button_click()
            if inter.author == member:
                await inter.reply(f"DecryptedMessage: {String}.\nMessage: {content}.\nSent by: {ctx.author.mention}", ephemeral=True)  # noqa
                seen = True
                await msg.delete()
            elif inter.author == ctx.author:
                await inter.reply(f"You are author of message, so here is info you sent:\n{content} -> {member.mention}", ephemeral=True)  # noqa
            else:
                await inter.reply("Sorry, the author of the message didn't send it to you", ephemeral=True) # noqa

    @tasks.loop(hours=1.0)
    async def send(self):
        for guild in self.client.guilds:
            if await self.File.ReadFile(f"Files/{guild.id}/Settings.txt") == "True":  # noqa
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        tip = await self.GenSecurityTip()
                        await channel.send("Security Tip of the hour: \n" + tip)  # noqa
                        break

    @commands.command(
        help="Get a Security Tip",
        usage="",
        aliases=['tip']
    )
    async def Tip(self, ctx):
        await ctx.reply(await self.GenSecurityTip())

    async def GenSecurityTip(self):
        PossibleTips = await self.File.ReadLinesFile("Class/SecurityTips.txt")  # noqa
        return PossibleTips[random.randint(0, len(PossibleTips) - 1)]

    def cog_unload(self):
        self.send.cancel()

    @send.before_loop
    async def BeforeSend(self):
        print('waiting for bot to load')
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(Secuirty(client))
