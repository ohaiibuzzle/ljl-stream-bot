from aiohttp import web
from aiohttp.web_response import Response
import aiohttp_jinja2
from aiosqlite import context
from discord.ext import commands, tasks
import discord
import os
import aiosqlite
import aiohttp
import jinja2

app = web.Application()
routes = web.RouteTableDef()

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('src/web_interface/templates'))

DATABASE = 'runtime/links.db'

class WebInterface(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.web_server.start()

        @routes.get('/')
        async def WebInterfaceHandler(request):
            async with aiosqlite.connect(DATABASE) as db:
                async with db.execute_fetchall('''SELECT Name, Platform, StreamName, Link, Twitter, IsLive FROM LJLInfo''') as content:
                    context = {
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
