# cogs/welcome.py
import discord
from discord.ext import commands
from datetime import datetime


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
            description=f"1. Read {member.guild.rules_channel.mention}\n"
                        f"2. Pick roles in <#{self.role_channel_id}>\n"
                        f"3. Enjoy your stay!",
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


async def setup(bot):
    await bot.add_cog(Welcome(bot))