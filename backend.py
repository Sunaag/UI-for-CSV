#run the code if you want to update the database
import csv
import sqlite3
import os

# Database Connection Info
conn = sqlite3.connect('csv_db.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Csv;
DROP TABLE IF EXISTS Data;


CREATE TABLE Csv (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    filename    TEXT UNIQUE
);


CREATE TABLE  Data(
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    csv_id  INTEGER,
    tweet   TEXT ,
    timestam TEXT ,
    source TEXT ,
    matter TEXT ,
    expanded_urls VARCHAR(100)

);
''')

# Assign path to  files
folder = "TWEETS_CSV"
files = os.listdir(folder)
for file in files:
         if file.endswith('.csv'):
             #print(file)
             cur.execute('''INSERT INTO Csv(filename) VALUES(?)''',(file,))
             cur.execute('SELECT id FROM Csv WHERE filename = ? ', (file, ))
             csv_id = cur.fetchone()[0]
             csv_files = os.path.join(folder, file)
             #print(csv_files)
             fh= open(csv_files,'r')
             csv_data = csv.reader(fh)
             next(csv_data) #throw away first
             for row in csv_data:
                 tweet=row[0]
                 timestam=row[1]
                 source=row[2]
                 matter=row[3]
                 expanded_urls=row[4]
                 cur.execute('''INSERT INTO Data(csv_id,tweet,timestam,source,matter,expanded_urls)
                                     VALUES (?,?,?,?,?,?)''',(csv_id,tweet,timestam,source,matter,expanded_urls))


cur.close()

conn.commit()

conn.close()

print("Script has successfully run!")
