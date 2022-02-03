import os
import csv
import sqlite3

STREAMER_LINKS = 'runtime/links.csv'
DATABASE = 'runtime/links.db'

if (not os.path.isdir('runtime')):
    os.mkdir('runtime')

links = open(STREAMER_LINKS, "r")
link_reader = csv.reader(links)

db = sqlite3.connect(DATABASE)

db.execute('''DROP TABLE IF EXISTS "LJLInfo"''')
db.execute('''CREATE TABLE "LJLInfo" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
	"Name"	TEXT NOT NULL,
	"Platform"	TEXT DEFAULT NULL,
	"StreamName"	TEXT DEFAULT NULL,
	"Link"	TEXT DEFAULT NULL,
    "Twitter"   TEXT DEFAULT NULL,
	"IsLive"	INTEGER DEFAULT 0
)''')

for row in link_reader:
    print(row)
    db.execute('''INSERT INTO LJLInfo (Name, Twitter, Platform, StreamName, Link) VALUES
    (:name, :twitter, :platform, :streamname, :link)''',
    {'name': row[1] if len(row[1].strip()) != 0 else None, 
    'twitter': row[2] if len(row[2].strip()) != 0 else None, 
    'platform': row[3] if len(row[3].strip()) != 0 else None, 
    'streamname': row[4] if len(row[4].strip()) != 0 else None, 
    'link': row[5] if len(row[5].strip()) != 0 else None})

db.commit()