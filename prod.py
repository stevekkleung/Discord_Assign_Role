#######################################################################
# BonFire Discord Bot: assign_role
# Purpose: Read-in BonFire API: discord-role-assign
#          1) Assign Property-Roles to userDiscordId
#          2) Remove Roles if not in API (currently disabled)
######################################################################
# Bot triggers once every 12 hours
######################################################################

# required packages
import os
from dotenv import load_dotenv

import requests
import json
import discord
import asyncio
# from discord import app_commands
from discord.ext import commands, tasks

# required hotfix for
import nest_asyncio
nest_asyncio.apply()

# API URL
url = "https://app.bonfire.capital/api/discord-role-assign"  

# read discord bot token
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN_assign_role")

# Discord Server ID
serverId = 1038544563410841630 #testing server
#serverId = 986758425394425959  #production server

# Discord bot required commands
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)


# bot online message
@bot.event
async def on_ready():
    print('------------------------')
    print(f'{bot.user} is now running! (BOT ID: {bot.user.id}) \n')
    role_loop.start()

#@tasks.loop(seconds=30)
@tasks.loop(hours=12)
async def role_loop():
    await bot.assign_role()

# assign discordIds to discordRoles based on the API
@bot.event
async def assign_role():
    # define guild with server ID
    guild = bot.get_guild(serverId)

    # read API and create a json file
    API_json = json.loads(requests.get(url).text)    
    
    # find all the unique discord roles from API
    discordRoles = set()
    for i in range(len(API_json)):
        if API_json[i]['discordRole']!=None:
            discordRoles.add(API_json[i]['discordRole'])
    print(f'checkpoint 1: print unique discordRoles from API: {discordRoles}')

    # loop through all of the discordRoles
    # within the API, find all of the discordIds for each of the roles
    for discordRole in discordRoles:
        userDiscordIds = set()
        for i in range(len(API_json)):
            if API_json[i]['discordRole']==discordRole and API_json[i]['userDiscordId']!=None:
                userDiscordIds.add(API_json[i]['userDiscordId'])
        print(f'checkpoint 2: for discordRole: {discordRole}, we have these discordIds: {userDiscordIds}')

        # convert discord name into member object, then put them into a list
        members = set()
        for userDiscordId in userDiscordIds:
            try:
                member = guild.get_member_named(userDiscordId)
                members.add(member)
                print(f'checkpoint 2b: userDiscordId is: {userDiscordId} & member object is {member}')
#            print(f'checkpoint 2b: {userDiscordId} & {member} data type updated')
            except:
                print(f'checkpoint 2c: {userDiscordId} exception raised')
                pass
        print(f'checkpoint 3: userDiscordIds value: {members}')

        # convert role name into role id
        role = discord.utils.get(guild.roles, name=discordRole)
        roleid = role.id
        print(f'checkpoint 4: role: {role} and roleid: {roleid}')

        # find all existing memberids in the server with the role
        existing_members = set()
        for i in role.members:
            existing_members.add(i)

        add_role_list = list(members - existing_members)
        # loop the list and add roles
        for i in add_role_list:
            print(f'checkpoint 5: member value: {i}')
            try:
                await i.add_roles(role)
                print(f'checkpoint 5b: added role {role} to {i}')
            except:
                print('checkpoint 5c: error')
                pass

'''
        remove_role_list = list(existing_members - members)
        # loop the list and remove roles
        for i in remove_role_list:
            print(f'checkpoint 5: member value: {i}')
            try:
                await i.remove_roles(role)
                print(f'checkpoint 5b: removed role {role} from {i}')
            except:
                print('checkpoint 5c: error')
                pass
'''

bot.run(BOT_TOKEN)
