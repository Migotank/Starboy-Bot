# cogs/welcome.py
import discord
from discord.ext import commands
from datetime import datetime
import os
import json


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = 1370163477817196544  # Replace with your welcome channel ID
        self.role_channel_id = 1370174300421623980     # Replace with your role channel ID
        self.reaction_emoji = "🔴"
        self.reaction_role_name = "Arsenal Fan"
        self.reaction_message_file = "reaction_message.json"

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Send welcome embed and reaction instructions"""
        channel = self.bot.get_channel(self.welcome_channel_id)
        if not channel:
            return

        # Send embed in welcome channel
        embed = discord.Embed(
            title=f"🌟 Welcome {member.display_name}!",
            description=(
                f"➤ Read {member.guild.rules_channel.mention} pinned message\n"
                f"➤ Pick roles in <#{self.role_channel_id}>\n"
                f"➤ Enjoy your stay!"
            ),
            color=0xEF0107,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Member #{member.guild.member_count}")
        await channel.send(embed=embed)

        # Create or get existing reaction message
        message = await self.get_or_create_reaction_message(channel)

        # Send DM with direct link to reaction message
        try:
            await member.send(
                f"**Welcome to {member.guild.name}!** ⚽\n\n"
                f"➤ Rules: {member.guild.rules_channel.mention}\n"
                f"➤ Roles: <#{self.role_channel_id}>\n"
                f"➤ React with {self.reaction_emoji} to [this message]({message.jump_url}) "
                f"to get the **{self.reaction_role_name}** role!"
            )
        except discord.Forbidden:
            pass  # DMs disabled

    async def get_or_create_reaction_message(self, channel):
        """Ensure the reaction message exists; create if not"""
        if os.path.exists(self.reaction_message_file):
            with open(self.reaction_message_file, "r") as f:
                data = json.load(f)
            try:
                return await self.bot.get_channel(data["channel_id"]).fetch_message(data["message_id"])
            except discord.NotFound:
                pass  # Message deleted or invalid

        # Create new reaction message
        msg = await channel.send(f"React with {self.reaction_emoji} to get the **{self.reaction_role_name}** role!")
        await msg.add_reaction(self.reaction_emoji)

        with open(self.reaction_message_file, "w") as f:
            json.dump({"message_id": msg.id, "channel_id": channel.id}, f)

        return msg

    @commands.command(name="testwelcome")
    @commands.has_permissions(administrator=True)
    async def test_welcome(self, ctx, member: discord.Member = None):
        """Manually trigger welcome message"""
        member = member or ctx.author
        await self.on_member_join(member)
        await ctx.send(f"✅ Simulated welcome for {member.mention}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member and payload.member.bot:
            return
        if not os.path.exists(self.reaction_message_file):
            return

        with open(self.reaction_message_file, "r") as f:
            data = json.load(f)

        if payload.message_id != data["message_id"] or str(payload.emoji) != self.reaction_emoji:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = payload.member or guild.get_member(payload.user_id)
        role = discord.utils.get(guild.roles, name=self.reaction_role_name)
        if role and member:
            await member.add_roles(role, reason="Reacted to gain role")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if not os.path.exists(self.reaction_message_file):
            return

        with open(self.reaction_message_file, "r") as f:
            data = json.load(f)

        if payload.message_id != data["message_id"] or str(payload.emoji) != self.reaction_emoji:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = discord.utils.get(guild.roles, name=self.reaction_role_name)
        if role and member:
            await member.remove_roles(role, reason="Unreacted to remove role")


async def setup(bot):
    await bot.add_cog(Welcome(bot))
