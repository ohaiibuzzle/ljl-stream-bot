from aiohttp import web
import aiohttp_jinja2
from discord.ext import commands, tasks
import os
import aiosqlite
import jinja2
import pickledb
import asyncio

from update_lists import PERSIST_DB

app = web.Application()
routes = web.RouteTableDef()

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('src/web_interface/templates'))

PERSIST = 'runtime/persist.json'
DATABASE = 'runtime/links.db'

persist_db = pickledb.load(PERSIST, False) 

class WebInterface(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.web_server.start()

        @routes.get('/')
        async def WebInterfaceHandler(request):
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, persist_db._loaddb)
            async with aiosqlite.connect(DATABASE) as db:
                async with db.execute_fetchall('''SELECT Name, Platform, StreamName, Link, Twitter, IsLive FROM LJLInfo''') as content:
                    context = {
                        'last_update': persist_db.get('last_update'),
                        'players' : content
                    }
                    response = aiohttp_jinja2.render_template('main.jinja2', request, context=context)
                    return response

        self.webserver_port = os.environ.get('PORT', 5000)
        app.add_routes(routes)

    @tasks.loop()
    async def web_server(self):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host='0.0.0.0', port=self.webserver_port)
        await site.start()

    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.client.wait_until_ready()

def setup(client: commands.Bot):
    client.add_cog(WebInterface(client))
