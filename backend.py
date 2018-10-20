#run the code if you want to update the database
import csv
import sqlite3
import os

# Database Connection Info
conn = sqlite3.connect('csv_db.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Csv;
DROP TABLE IF EXISTS Field;


CREATE TABLE Csv(
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    filename    TEXT UNIQUE
);
''')
# Assign path to  files

folder = 'TWEETS_CSV'
files = os.listdir(folder)
for file in files:
    if file.endswith('.csv'):
        csv_file= os.path.join(folder,file)
        fh=open(csv_file,'r')
        csv_data= csv.reader(fh)
        names_list = next(csv_data)
        break
table_name = 'Field'

#insert_query='''UPDATE Field SET (%s) ON Field.csv_id= Csv.id  WHERE Csv.filename= ?'''%(', '.join('{}=%s'.format(name) for name in names_list))
#insert_query='''UPDATE Field SET %s WHERE (SELECT id FROM Csv WHERE filename = ? )=csv_id '''%(', '.join('{}=?'.format(name) for name in names_list)),(file,)'''UPDATE Field SET %s WHERE (SELECT id FROM Csv WHERE filename = ? )=csv_id '''%(', '.join('{}=?'.format(name) for name in names_list))
#print(insert_query)
for file in files:
         if file.endswith('.csv'):
             #print(file)
             cur.execute('''INSERT INTO Csv(filename) VALUES(?)''',(file,))
             cur.execute('SELECT id FROM Csv WHERE filename = ? ', (file, ))
             csv_id = cur.fetchone()[0]
             print(csv_id)
             cur.execute("""CREATE TABLE IF NOT EXISTS """ + table_name + " (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,csv_id INTEGER," + " TEXT,".join(names_list) + " TEXT)")
             csv_files = os.path.join(folder, file)
             fh= open(csv_files,'r')
             csv_data = csv.reader(fh)
             names=next(csv_data) #throw away firs
             print(csv_id)
             print(file)

             for row in csv_data:
                 cur.execute('INSERT INTO Field(csv_id) VALUES(?)',(csv_id,) )
             cur.executemany('''UPDATE Field SET %s WHERE csv_id IN (SELECT id FROM Csv WHERE filename = 'tweets.csv' ) '''%(', '.join('{}=?'.format(name) for name in names_list)),csv_data)
cur.close()

conn.commit()

conn.close()

print("Script has successfully run!")
