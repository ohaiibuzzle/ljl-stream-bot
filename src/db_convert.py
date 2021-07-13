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

for row in link_reader:
    db.execute('''INSERT INTO LJLInfo (Name, Platform, StreamName, Link) VALUES
    (:name, :platform, :streamname, :link)''',
    {'name': row[3], 'platform': row[6], 'streamname': row[7], 'link': row[8]})

db.commit()