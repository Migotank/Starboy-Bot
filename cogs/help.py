# cogs/help.py
import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Displays a list of all available commands for the bot"""
        help_text = """
        **Bot Commands:**

        **General Commands**
        `!help` - Displays this message.

        **Welcome Commands**
        `!testwelcome` - Manually trigger the welcome message (admin only).
        `!setup_reaction_message` - Set up the reaction role message in the server (admin only).
        """
        await ctx.send(help_text)

# Adding this cog to the bot
async def setup(bot):
    await bot.add_cog(Help(bot))
