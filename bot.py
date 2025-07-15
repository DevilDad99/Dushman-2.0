import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

BLOCKED_WORDS = ["good morning", "gm", "shubh prabhat", "gud morning"]
IGNORED_USERS = []  # Add user IDs to ignore
BOSS_USERS = [1368236764564553829, 1025027158567043072, 1135951424199606434]  # Boss user IDs

LOG_FILE = "bot_logs.txt"

def log_action(action):
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action}\n")

@bot.event
async def on_ready():
    print(f"Dushman Bot v3 is online as {bot.user}")
    log_action("Bot started and ready.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    if any(word in content for word in BLOCKED_WORDS):
        if message.author.id in BOSS_USERS:
            await message.channel.send(f"{message.author.mention} Malik, aap takleef na karein... main bol dunga sabko 😌")
            log_action(f"Ignored morning wish from boss: {message.author}")
        elif message.author.id in IGNORED_USERS:
            log_action(f"Ignored user sent: {content}")
        else:
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Andha nahi hai, subah ho gayi hai. Bade aaye Good Morning bolne wale 😎")
                log_action(f"Deleted message: {message.author} said: {content}")
            except discord.Forbidden:
                log_action(f"Permission error trying to delete from {message.author}")

    if "@everyone" in message.content or "@here" in message.content:
        await message.channel.send(f"{message.author.mention} Maan ja, kyun ban khayega 😤")
        log_action(f"Mass mention detected by {message.author}")

    await bot.process_commands(message)

@bot.command()
async def showlog(ctx):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as log:
            lines = log.readlines()[-10:]
            await ctx.send("```" + "".join(lines) + "```")
    except FileNotFoundError:
        await ctx.send("No log file found.")
bot.run("MTM5NDYwOTI0NzQzNzg1MjcxNA.Gljxq4.cX09doGAGlqPmIRppI4P3OwGzL2Ez3FG_WzaS8")
