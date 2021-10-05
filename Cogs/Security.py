import discord
from discord.ext import commands
from discord.ext.commands import has_permissions  # noqa
import asyncio
import random


class Secuirty(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Securly loaded the security cog")

    @has_permissions(administrator=True)
    @commands.command(
        help="Setup",
        usage="Setup the security that this bot gives"
    )
    async def Setup(self, ctx):
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
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
                discord.utils.get(ctx.guild.roles, name="Verified"): discord.PermissionOverwrite(read_messages=False)  # noqa
            }
            await ctx.guild.create_text_channel("Verify",
                                                overwrites=overwrites,
                                                topic="Verify here!",
                                                reason=f"Added via setup command by {ctx.author}")  # noqa
            await ctx.reply("Finished setup of server. Please note that some permissions might need changing mainly")  # noqa
        else:
            await ctx.reply("Cannot setup server because there is already a role called 'Verified'")  # noqa

    @commands.command(
        hidden=True,
        enabled=False
    )
    async def Delete(self, ctx):
        try:
            role = discord.utils.get(ctx.guild.roles, name="Verified")
            await role.delete()
        except AttributeError:
            print("AttributeError in deleting role")
        for channel in ctx.guild.channels:
            if channel.name == "verify":
                await channel.delete()
                break

    @Setup.error
    async def Setup_Error(self, ctx, error):
        await ctx.send(f"Error whilst seting up server! Error: {error}")

    @commands.command(
        help="Verify",
        usage="Verify your account"
    )
    async def Verify(self, ctx):
        Questions = ["What is the server id?", "What level (nitro boost) is the server at?"]  # noqa
        answers = [str(ctx.guild.id), str(ctx.guild.premium_tier)]

        verified = False
        for role in ctx.author.roles:
            if role.name == "Verified":
                verified = True
                await ctx.reply("You have already been verified!")
                break
        if not verified:
            embed = discord.Embed(
                title=f"Welcome to {ctx.guild}!",
                description="Verification process inisated"
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
                return not user.bot and reaction.message == msg and str(reaction.emoji) == "✅"  # noqa

            await msg.add_reaction("✅")
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=600, check=check)  # 600 = 10mins # noqa
            except asyncio.TimeoutError:
                await msg.reply("Oops, you didn't react in time, don't worry you are still in the server. say !verify in that server again to verify.")  # noqa
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
                    msg2 = await self.client.wait_for('message', timeout=600, check=Msgcheck)  # noqa
                except asyncio.TimeoutError:
                    await msg2.reply("Oops, you didn't respond in time.")
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
                        await msg3.reply("Oops, you didn't respond in time.")
                    else:
                        await ctx.author.send("Well done! You are now verified!")  # noqa
                        role = discord.utils.get(ctx.guild.roles, name="Verified")  # noqa
                        await ctx.author.add_roles(role, reason="User Verified!")  # noqa
                        await ctx.message.delete()


def setup(client):
    client.add_cog(Secuirty(client))
