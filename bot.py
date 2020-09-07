import discord
from discord.ext import commands
import asyncio
import json
import math
import os
import random
import sqlite3
import sys, traceback
import time

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

#############################################cleaner
@bot.event
async def on read():
    print('Bot is ready.')

@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
#############################################

#############################################spam
@bot.command(pass_context=true)
async def spam(ctx):
    while True:
        await bot.say("")
        await bot.say("")
        await bot.say("")
#############################################

#############################################ban/unban
@client.command()
@commands.has_permission(kick_members=True)
##########################ban by id
#async def ban (ctx, member:discord.User=None, reason=None):
#if member == None or member == ctx.message.author:
#await ctx.channel.send("You cannot ban yourself")
#return
#if reason == None:
#reason = "for being a jerk!"
#message = f"you have been banned from {ctx.guild.name} for {reason}"
#await member.send(message)
#await ctx.channel.send(f"{member} is banned!")

async def ban(ctx, user: discord.Member, *, reason=None):
    await user.ban(reason=reason)
    await ctx.send(f"{user} have been banned sucessfully")
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user} have been unbanned successfully")
            return
#############################################
bot.run('TOKEN_HERE')
