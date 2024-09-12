import os
import discord
import pytz
import contextlib
import asyncio
import random

from datetime import datetime, timedelta
from discord.ext import commands
from discord.ui import Button, View, Select, Modal, InputText
from discord import utils

from db.database import *
from db.tokens import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-', intents=intents)
bot.remove_command('help')
users = []


def check_category():
    async def predicate(ctx):
        return ctx.channel.category_id == category_id
    return commands.check(predicate)

def check_category_teams():
    async def predicate(ctx):
        return ctx.channel.category_id == category_team_id
    return commands.check(predicate)

def channel_exception(channel):
    if channel == channel_id_create:
        return True
    return False


def delete_channel(channel_id):
    delete_members(channel_id)
    delete_channel_by_id(channel_id)
    channel = bot.get_channel(channel_id)
    if channel:
        return channel.delete(reason="Empty Temp Channel")


def delete_teams_channel(channel_id):
    channel = bot.get_channel(channel_id)
    if channel:
        return channel.delete(reason="Empty Temp Channel")


def randomize_groups():
    random.shuffle(users)
    middle = len(users) // 2
    team1 = users[:middle]
    team2 = users[middle:]
    return team1, team2


def embeds_random(team1, team2):
    number_of_players = str(len(users))
    embed = discord.Embed(title="**Team Generator**", colour=0xFF0000)
    embed.set_author(name="ТИМА ДОЛБоЕБОВ!",
                     icon_url="https://cdn.discordapp.com/avatars/924881929877217280/15ba66a5e22515fd468608d581da5118.png?size=1024")
    embed.add_field(name=f"Участников: {number_of_players}.", value="", inline=False)
    embed.add_field(name="Team 1:", value="\n".join([member.mention for member in team1]), inline=True)
    embed.add_field(name="Team 2:", value="\n".join([member.mention for member in team2]), inline=True)
    embed.set_image(url="https://raw.githubusercontent.com/dblgq/jdmcars/main/headerr.png")
    embed.set_footer(text="gl hf")
    return embed


def embeds_start():
    number_of_players = str(len(users))
    embed = discord.Embed(colour=0xFF0000)
    embed.set_author(name="Team Generator",
                     icon_url="https://cdn.discordapp.com/avatars/924881929877217280/15ba66a5e22515fd468608d581da5118.png?size=1024")
    embed.add_field(name=f"Участников: {number_of_players}.", value="", inline=False)
    field_value = ""
    for index, user in enumerate(users, 1):
        field_value += f"{index}: {user.mention}\n"
    embed.add_field(name="Игроки:", value=field_value, inline=False)
    return embed


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return

    if after.channel is not None:
        if after.channel.id == channel_id_create:
            await auto_room(member, after.channel)
        else:
            if after.channel.category_id == category_id:
                insert_member(after.channel.id, member.id, 1, 1)

    with contextlib.suppress(Exception):
        guild = bot.get_guild(guild_id)
        for category in guild.categories:
            if category.id == category_id:
                for channel in category.voice_channels:
                    if not channel.members and not channel_exception(channel.id):
                        if not channel.id == channel_id_create:
                            await delete_channel(channel.id)

    with contextlib.suppress(Exception):
        guild = bot.get_guild(guild_id)
        for category in guild.categories:
            if category.id == category_team_id:
                for channel in category.voice_channels:
                    if not channel.members and not channel_exception(channel.id):
                        if not channel.id == wait_room:
                            await delete_teams_channel(channel.id)


async def auto_room(member, channel):
    guild = bot.get_guild(guild_id)
    cat = discord.utils.get(guild.categories, id=category_id)
    channelName = member.display_name + "'s Рума"
    newChannel = await member.guild.create_voice_channel(channelName, overwrites={
        member.guild.default_role: discord.PermissionOverwrite(connect=True, speak=True),
        member: discord.PermissionOverwrite(manage_channels=True, connect=True, speak=True)
    },
                                                      category=cat, user_limit=5, rtc_region=russia)

    # Записываем созданный канал в базу данных
    insert_channel(newChannel.id, member.id, 1, 5)

    await member.move_to(newChannel, reason='Temp Channel')


@bot.event
async def on_ready():
    time_now = datetime.now(tz=pytz.timezone('Asia/Singapore'))
    login_time = time_now.strftime('%d-%m-%Y %I:%M %p')
    print("-----------------")
    print('Logged in as {0} at {1}'.format(bot.user.name, login_time))
    print("-----------------")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")
bot.run(TOKEN)
