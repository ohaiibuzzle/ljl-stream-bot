import discord
from discord.ext import commands
import os, sqlite3

if not os.path.isdir('runtime'):
    os.mkdir('runtime')
    print("Please populate the /runtime directory with your credentials!")
    exit(0)

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

client.load_extension('update_lists')
#client.load_extension('web_interface.web_interface')

key = ''
with open('runtime/discord.key', 'r') as keyfile:
    key = keyfile.readline()
client.run(key)