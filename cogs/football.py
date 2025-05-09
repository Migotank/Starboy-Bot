# cogs/football.py
import os
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime


class Football(commands.Cog):
    """Complete football stats with multi-team and player support"""

    def __init__(self, bot):
        self.bot = bot
        self.leagues = {
            "premier_league": {
                "id": 39,
                "teams": {
                    "arsenal": {"id": 42, "color": 0xEF0107, "logo": "https://crests.football-data.org/57.png"},  # Red
                    "astonvilla": {"id": 66, "color": 0x670E36, "logo": "https://crests.football-data.org/58.png"},  # Claret & Blue
                    "bournemouth": {"id": 35, "color": 0xDA291C, "logo": "https://crests.football-data.org/bournemouth.png"},  # Red/Black
                    "brentford": {"id": 55, "color": 0xE30613, "logo": "https://crests.football-data.org/402.png"},  # Red/White
                    "brighton": {"id": 51, "color": 0x0057B8, "logo": "https://crests.football-data.org/397.png"},  # Blue
                    "chelsea": {"id": 49, "color": 0x034694, "logo": "https://crests.football-data.org/61.png"},  # Royal Blue
                    "crystalpalace": {"id": 52, "color": 0x1B458F, "logo": "https://crests.football-data.org/354.png"},  # Red/Blue
                    "everton": {"id": 45, "color": 0x003399, "logo": "https://crests.football-data.org/62.png"},  # Royal Blue
                    "fulham": {"id": 36, "color": 0x000000, "logo": "https://crests.football-data.org/63.png"},  # Black/White
                    "liverpool": {"id": 40, "color": 0xC8102E, "logo": "https://crests.football-data.org/64.png"},  # Red
                    "luton": {"id": 1359, "color": 0xFF5000, "logo": ""},  # Orange
                    "mancity": {"id": 50, "color": 0x6CABDD, "logo": "https://crests.football-data.org/65.png"},  # Sky Blue
                    "manutd": {"id": 33, "color": 0xDA291C, "logo": "https://crests.football-data.org/66.png"},  # Red
                    "newcastle": {"id": 34, "color": 0x241F20, "logo": "https://crests.football-data.org/67.png"},  # Black/White
                    "nottingham": {"id": 65, "color": 0xE53233, "logo": "https://crests.football-data.org/351.png"},  # Red
                    "sheffield": {"id": 62, "color": 0xEE2737, "logo": ""},  # Red/White
                    "tottenham": {"id": 47, "color": 0x132257, "logo": "https://crests.football-data.org/73.png"},  # Navy Blue
                    "westham": {"id": 48, "color": 0x7A263A, "logo": "https://crests.football-data.org/563.png"},  # Claret
                    "wolverhampton": {"id": 39, "color": 0xFDB913, "logo": "https://crests.football-data.org/76.png"}  # Gold/Black
                }
            },
            "la_liga": {
                "id": 140,
                "teams": {
                    "alaves": {"id": 542, "color": 0x0055A4, "logo": "https://crests.football-data.org/263.png"},  # Blue/White
                    "almeria": {"id": 723, "color": 0xEE2A24, "logo": ""},  # Red/White
                    "athletic": {"id": 531, "color": 0xEE2523, "logo": "https://crests.football-data.org/77.png"},  # Red/White
                    "atletico": {"id": 530, "color": 0xCB3524, "logo": "https://crests.football-data.org/78.png"},  # Red/White/Blue
                    "barcelona": {"id": 529, "color": 0xA50044, "logo": "https://crests.football-data.org/81.png"},  # Blue/Red
                    "betis": {"id": 543, "color": 0x1C9E4A, "logo": "https://crests.football-data.org/90.png"},  # Green/White
                    "cadiz": {"id": 724, "color": 0xFEF200, "logo": ""},  # Yellow/Blue
                    "celta": {"id": 538, "color": 0x67B2E8, "logo": "https://crests.football-data.org/558.png"},  # Sky Blue
                    "getafe": {"id": 546, "color": 0x0B5EA6, "logo": "https://crests.football-data.org/82.png"},  # Blue
                    "girona": {"id": 547, "color": 0xFFD100, "logo": "https://crests.football-data.org/298.png"},  # Red/White
                    "granada": {"id": 715, "color": 0xEE2033, "logo": ""},  # Red/Blue
                    "laspalmas": {"id": 534, "color": 0x007D4D, "logo": "https://crests.football-data.org/275.png"},  # Yellow/Blue
                    "mallorca": {"id": 536, "color": 0xE6003A, "logo": "https://crests.football-data.org/89.png"},  # Red/Black
                    "osasuna": {"id": 727, "color": 0x092C5C, "logo": "https://crests.football-data.org/79.png"},  # Red/Blue
                    "rayo": {"id": 728, "color": 0xDF0029, "logo": "https://crests.football-data.org/87.png"},  # Red
                    "realmadrid": {"id": 541, "color": 0xFEBE10, "logo": "https://crests.football-data.org/86.png"},  # White
                    "realsociedad": {"id": 548, "color": 0x0067B1, "logo": "https://crests.football-data.org/92.png"},  # Blue/White
                    "sevilla": {"id": 536, "color": 0xD4002A, "logo": "https://crests.football-data.org/559.png"},  # Red/White
                    "valencia": {"id": 532, "color": 0xF7A600, "logo": "https://crests.football-data.org/95.png"},  # Orange/Black
                    "villarreal": {"id": 533, "color": 0xF3C100, "logo": "https://crests.football-data.org/94.png"}  # Yellow
                }
            }
        }

        async def fetch_football_data(self, endpoint: str, params: dict = None):
            """Universal API fetcher with error handling"""
            headers = {
                "X-Auth-Token": os.getenv("FOOTBALL_API_KEY"),
                "Content-Type": "application/json"
            }
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(
                            f"https://api.football-data.org/v4/{endpoint}",
                            headers=headers,
                            params=params,
                            timeout=10
                    ) as response:
                        if response.status == 200:
                            return await response.json()
                        await self._handle_api_error(response.status)
                except Exception as e:
                    print(f"API Error: {e}")
                    return None

        @commands.command(name="team")
        async def team_stats(self, ctx, *, team_name: str):
            """Get team statistics (!team arsenal)"""
            team_data = await self._find_team(team_name)
            if not team_data:
                return await ctx.send("⚠️ Team not found. Try `!leagues` for options.")

            data = await self.fetch_football_data(f"teams/{team_data['id']}")

            embed = discord.Embed(
                title=f"🏟️ {data['name']} ({team_data['league']})",
                color=team_data["color"]
            )
            embed.set_thumbnail(url=team_data["logo"])
            embed.add_field(name="Venue", value=data["venue"], inline=False)
            embed.add_field(name="Founded", value=data["founded"], inline=True)
            await ctx.send(embed=embed)

        @commands.command(name="player")
        async def player_stats(self, ctx, *, name: str):
            """Get player statistics (!player vinicius)"""
            data = await self.fetch_football_data("players", {"name": name})

            if not data.get("response"):
                return await ctx.send(f"⚠️ Player '{name}' not found.")

            player = data["response"][0]["player"]
            stats = data["response"][0]["statistics"][0]
            team_name = stats["team"]["name"].lower().replace(" ", "")

            embed = discord.Embed(
                title=f"⭐ {player['name']} ({player['position']})",
                color=self._get_team_color(team_name)
            )
            embed.set_thumbnail(url=player["photo"])
            embed.add_field(name="Team", value=stats["team"]["name"], inline=True)
            embed.add_field(name="Goals", value=stats["goals"]["total"], inline=True)
            await ctx.send(embed=embed)

        @commands.command(name="leagues")
        async def list_leagues(self, ctx):
            """Show available leagues"""
            embed = discord.Embed(title="Available Leagues", color=0x7289DA)
            for league_id, league in self.leagues.items():
                embed.add_field(
                    name=f"🏆 {league['name']}",
                    value=f"`!teams {league_id}` to list teams",
                    inline=False
                )
            await ctx.send(embed=embed)

        @commands.command(name="teams")
        async def list_teams(self, ctx, league: str = "premier_league"):
            """List teams in a league (!teams la_liga)"""
            league_data = self.leagues.get(league.lower())
            if not league_data:
                return await ctx.send("⚠️ League not found. Try `!leagues`.")

            embed = discord.Embed(
                title=f"{league_data['name']} Teams",
                color=0x00FF00
            )
            team_list = "\n".join(
                f"• {team.replace('_', ' ').title()}"
                for team in league_data["teams"].keys()
            )
            embed.description = team_list
            await ctx.send(embed=embed)

        async def _find_team(self, team_name: str):
            """Search for team across all leagues"""
            team_key = team_name.lower().replace(" ", "")
            for league in self.leagues.values():
                if team_key in league["teams"]:
                    return {
                        **league["teams"][team_key],
                        "league": league["name"]
                    }
            return None

        def _get_team_color(self, team_name: str):
            """Get color for any team by name"""
            for league in self.leagues.values():
                for name, data in league["teams"].items():
                    if name == team_name.lower().replace(" ", ""):
                        return data["color"]
            return 0x000000  # Default black

    async def setup(bot):
        await bot.add_cog(Football(bot))