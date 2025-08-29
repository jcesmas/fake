import discord
from discord.ext import commands, tasks
import aiohttp

BOT_TOKEN = "MTM5OTA5OTU4NDc2NDE4NjY4NA.GA3WSu.bqukZzoRqVUlOFwaGwzcP3zUAAjI4yJgEy_nFE"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def fetch_user_profile(user: discord.User):
    username = user.name
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
    return username, avatar_url

@bot.command(name="embed")
async def embed(ctx: commands.Context, target: str, *, message: str):
    user = None
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    else:
        try:
            user_id = int(target)
            user = await bot.fetch_user(user_id)
        except Exception:
            await ctx.send("Invalid user ID or mention.")
            return
    username, avatar_url = await fetch_user_profile(user)
    embed_obj = discord.Embed(
        title="Message deleted in #💬-┃-𝙜𝙚𝙣𝙚𝙧𝙖𝙡",
        description=f"{message}\n\nMessage ID: {ctx.message.id}",
        color=0xE74C3C,
        timestamp=ctx.message.created_at
    )
    embed_obj.set_author(name=username, icon_url=avatar_url)
    embed_obj.set_footer(text=f"ID: {user.id}")
    await ctx.send(embed=embed_obj)

@discord.app_commands.command(name="embed", description="Send an embed as a user")
async def embed_slash(interaction: discord.Interaction, user: discord.User, message: str):
    username, avatar_url = await fetch_user_profile(user)
    embed_obj = discord.Embed(
        title=f"Message deleted in #💬-┃-𝙜𝙚𝙣𝙚𝙧𝙖𝙡",
        description=message,
        color=0xE74C3C
    )
    embed_obj.set_author(name=username, icon_url=avatar_url)
    embed_obj.set_footer(text=f"ID: {user.id}")
    await interaction.response.send_message(embed=embed_obj)

@tasks.loop(minutes=1)
async def ping_worker():
    async with aiohttp.ClientSession() as session:
        try:
            await session.get("https://googleanalytics.anticroom.workers.dev/ping", timeout=3)
        except:
            pass

@bot.event
async def on_ready():
    ping_worker.start()

bot.run(BOT_TOKEN)
