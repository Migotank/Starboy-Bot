# cogs/utility.py
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio


class Utility(commands.Cog):
    """Server utilities and general purpose commands"""

    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}
        self.poll_cache = {}

    @commands.command(name="serverinfo")
    async def server_info(self, ctx):
        """Display server statistics"""
        guild = ctx.guild

        embed = discord.Embed(
            title=f"🛠️ {guild.name}",
            color=0xEF0107  # Arsenal red
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%b %d, %Y"), inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Channels", value=f"{len(guild.text_channels)} Text | {len(guild.voice_channels)} Voice",
                        inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name="userinfo")
    async def user_info(self, ctx, member: discord.Member = None):
        """Get user information"""
        member = member or ctx.author

        embed = discord.Embed(
            title=f"👤 {member.display_name}",
            color=member.color
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="Account Created", value=member.created_at.strftime("%b %d, %Y"), inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%b %d, %Y"), inline=True)

        roles = [role.mention for role in member.roles[1:]]  # Skip @everyone
        embed.add_field(
            name=f"Roles ({len(roles)})",
            value=" ".join(roles) if roles else "None",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="poll")
    async def create_poll(self, ctx, question, *options):
        """Create a poll (!poll "Question" "Option1" "Option2")"""
        if len(options) > 10:
            return await ctx.send("❌ Maximum 10 options allowed!")

        if len(options) < 2:
            return await ctx.send("❌ Need at least 2 options!")

        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        description = []

        for idx, option in enumerate(options):
            description.append(f"{emojis[idx]} {option}")

        embed = discord.Embed(
            title=f"📊 {question}",
            description="\n".join(description),
            color=0x7289DA
        )
        embed.set_footer(text=f"Poll by {ctx.author.display_name}")

        poll_msg = await ctx.send(embed=embed)

        # Cache poll info
        self.poll_cache[poll_msg.id] = {
            "question": question,
            "options": options,
            "author": ctx.author.id
        }

        # Add reactions
        for i in range(len(options)):
            await poll_msg.add_reaction(emojis[i])

    @commands.command(name="remind")
    async def set_reminder(self, ctx, time: str, *, reminder: str):
        """Set a reminder (!remind 1h30m Do homework)"""
        seconds = 0
        time = time.lower()

        if "d" in time:
            seconds += int(time.split("d")[0]) * 86400
            time = time.split("d")[1]
        if "h" in time:
            seconds += int(time.split("h")[0]) * 3600
            time = time.split("h")[1]
        if "m" in time:
            seconds += int(time.split("m")[0]) * 60

        if seconds <= 0:
            return await ctx.send("❌ Invalid time format! Use like `1h30m`")

        reminder_time = datetime.now() + timedelta(seconds=seconds)

        self.reminders[ctx.author.id] = {
            "time": reminder_time,
            "message": reminder,
            "channel": ctx.channel.id
        }

        await ctx.send(f"⏰ Reminder set for {reminder_time.strftime('%b %d at %H:%M')}!")

    @commands.Cog.listener()
    async def on_ready(self):
        """Start reminder loop when bot starts"""
        self.reminder_loop.start()

    @tasks.loop(minutes=1)
    async def reminder_loop(self):
        """Check for due reminders"""
        now = datetime.now()
        to_remove = []

        for user_id, reminder in self.reminders.items():
            if now >= reminder["time"]:
                channel = self.bot.get_channel(reminder["channel"])
                if channel:
                    user = await self.bot.fetch_user(user_id)
                    await channel.send(f"⏰ Reminder for {user.mention}: {reminder['message']}")
                to_remove.append(user_id)

        for user_id in to_remove:
            del self.reminders[user_id]


async def setup(bot):
    await bot.add_cog(Utility(bot))