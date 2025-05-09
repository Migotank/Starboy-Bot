# cogs/welcome.py
import discord
from discord.ext import commands
from datetime import datetime
import os
import json


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = 1370163477817196544 # Replace with your welcome channel ID
        self.role_channel_id = 1370174300421623980  # Your role channel ID

    @commands.command(name="testwelcome")
    @commands.has_permissions(administrator=True)  # Optional: restrict to admins
    async def test_welcome(self, ctx, member: discord.Member = None):
        """Manually trigger the welcome message for testing"""
        member = member or ctx.author
        await self.on_member_join(member)
        await ctx.send(f"✅ Simulated welcome message for {member.mention}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Send welcome message with role channel reference"""
        channel = self.bot.get_channel(self.welcome_channel_id)
        if not channel:
            return

        embed = discord.Embed(
            title=f"🌟 Welcome {member.display_name}!",
            description=f"➤ Read {member.guild.rules_channel.mention} pinned message\n"
                        f"➤ Pick roles in <#{self.role_channel_id}>\n"
                        f"➤ Enjoy your stay!",
            color=0xEF0107,  # Arsenal red
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Member #{member.guild.member_count}")

        await channel.send(embed=embed)

        # Friendly DM with instructions
        try:
            await member.send(
                f"**Welcome to {member.guild.name}!** ⚽\n\n"
                f"➤ Rules: {member.guild.rules_channel.mention}\n"
                f"➤ Roles: <#{self.role_channel_id}>\n"
                f"➤ React with 🔴 to get Arsenal Fan role!"
            )
        except discord.Forbidden:
            pass  # User has DMs disabled

    @commands.command(name="setup_reaction_message")
    @commands.has_permissions(administrator=True)
    async def setup_reaction_message(self, ctx):
        """Send the reaction role message and store its ID"""
        message = await ctx.send("React with 🔴 to get the Arsenal Fan role!")
        await message.add_reaction("🔴")

        # Save message ID for tracking
        with open("reaction_message.json", "w") as f:
            json.dump({"message_id": message.id}, f)

        await ctx.send("✅ Reaction message set up and ID saved.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        if not os.path.exists("reaction_message.json"):
            return
        with open("reaction_message.json", "r") as f:
            data = json.load(f)

        if payload.message_id != data.get("message_id"):
            return
        if str(payload.emoji) != "🔴":
            return

        guild = self.bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name="Arsenal Fan")
        if role:
            await payload.member.add_roles(role, reason="Reacted for role")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if not os.path.exists("reaction_message.json"):
            return
        with open("reaction_message.json", "r") as f:
            data = json.load(f)

        if payload.message_id != data.get("message_id"):
            return
        if str(payload.emoji) != "🔴":
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = discord.utils.get(guild.roles, name="Arsenal Fan")
        if role and member:
            await member.remove_roles(role, reason="Unreacted from role")


async def setup(bot):
    await bot.add_cog(Welcome(bot))