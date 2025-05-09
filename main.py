import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Required for message reading
intents.members = True  # Required for welcome messages

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,  # Disable default help command
    case_insensitive=True  # Makes !Ping work like !ping
)


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded cog: {filename[:-3]}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

    # Manually ensure utility loads even if not in /cogs folder
    try:
        await bot.load_extension("cogs.utility")  # 🛠️ Add this line
        print("✅ Loaded utility cog")
    except Exception as e:
        print(f"❌ Failed to load utility cog: {e}")


# Bot events
@bot.event
async def on_ready():
    print(f"\n🔴 StarBot is online as {bot.user.name}")
    print(f"🛠️ Guilds: {len(bot.guilds)}")
    print(f"⌚ Discord.py version: {discord.__version__}\n")

    await load_cogs()  # Load all cogs
    await bot.tree.sync()  # Sync slash commands (if using)

    # Set custom status
    await bot.change_presence(activity=discord.Game(name="⚽ North London Is Red!"))


# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.send(f"❌ Error: {str(error)}", delete_after=10)


# Basic test command
@bot.command(name="ping")
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! {latency}ms")


# Run the bot
if __name__ == "__main__":
    try:
        bot.run(os.getenv("DISCORD_BOT_TOKEN"))
    except discord.LoginFailure:
        print("⚠️ Invalid bot token! Check your .env file.")
    except KeyboardInterrupt:
        print("🛑 Bot shutting down...")