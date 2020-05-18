import discord
from discord.ext import commands
import asyncio
import sys, traceback
import time
import os
import math
import json
import sqlite3

bot = commands.Bot(command_prefix='?', case_insensitive=True)
bot.remove_command('help')

@bot.event
async def on_guild_join(guild):
    main = sqlite3.connect('Leveling/main.db')
    cursor = main.cursor()
    cursor.execute(f"SELECT enabled FROM glevel WHERE guild_id = '{guild.id}'")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO glevel(guild_id, enabled) VALUES(?,?)")
        val = (str(guild.id), 'enabled')
        cursor.execute(sql, val)
        main.commit()
    elif str(result[0]) == 'disabled':
        sql = ("UPDATE glevel SET enabled = ? WHERE guild_id = ?")
        val = ('enabled', str(guild.id))
        cursor.execute(sql, val)
        main.commit()
    cursor.close()
    main.close()

@bot.command()
async def load(ctx, *, extension):
    ctx.load_extension(f'src.bot.cogs.{extension}')

@bot.command()
async def unload(ctx, *, extension):
    ctx.unload_extension(f'src.bot.cogs.{extension}')

for filename in os.listdir('./src/bot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'src.bot.cogs.{filename[:-3]}')

bot.run('TOKEN_HERE')
