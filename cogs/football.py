import os
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime


class Football(commands.Cog):
    """Complete football team statistics with squad and match data"""

    def __init__(self, bot):
        self.bot = bot
        self.team_ids = {
            "premier_league": {
                "arsenal": 57,
                "chelsea": 61,
                "manutd": 66,
                "mancity": 65,
                "tottenham": 73,
                "liverpool": 64
            },
            "la_liga": {
                "barcelona": 81,
                "realmadrid": 86,
                "atletico": 78
            }
        }

    async def fetch_football_data(self, endpoint: str):
        """Universal API fetcher with error handling"""
        headers = {
            "X-Auth-Token": os.getenv("FOOTBALL_API_TOKEN").strip(),
            "Content-Type": "application/json"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"https://api.football-data.org/v4/{endpoint}",
                        headers=headers,
                        timeout=10
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return {"error": f"API Error: HTTP {response.status}"}
        except Exception as e:
            return {"error": f"Connection failed: {str(e)}"}

    @commands.command(name="team")
    async def team_info(self, ctx, *, team_name: str):
        """Get comprehensive team information"""
        team_id = await self._get_team_id(team_name)
        if not team_id:
            return await ctx.send("⚠️ Team not found. Try `!teams` for options.")

        data = await self.fetch_football_data(f"teams/{team_id}")
        if "error" in data:
            return await ctx.send(f"⚠️ {data['error']}")

        embed = discord.Embed(
            title=f"🏟️ {data['name']} ({data['shortName']})",
            description=f"*{data['clubColors']}*",
            color=await self._get_team_color(team_name)
        )
        embed.set_thumbnail(url=data['crest'])

        # Core information
        embed.add_field(name="📍 Venue", value=data['venue'], inline=True)
        embed.add_field(name="📅 Founded", value=data['founded'], inline=True)
        embed.add_field(name="🌍 Area", value=data['area']['name'], inline=True)

        # Competitions
        comps = "\n".join(f"• {c['name']}" for c in data['runningCompetitions'])
        embed.add_field(name="🏆 Current Competitions", value=comps, inline=False)

        # Coach info if available
        if data.get('coach'):
            embed.add_field(
                name="👔 Coach",
                value=f"{data['coach']['name']} ({data['coach']['nationality']})",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name="squad")
    async def team_squad(self, ctx, *, team_name: str):
        """Show team squad with positions"""
        team_id = await self._get_team_id(team_name)
        if not team_id:
            return await ctx.send("⚠️ Team not found. Try `!teams` for options.")

        data = await self.fetch_football_data(f"teams/{team_id}")
        if "error" in data:
            return await ctx.send(f"⚠️ {data['error']}")

        embed = discord.Embed(
            title=f"👥 {data['name']} Squad",
            color=await self._get_team_color(team_name)
        )

        # Group players by position
        positions = {}
        for player in data['squad']:
            positions.setdefault(player['position'], []).append(player['name'])

        # Add fields for each position
        for position, players in positions.items():
            embed.add_field(
                name=f"⚽ {position}",
                value="\n".join(players),
                inline=True
            )

        await ctx.send(embed=embed)

    @commands.command(name="matches")
    async def team_matches(self, ctx, *, team_name: str):
        """Show team's upcoming matches"""
        team_id = await self._get_team_id(team_name)
        if not team_id:
            return await ctx.send("⚠️ Team not found. Try `!teams` for options.")

        data = await self.fetch_football_data(f"teams/{team_id}/matches?status=SCHEDULED")
        if "error" in data:
            return await ctx.send(f"⚠️ {data['error']}")

        embed = discord.Embed(
            title=f"📅 {team_name.title()} Upcoming Matches",
            color=await self._get_team_color(team_name)
        )

        for match in data['matches'][:5]:  # Show next 5 matches
            date = datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
            embed.add_field(
                name=f"🆚 {match['homeTeam']['shortName']} vs {match['awayTeam']['shortName']}",
                value=f"🗓️ {date.strftime('%b %d %H:%M')}\n🏆 {match['competition']['name']}",
                inline=False
            )

        await ctx.send(embed=embed)

    async def _get_team_id(self, team_name: str):
        """Find team ID from name"""
        team_key = team_name.lower().replace(" ", "")
        for league in self.team_ids.values():
            if team_key in league:
                return league[team_key]
        return None

    async def _get_team_color(self, team_name: str):
        """Get team color for embeds"""
        # You could expand this with actual team colors
        return 0x7289DA  # Default discord blue

    @commands.command(name="teams")
    async def list_teams(self, ctx):
        """List all available teams"""
        embed = discord.Embed(title="Available Teams", color=0x00FF00)

        for league_name, teams in self.team_ids.items():
            team_list = "\n".join(
                f"• {team.replace('_', ' ').title()}"
                for team in teams.keys()
            )
            embed.add_field(
                name=f"🏆 {league_name.replace('_', ' ').title()}",
                value=team_list,
                inline=False
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Football(bot))