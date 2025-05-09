import os
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime


class Football(commands.Cog):
    """Complete football stats with all Premier League and La Liga teams"""

    def __init__(self, bot):
        self.bot = bot
        self.team_data = {
            "premier_league": {
                "name": "Premier League",
                "teams": {
                    "arsenal": {"id": 57, "color": 0xEF0107},
                    "astonvilla": {"id": 58, "color": 0x670E36},
                    "bournemouth": {"id": 1044, "color": 0xDA291C},
                    "brentford": {"id": 402, "color": 0xE30613},
                    "brighton": {"id": 397, "color": 0x0057B8},
                    "chelsea": {"id": 61, "color": 0x034694},
                    "crystalpalace": {"id": 354, "color": 0x1B458F},
                    "everton": {"id": 62, "color": 0x003399},
                    "fulham": {"id": 63, "color": 0x000000},
                    "liverpool": {"id": 64, "color": 0xC8102E},
                    "luton": {"id": 1359, "color": 0xFF5000},
                    "mancity": {"id": 65, "color": 0x6CABDD},
                    "manutd": {"id": 66, "color": 0xDA291C},
                    "newcastle": {"id": 67, "color": 0x241F20},
                    "nottingham": {"id": 351, "color": 0xE53233},
                    "sheffield": {"id": 356, "color": 0xEE2737},
                    "tottenham": {"id": 73, "color": 0x132257},
                    "westham": {"id": 563, "color": 0x7A263A},
                    "wolves": {"id": 76, "color": 0xFDB913}
                }
            },
            "la_liga": {
                "name": "La Liga",
                "teams": {
                    "alaves": {"id": 263, "color": 0x0055A4},
                    "almeria": {"id": 724, "color": 0xEE2A24},
                    "athletic": {"id": 77, "color": 0xEE2523},
                    "atletico": {"id": 78, "color": 0xCB3524},
                    "barcelona": {"id": 81, "color": 0xA50044},
                    "betis": {"id": 90, "color": 0x1C9E4A},
                    "cadiz": {"id": 724, "color": 0xFEF200},
                    "celta": {"id": 558, "color": 0x67B2E8},
                    "getafe": {"id": 82, "color": 0x0B5EA6},
                    "girona": {"id": 298, "color": 0xFFD100},
                    "granada": {"id": 715, "color": 0xEE2033},
                    "laspalmas": {"id": 275, "color": 0x007D4D},
                    "mallorca": {"id": 89, "color": 0xE6003A},
                    "osasuna": {"id": 79, "color": 0x092C5C},
                    "rayo": {"id": 87, "color": 0xDF0029},
                    "realmadrid": {"id": 86, "color": 0xFEBE10},
                    "realsociedad": {"id": 92, "color": 0x0067B1},
                    "sevilla": {"id": 559, "color": 0xD4002A},
                    "valencia": {"id": 95, "color": 0xF7A600},
                    "villarreal": {"id": 94, "color": 0xF3C100}
                }
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
        team_info = await self._get_team_info(team_name)
        if not team_info:
            return await ctx.send("⚠️ Team not found. Try `!teams` for options.")

        data = await self.fetch_football_data(f"teams/{team_info['id']}")
        if "error" in data:
            return await ctx.send(f"⚠️ {data['error']}")

        embed = discord.Embed(
            title=f"🏟️ {data['name']} ({data['shortName']})",
            color=team_info["color"]
        )
        embed.set_thumbnail(url=data['crest'])

        # Core info
        embed.add_field(name="📍 Venue", value=data['venue'], inline=True)
        embed.add_field(name="📅 Founded", value=data['founded'], inline=True)
        embed.add_field(name="🌍 Area", value=data['area']['name'], inline=True)

        # Competitions
        comps = "\n".join(f"• {c['name']}" for c in data['runningCompetitions'])
        embed.add_field(name="🏆 Competitions", value=comps, inline=False)

        await ctx.send(embed=embed)

    async def _get_team_info(self, team_name: str):
        """Find team data from name"""
        team_key = team_name.lower().replace(" ", "")
        for league in self.team_data.values():
            if team_key in league["teams"]:
                return {
                    "id": league["teams"][team_key]["id"],
                    "color": league["teams"][team_key]["color"],
                    "league": league["name"]
                }
        return None

    @commands.command(name="teams")
    async def list_teams(self, ctx, *, league: str = None):
        """List all teams or filter by league"""
        embed = discord.Embed(title="Available Teams", color=0x00FF00)

        if league:
            league_key = league.lower().replace(" ", "_")
            if league_key in self.team_data:
                team_list = "\n".join(
                    f"• {team.replace('_', ' ').title()}"
                    for team in self.team_data[league_key]["teams"].keys()
                )
                embed.add_field(
                    name=f"🏆 {self.team_data[league_key]['name']}",
                    value=team_list,
                    inline=False
                )
            else:
                await ctx.send("⚠️ League not found. Try `!leagues`")
                return
        else:
            for league_name, league in self.team_data.items():
                team_list = "\n".join(
                    f"• {team.replace('_', ' ').title()}"
                    for team in league["teams"].keys()
                )
                embed.add_field(
                    name=f"🏆 {league['name']}",
                    value=team_list,
                    inline=False
                )

        await ctx.send(embed=embed)

    @commands.command(name="leagues")
    async def list_leagues(self, ctx):
        """List available leagues"""
        embed = discord.Embed(title="Available Leagues", color=0x7289DA)
        for league in self.team_data.values():
            embed.add_field(
                name=f"🏆 {league['name']}",
                value=f"`!teams {league['name'].lower()}` to view teams",
                inline=False
            )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Football(bot))