import discord, os
from discord.ext import commands
from discord import app_commands
from database import *
from automod import *
from plugins import load_plugins
from keep_alive import keep_alive

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await setup()
    load_plugins(bot)
    await bot.tree.sync()
    print("Bot online")

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return

    roles = await get_bypass_roles(msg.guild.id)
    if any(r.id in roles for r in msg.author.roles):
        return await bot.process_commands(msg)

    spam_on, caps_on, links_on = await get_automod(msg.guild.id)

    if spam_on and spam(msg.author.id):
        await msg.delete()
        return
    if caps_on and caps(msg.content):
        await msg.delete()
        return
    if links_on and links(msg.content):
        await msg.delete()
        return

    await bot.process_commands(msg)

@bot.command()
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member, *, reason):
    await add_warning(member.id, ctx.guild.id, reason)
    await log_action(ctx.guild.id, "WARN", ctx.author.id, member.id, reason)
    await ctx.send("Warned.")

@bot.tree.command(name="ping")
async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"{round(bot.latency*1000)}ms")

keep_alive()
bot.run(os.getenv("TOKEN"))
