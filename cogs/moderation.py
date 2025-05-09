# cogs/moderation.py
import discord
from discord.ext import commands
from datetime import datetime
import asyncio

class Moderation(commands.Cog):
    """Server moderation commands"""

    def __init__(self, bot):
        self.bot = bot
        self.mute_role = None  # Set during setup
        self.log_channel = None

    async def cog_load(self):
        """Initialize mute role and log channel"""
        if not self.bot.guilds:
            return  # Avoid index error if not connected

        guild = self.bot.guilds[0]
        self.mute_role = discord.utils.get(guild.roles, name="Muted")
        self.log_channel = discord.utils.get(guild.channels, name="mod-logs")

    async def log_action(self, action: str, moderator: discord.Member, target: discord.Member, reason: str = None):
        """Log moderation actions to a channel"""
        if not self.log_channel:
            return

        embed = discord.Embed(
            title=f"🛠️ {action}",
            color=0xFF0000,
            timestamp=datetime.now()
        )
        embed.add_field(name="Moderator", value=moderator.mention, inline=True)
        embed.add_field(name="Target", value=target.mention, inline=True)
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)

        await self.log_channel.send(embed=embed)

    def is_admin_or_owner():
        """Custom check for admin or owner"""
        async def predicate(ctx):
            # Check if the user has 'Administrator' permission or is the server owner
            return ctx.author.guild_permissions.administrator or ctx.author.id == ctx.guild.owner_id
        return commands.check(predicate)

    @commands.command()
    @is_admin_or_owner()
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Kick a member from the server"""
        try:
            await member.kick(reason=reason)
            await ctx.send(f"✅ {member.display_name} has been kicked.")
            await self.log_action("Kick", ctx.author, member, reason)
        except Exception as e:
            await ctx.send(f"❌ Failed to kick: {e}")

    @commands.command()
    @is_admin_or_owner()
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Ban a member from the server"""
        try:
            await member.ban(reason=reason, delete_message_days=7)
            await ctx.send(f"✅ {member.display_name} has been banned.")
            await self.log_action("Ban", ctx.author, member, reason)
        except Exception as e:
            await ctx.send(f"❌ Failed to ban: {e}")

    @commands.command()
    @is_admin_or_owner()
    async def unban(self, ctx, *, user_id: int):
        """Unban a user by ID"""
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(f"✅ {user.name} has been unbanned.")
            await self.log_action("Unban", ctx.author, user)
        except Exception as e:
            await ctx.send(f"❌ Failed to unban: {e}")

    @commands.command()
    @is_admin_or_owner()
    async def mute(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Mute a member (requires 'Muted' role setup)"""
        if not self.mute_role:
            return await ctx.send("❌ Mute role not configured!")

        try:
            await member.add_roles(self.mute_role, reason=reason)
            await ctx.send(f"🔇 {member.display_name} has been muted.")
            await self.log_action("Mute", ctx.author, member, reason)
        except Exception as e:
            await ctx.send(f"❌ Failed to mute: {e}")

    @commands.command()
    @is_admin_or_owner()
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a member"""
        if not self.mute_role:
            return await ctx.send("❌ Mute role not configured!")

        try:
            await member.remove_roles(self.mute_role)
            await ctx.send(f"🔊 {member.display_name} has been unmuted.")
            await self.log_action("Unmute", ctx.author, member)
        except Exception as e:
            await ctx.send(f"❌ Failed to unmute: {e}")

    @commands.command()
    @is_admin_or_owner()
    async def purge(self, ctx, amount: int = 5):
        """Bulk delete messages (default: 5)"""
        if not 1 <= amount <= 100:
            return await ctx.send("❌ Amount must be between 1-100")

        try:
            await ctx.channel.purge(limit=amount + 1)  # +1 to include the command
            msg = await ctx.send(f"🧹 Deleted {amount} messages.", delete_after=3)
            await self.log_action("Purge", ctx.author, None, f"{amount} messages in {ctx.channel.mention}")
        except Exception as e:
            await ctx.send(f"❌ Failed to purge: {e}")

    @commands.command()
    @is_admin_or_owner()
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        """Warn a member with a reason"""
        try:
            await member.send(f"⚠️ You were warned in {ctx.guild.name}:\n**Reason:** {reason}")
            await ctx.send(f"⚠️ {member.mention} has been warned.")
            await self.log_action("Warn", ctx.author, member, reason)
        except Exception as e:
            await ctx.send(f"❌ Couldn't DM warning: {e}")


async def setup(bot): #
    await bot.add_cog(Moderation(bot))
