import aiosqlite
import asyncio

from update_lists import DATABASE

async def get_teams():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT Team FROM LJLInfo") as cursor:
            teams = await cursor.fetchall()
            return {
                'teams': ['All'] + list(dict.fromkeys([team[0].strip() for team in teams]))
                }

async def get_team_members(team: str):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT Name, Twitter, StreamName, Link, Platform, IsLive FROM LJLInfo WHERE Team = ?", (team,)) as cursor:
            result = await cursor.fetchall()
            if result is not None:
                member = list()
                count = 0
                for row in result:
                    member.append({
                        "Pos": count,
                        "Name": row[0] if row[0] is not None else 'None',
                        "Twitter": row[1] if row[1] is not None else 'None',
                        "StreamName": row[2] if row[2] is not None else 'None',
                        "Link": row[3] if row[3] is not None else 'None',
                        "Platform": row[4] if row[4] is not None else 'None',
                        "Status": row[5] if row[5] is not None else 'None'
                    })
                    count += 1
                return {'players': member}
            else:
                return None

async def get_all_players():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT Name, Twitter, StreamName, Link, Platform, IsLive FROM LJLInfo") as cursor:
            result = await cursor.fetchall()
            if result is not None:
                member = list()
                count = 0
                for row in result:
                    member.append({
                        "Pos": count,
                        "Name": row[0] if row[0] is not None else 'None',
                        "Twitter": row[1] if row[1] is not None else 'None',
                        "StreamName": row[2] if row[2] is not None else 'None',
                        "Link": row[3] if row[3] is not None else 'None',
                        "Platform": row[4] if row[4] is not None else 'None',
                        "Status": row[5] if row[5] is not None else 'None'
                    })
                    count += 1
                return {'players': member}
            else:
                return None
