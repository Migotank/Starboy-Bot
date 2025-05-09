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
        - `!teams [league]`: Lists all teams, or filters by league.
        - `!teams`: Lists all teams in all leagues.
        - `!teams premier league`: Lists only Premier League teams.
        - `!teams la liga`: Lists only La Liga teams.
        - `!leagues`: Displays a list of available leagues

        **General Commands**
        `!help` - Displays this message.

        **Welcome Commands**
        `!testwelcome` - Manually trigger the welcome message (admin only).
        `!setup_reaction_message` - Set up the reaction role message in the server (admin only).
        
        **Utility Commands:**
        - `!serverinfo`: Displays server statistics such as the server name, owner, member count, roles, and more.
        - `!userinfo [member]`: Displays information about a specific user or the user who triggered the command.
        - `!poll "question" "option1" "option2" ...`: Creates a poll with up to 10 options.
        - `!remind [time] [reminder]`: Set a reminder with a specified time (e.g., `1h30m Do homework`).
        - Time format can include days (`d`), hours (`h`), and minutes (`m`).
        - The bot will remind you in the specified channel.
        
        **Moderation Commands:**
        - `!kick [member] [reason]`: Kicks a member from the server with an optional reason. (admin only).
        - `!ban [member] [reason]`: Bans a member from the server for a specified reason. (admin only).
        - `!unban [user_id]`: Unbans a user from the server using their user ID. (admin only).
        - `!mute [member] [reason]`: Mutes a member (requires the 'Muted' role to be set up in the server).

        For more information on specific commands, just type `!help [command]`.
        """
        await ctx.send(help_text)

# Adding this cog to the bot
async def setup(bot):
    await bot.add_cog(Help(bot))
