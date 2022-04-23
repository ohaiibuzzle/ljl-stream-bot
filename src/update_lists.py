from typing_extensions import runtime
from discord.ext import commands, tasks
import discord
import aiosqlite
import twitch
import asyncio
import mildom
import aiohttp
from bs4 import BeautifulSoup
import time
import io
import configparser
import datetime, pytz
import pickledb

from colored_output import colors

SECRETS = "runtime/config.ini"
PERSIST_DB = "runtime/persist.json"
DATABASE = "runtime/links.db"

config = configparser.ConfigParser()
config.read(SECRETS)

key = config["Secrets"]["twitch_client_id"]
secret = config["Secrets"]["twitch_client_secret"]
msg_channel = int(config["Secrets"]["msg_channel_id"])

persist_db = pickledb.load(PERSIST_DB, True)


class UpdatePlayersStatus(commands.Cog):
    fallback = "?fallback=https://source.boringavatars.com/beam/400/LnlyHikikomori?colors=55CDFC%2CF7A8B8%2CFFFFFF%2CF7A8B8%2C55CDFC"

    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        if persist_db.get("was_active"):
            self.update_loop.start()
        # self.db = sqlite3.connect(DATABASE)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def startUpdate(self, ctx, seconds=None):
        if seconds is not None:
            self.update_loop.change_interval(seconds=seconds)
        self.update_loop.start()
        persist_db.set("was_active", True)
        await ctx.send("Stream alert started...")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stopUpdate(self, ctx):
        persist_db.set("was_active", False)
        self.update_loop.stop()
        self.update_loop.cancel()
        await ctx.send("Stream alert stopped")

    @tasks.loop(seconds=300)
    async def update_loop(self):
        channel = discord.utils.find(
            lambda c: c.id == msg_channel, self.client.get_all_channels()
        )
        print("Checking...")
        start_time = time.time()
        helix = twitch.Helix(key, secret)
        async with aiosqlite.connect(DATABASE) as db:
            q = await db.execute(
                """SELECT Name, StreamName, IsLive, Link, Platform, Twitter FROM LJLInfo"""
            )
            async for player in q:
                embed_thumbnail = (
                    "https://unavatar.io/twitter/" + player[5] + self.fallback
                    if player[5]
                    else None
                )
                if player[4] == "Twitch":
                    (
                        status,
                        stream_title,
                        stream_thumbnail,
                    ) = await UpdatePlayersStatus.async_check_live_twitch_player(
                        helix, player[1]
                    )
                    if status is None:
                        continue
                    # print(f"{player[0]}: {status}")
                    if status and player[2] == 0:
                        embed, thumb_file = await UpdatePlayersStatus.live_embed(
                            player[0],
                            player[3],
                            player[4],
                            "https://twitch.tv/favicon.ico",
                            stream_title,
                            stream_thumbnail,
                            embed_thumbnail,
                        )
                        if thumb_file:
                            try:
                                await channel.send(embed=embed, file=thumb_file)
                            except discord.errors.DiscordException as e:
                                print(f"{colors.FAIL} Discord exception: {e}")
                                continue
                        else:
                            try:
                                await channel.send(embed=embed)
                            except discord.errors.DiscordException as e:
                                print(f"{colors.FAIL} Discord exception: {e}")
                                continue
                        await db.execute(
                            """UPDATE LJLInfo SET IsLive = 1 WHERE StreamName=:streamName AND Platform=:platform""",
                            {"streamName": player[1], "platform": player[4]},
                        )
                        await db.commit()
                    elif not status and player[2] == 1:
                        await db.execute(
                            """UPDATE LJLInfo SET IsLive = 0 WHERE StreamName=:streamName AND Platform=:platform""",
                            {"streamName": player[1], "platform": player[4]},
                        )
                        await db.commit()
                elif player[4] == "Mildom":
                    (
                        status,
                        stream_title,
                        stream_thumbnail,
                    ) = await UpdatePlayersStatus.async_check_live_mildom_player(
                        int(player[1])
                    )
                    if status is None:
                        continue
                    # print(f"{player[0]}: {status}")
                    if status and player[2] == 0:
                        embed, thumb_file = await UpdatePlayersStatus.live_embed(
                            player[0],
                            player[3],
                            player[4],
                            "https://www.mildom.com/assets/mildom_logo_big.png",
                            stream_title,
                            stream_thumbnail,
                            embed_thumbnail,
                        )
                        if thumb_file:
                            try:
                                await channel.send(embed=embed, file=thumb_file)
                            except discord.errors.DiscordException as e:
                                print(f"{colors.FAIL} Discord exception: {e}")
                                continue
                        else:
                            try:
                                await channel.send(embed=embed)
                            except discord.errors.DiscordException as e:
                                print(f"{colors.FAIL} Discord exception: {e}")
                                continue
                        await db.execute(
                            """UPDATE LJLInfo SET IsLive = 1 WHERE StreamName=:streamName AND Platform=:platform""",
                            {"streamName": player[1], "platform": player[4]},
                        )
                        await db.commit()
                    elif not status and player[2] == 1:
                        await db.execute(
                            """UPDATE LJLInfo SET IsLive = 0 WHERE StreamName=:streamName AND Platform=:platform""",
                            {"streamName": player[1], "platform": player[4]},
                        )
                        await db.commit()
                elif player[4] == "OPENREC.tv":
                    (
                        status,
                        stream_title,
                        stream_thumbnail,
                    ) = await UpdatePlayersStatus.check_live_openrectv_player(player[1])
                    if status is None:
                        continue
                    # print(f"{player[0]}: {status}")
                    if status and player[2] == 0:
                        embed, thumb_file = await UpdatePlayersStatus.live_embed(
                            player[0],
                            player[3],
                            player[4],
                            "https://www.openrec.tv/favicon.ico",
                            stream_title,
                            stream_thumbnail,
                            embed_thumbnail,
                        )
                        if thumb_file:
                            try:
                                await channel.send(embed=embed, file=thumb_file)
                            except discord.errors.DiscordException as e:
                                print(f"{colors.FAIL} Discord exception: {e}")
                                continue
                        else:
                            try:
                                await channel.send(embed=embed)
                            except discord.errors.DiscordException as e:
                                print(f"{colors.FAIL} Discord exception: {e}")
                                continue
                        await db.execute(
                            """UPDATE LJLInfo SET IsLive = 1 WHERE StreamName=:streamName AND Platform=:platform""",
                            {"streamName": player[1], "platform": player[4]},
                        )
                        await db.commit()
                    elif not status and player[2] == 1:
                        await db.execute(
                            """UPDATE LJLInfo SET IsLive = 0 WHERE StreamName=:streamName AND Platform=:platform""",
                            {"streamName": player[1], "platform": player[4]},
                        )
                        await db.commit()
                else:
                    continue
        print("Done.")
        print(f"Took {(time.time()-start_time)}s")
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            persist_db.set,
            "last_update",
            f"{str(datetime.datetime.now(pytz.timezone('Asia/Tokyo')))[:-16]} JST",
        )
        print(
            f"Iteration {colors.OKGREEN}{self.update_loop.current_loop}{colors.ENDC} completed. Next check scheduled at {colors.OKGREEN}{self.update_loop.next_iteration}{colors.ENDC}"
        )

    @update_loop.before_loop
    async def update_loop_wait_ready(self):
        print("Waiting for connection")
        return await self.client.wait_until_ready()

    @staticmethod
    async def async_check_live_twitch_player(
        helix: twitch.Helix, streamName: str
    ) -> bool:
        loop = asyncio.get_event_loop()
        try:
            return await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    UpdatePlayersStatus.check_live_twitch_player,
                    helix,
                    streamName,
                ),
                timeout=15.0,
            )
        except asyncio.TimeoutError:
            print(f"Stream {streamName} check {colors.WARNING}timed out.{colors.ENDC}")
            return None, None, None
        except Exception as e:
            print(
                f"{colors.FAIL}Exception while checking stream {streamName}: {e} {colors.ENDC}"
            )
            return None, None, None

    @staticmethod
    async def async_check_live_mildom_player(streamName: str) -> bool:
        loop = asyncio.get_event_loop()
        try:
            return await asyncio.wait_for(
                loop.run_in_executor(
                    None, UpdatePlayersStatus.check_live_mildom_player, streamName
                ),
                timeout=15.0,
            )
        except asyncio.TimeoutError:
            print(f"{streamName} check {colors.WARNING}timed out.{colors.ENDC}")
            return None, None, None
        except Exception as e:
            print(f"Exception while checking stream {streamName}: {e}")
            return None, None, None

    @staticmethod
    def check_live_twitch_player(helix: twitch.Helix, streamName: str) -> bool:
        user = helix.user(streamName)
        if user.is_live:
            print(f"Stream {streamName} {colors.OKGREEN}is online{colors.ENDC}")
            return (
                user.is_live,
                user.stream.title,
                user.stream.thumbnail_url.format(width=1280, height=720),
            )
        else:
            print(f"Stream {streamName} {colors.OKBLUE}is offline{colors.ENDC}")
            return user.is_live, None, None

    @staticmethod
    def check_live_mildom_player(streamName: int) -> bool:
        user = mildom.User(streamName)
        if user.is_live:
            print(f"Stream {streamName} {colors.OKGREEN}is online{colors.ENDC}")
            return user.is_live, user.latest_live_title, user.latest_live_thumbnail
        else:
            print(f"Stream {streamName} {colors.OKBLUE}is offline{colors.ENDC}")
            return user.is_live, None, None

    @staticmethod
    async def check_live_openrectv_player(streamName: str) -> bool:
        endpoint = "https://www.openrec.tv/user/"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        }
        timeout = aiohttp.ClientTimeout(total=15)

        try:
            async with aiohttp.ClientSession(
                timeout=timeout, headers=header
            ) as session:
                resp = await session.get(endpoint + streamName)
                soup = BeautifulSoup(await resp.read(), features="html.parser")
                # print(soup)
                live_span_tag = soup.find("div", {"class": "c-content__title"})
                if live_span_tag:
                    if live_span_tag.text == "Live":
                        print(
                            f"Stream {streamName} {colors.OKGREEN}is online{colors.ENDC}"
                        )
                        img_link = soup.find(
                            "img", {"class": "p-animation__thumbnail"}
                        )["src"]
                        title = soup.find("a", {"class": "c-thumbnailVideo__title"})[
                            "title"
                        ]
                        return live_span_tag.text == "Live", title, img_link
                print(f"Stream {streamName} {colors.OKBLUE}is offline{colors.ENDC}")
                return False, None, None
        except Exception as e:
            print(f"Exception while checking stream {streamName}: {e}")
            return None, None, None

    @staticmethod
    async def live_embed(
        player: str,
        stream_link: str,
        platform: str,
        footer_icon: str,
        title: str,
        thumbnail_url: str,
        embed_thumbnail: str = None,
    ) -> discord.Embed:
        to_return = discord.Embed(
            title=f"{player} went online on {platform}", url=stream_link
        )
        thumbnail_file = None
        if embed_thumbnail:
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                thumbnail_rq = await session.get(embed_thumbnail)
                thumbnail_bin = io.BytesIO(await thumbnail_rq.read())
                thumbnail_bin.seek(0)
                thumbnail_file = discord.File(thumbnail_bin, "thumbnail.jpg")
                to_return.set_thumbnail(url="attachment://thumbnail.jpg")
        to_return.set_image(url=thumbnail_url)
        to_return.add_field(name="Title", value=title, inline=False)
        to_return.add_field(name="Link", value=stream_link, inline=False)
        to_return.set_footer(text=platform, icon_url=footer_icon)
        return to_return, thumbnail_file


def setup(client: commands.Bot):
    client.add_cog(UpdatePlayersStatus(client))
