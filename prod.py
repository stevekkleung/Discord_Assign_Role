# required packages
import os
from dotenv import load_dotenv

# required for discord bots
import discord
#import asyncio
#from discord import app_commands
from discord.ext import commands

# required hotfix
import nest_asyncio
nest_asyncio.apply()

# parameters for bot
INPUT_TEXT = 'names_and_roles.txt'

# bot token
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN_assign_role")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is running!')

@bot.command()
async def role(ctx):
    # find all unique roles from txt
    roles = set()
    with open(INPUT_TEXT, 'r') as f:
        next(f)
        lines = f.readlines()
        for line in lines:
            roles.add(line.split(',')[1].strip())
    f.close()

    # loop all roles
    for role in roles:
        # list of names for each role
        names = set()
        with open(INPUT_TEXT,'r') as f:
            next(f)
            lines = f.readlines()
            for line in lines:
                if line.split(',')[1].strip()==role:
                    names.add(line.split(',')[0].strip())
        f.close()

        # convert name from text to object
        members = set()
        converter = commands.MemberConverter()
        for name in names:
            try:
                member = await converter.convert(ctx, name)
                members.add(member)
            except:
                pass

        # convert role from text to object
        role = discord.utils.get(ctx.guild.roles, name=role)

        # find names with the role
        existing_members = set()
        for i in role.members:
            existing_members.add(i)

        add_role_list = list(members - existing_members)
        remove_role_list = list(existing_members - members)

        # add role
        for i in add_role_list:
            try:
                await i.add_roles(role)
            except:
                pass

        # remove role
        for i in remove_role_list:
            try:
                await i.remove_roles(role)
            except:
                pass

bot.run(BOT_TOKEN)