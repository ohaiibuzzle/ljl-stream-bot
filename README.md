# ljl-stream-bot

Quick 'n' (sorta) clunky stream monitor for OpenREC, Twitch & Mildom

Hot Instructions:
- Place `discord.key` and `twitch.key` into the `runtime` directory (created after first launch)
- Create a SQLite3 database with something like
```
CREATE TABLE "LJLInfo" (
	"Name"	TEXT NOT NULL,
	"Platform"	TEXT DEFAULT NULL,
	"StreamName"	TEXT DEFAULT NULL,
	"Link"	TEXT DEFAULT NULL,
	"IsLive"	INTEGER DEFAULT 0,
	PRIMARY KEY("Name")
)
```
- Populate data
- Change the default channel (`src/update_lists.py`)
- At this point the bot should be ready to blast' updates.

![BADOOM](https://media1.tenor.com/images/a5200ff8939402e4e2bbda3a8107d2b1/tenor.gif)
