from discord.ext import commands
import os
import configparser

if not os.path.isdir("runtime"):
    os.mkdir("runtime")
    config = configparser.ConfigParser()

    config["Secrets"] = {
        "discord_key": "",
        "msg_channel_id": "",
        "twitch_client_id": "",
        "twitch_client_secret": "",
    }

    with open("runtime/config.ini", "w+") as conf_file:
        config.write(conf_file)

    print("Please populate the /runtime directory with your credentials!")
    exit(0)

client = commands.Bot(command_prefix=".", help_command=None)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


client.load_extension("update_lists")
client.load_extension("web_interface.web_interface")

config = configparser.ConfigParser()
config.read("runtime/config.ini")
key = config["Secrets"]["discord_key"]
client.run(key)
