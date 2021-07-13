from os import stat
from discord import client
from discord.ext import commands, tasks
import discord
import sqlite3, aiosqlite
from discord.ext.commands.core import check
import twitch
import asyncio
import mildom
import aiohttp
from bs4 import BeautifulSoup
import time

from twitch.helix.models import stream


DATABASE = 'runtime/links.db'

class UpdatePlayersStatus(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        #self.db = sqlite3.connect(DATABASE)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def startUpdate(self, ctx, seconds = None):
        if seconds is not None:
            self.update_loop.change_interval(seconds=seconds)
        self.update_loop.start()
        await ctx.send("Stream alert started...")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stopUpdate(self, ctx):
        self.update_loop.stop()
        await ctx.send("Stream alert stopped")    

    @tasks.loop(seconds=300)
    async def update_loop(self):
        channel = discord.utils.find(lambda c: c.id == 864516198384664636, self.client.get_all_channels())
        print("Checking...")
        start_time = time.time()
        async with aiosqlite.connect(DATABASE) as db:
            q = await db.execute('''SELECT Name, StreamName, IsLive, Link, Platform FROM LJLInfo''')
            async for player in q:
                if (player[4] == 'Twitch'):
                    status, stream_title, stream_thumbnail = await UpdatePlayersStatus.async_check_live_twitch_player(player[1])
                    #print(f"{player[0]}: {status}")
                    if status and player[2] == 0:
                        await channel.send(embed=UpdatePlayersStatus.live_embed(player[0], player[3], player[4], "https://twitch.tv/favicon.ico", stream_title, stream_thumbnail))
                        await db.execute('''UPDATE LJLInfo SET IsLive = 1 WHERE StreamName=:streamName''', {'streamName': player[1]})
                        await db.commit()
                    elif (not status and player[2] == 1):
                        await db.execute('''UPDATE LJLInfo SET IsLive = 0 WHERE StreamName=:streamName''', {'streamName': player[1]})
                        await db.commit()
                elif (player[4] == 'Mildom'):
                    status, stream_title, stream_thumbnail = await UpdatePlayersStatus.async_check_live_mildom_player(int(player[1]))
                    #print(f"{player[0]}: {status}")
                    if status and player[2] == 0:
                        await channel.send(embed=UpdatePlayersStatus.live_embed(player[0], player[3], player[4], "https://www.mildom.com/assets/mildom_logo_big.png", stream_title, stream_thumbnail))
                        await db.execute('''UPDATE LJLInfo SET IsLive = 1 WHERE StreamName=:streamName''', {'streamName': player[1]})
                        await db.commit()
                    elif (not status and player[2] == 1):
                        await db.execute('''UPDATE LJLInfo SET IsLive = 0 WHERE StreamName=:streamName''', {'streamName': player[1]})
                        await db.commit()
                elif (player[4] == 'OPENREC.tv'):
                    status, stream_title, stream_thumbnail = await UpdatePlayersStatus.check_live_openrectv_player(player[1])
                    #print(f"{player[0]}: {status}")
                    if status and player[2] == 0:
                        await channel.send(embed=UpdatePlayersStatus.live_embed(player[0], player[3], player[4], "https://www.openrec.tv/favicon.ico", stream_title, stream_thumbnail))
                        await db.execute('''UPDATE LJLInfo SET IsLive = 1 WHERE StreamName=:streamName''', {'streamName': player[1]})
                        await db.commit()
                    elif (not status and player[2] == 1):
                        await db.execute('''UPDATE LJLInfo SET IsLive = 0 WHERE StreamName=:streamName''', {'streamName': player[1]})
                        await db.commit()
                else:
                    continue
        print("Done.")
        print(f"Took {(time.time()-start_time)}s")

    @staticmethod
    async def async_check_live_twitch_player(streamName: str) -> bool:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, UpdatePlayersStatus.check_live_twitch_player, streamName)

    @staticmethod
    async def async_check_live_mildom_player(streamName: str) -> bool:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, UpdatePlayersStatus.check_live_mildom_player, streamName)


    @staticmethod
    def check_live_twitch_player(streamName: str) -> bool:
        key = ''
        secret = ''
        with open('runtime/twitch.key', 'r') as keyf:
            key = keyf.readline().strip()
            secret = keyf.readline().strip()
        helix = twitch.Helix(key, secret)
        user = helix.user(streamName)
        if user.is_live:
            return user.is_live, user.stream.title, user.stream.thumbnail_url.format(width=1280, height=720)
        else:
            return user.is_live, None, None
        
    @staticmethod
    def check_live_mildom_player(streamName: int) -> bool:
        user = mildom.User(streamName)
        if user.is_live:
            return user.is_live, user.latest_live_title, user.latest_live_thumbnail
        else:
            return user.is_live, None, None


    @staticmethod
    async def check_live_openrectv_player(streamName: str) -> bool:
        endpoint = 'https://www.openrec.tv/user/'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
        timeout = aiohttp.ClientTimeout(total=15)

        async with aiohttp.ClientSession(timeout=timeout, headers=header) as session:
            resp = await session.get(endpoint + streamName)
            soup = BeautifulSoup(await resp.read(), features="html.parser")
            #print(soup)
            live_span_tag = soup.find('div', {'class': 'c-content__title'})
            if live_span_tag:
                if live_span_tag.text == 'Live':
                    img_link = soup.find('img', {'class': 'p-animation__thumbnail'})['src']
                    title = soup.find('a', {'class': 'c-thumbnailVideo__title'})['title']
                    return live_span_tag.text == 'Live', title, img_link
            return False, None, None

    @staticmethod
    def live_embed(player: str, stream_link: str, platform: str, footer_icon: str, title: str, thumbnail_url: str) -> discord.Embed:
        to_return = discord.Embed(title=f"{player} went online on {platform}", url=stream_link)
        to_return.set_image(url=thumbnail_url)
        to_return.add_field(
            name="Title",
            value=title,
            inline=False
        )
        to_return.add_field(
            name="Link",
            value=stream_link,
            inline=False
        )
        to_return.set_footer(text=platform, icon_url=footer_icon)
        return to_return

def setup(client: commands.Bot):
    client.add_cog(UpdatePlayersStatus(client))

    