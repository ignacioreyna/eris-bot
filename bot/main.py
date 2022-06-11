import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import random

import buttons, keep_alive


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True


bot = commands.Bot(command_prefix=';', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith(';ping'):
        await message.channel.send('Pong!')
    await bot.process_commands(message)


@bot.event
async def on_member_join(member: discord.Member):
    channel = member.guild.system_channel
    content = f'Hola <@{member.id}>! Que rol vas a tener?'
    await channel.send(content, view=buttons.AskRole(member, content))


def get_members_in_voice_channel(ctx):
    requester = ctx.message.author.id
    channel = ctx.guild.get_member(requester).voice.channel
    connected_users = list(channel.voice_states.keys())
    return requester, connected_users


@bot.command()
async def daily(ctx):
    try:
        _, connected_users = get_members_in_voice_channel(ctx)
        random.shuffle(connected_users)
        await ctx.send(f'Momento daily! Va el orden:' )
        await ctx.send('\n'.join([f'{idx+1} - <@{member}>' for idx, member in enumerate(connected_users)]))
    except AttributeError as e:
        await ctx.send(f'No estas en un canal de voz!')


bot.run(TOKEN)
