from aiohttp import web
from discord.ext import commands, tasks
import os
import pickledb

from . import db_interface

from update_lists import PERSIST_DB, DATABASE

app = web.Application()
routes = web.RouteTableDef()

persist_db = pickledb.load(PERSIST_DB, False) 

class WebInterface(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.web_server.start()

        @routes.get('/api/last_update')
        async def last_update(request):
            return web.json_response({'time': persist_db.get('last_update')})

        @routes.get('/api/teams')
        async def get_teams(request):
            return web.json_response(await db_interface.get_teams())

        @routes.get('/api/team/{team}')
        async def get_team_members(request):
            if request.match_info['team'] == 'All':
                return web.json_response(await db_interface.get_all_players())
            return web.json_response(await db_interface.get_team_members(request.match_info['team']))

        @routes.get('/')
        async def index(request):
            return web.HTTPPermanentRedirect('/index.html')

        self.webserver_port = os.environ.get('PORT', 5000)
        app.add_routes(routes)
        app.router.add_static('/', f'{os.path.dirname(db_interface.__file__)}/content')

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
