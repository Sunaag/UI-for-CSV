#run the code if you want to update the database
import csv
import sqlite3
import os
import itertools

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
csv_list=[]
cols= 'csv_id,'+','.join(names_list)
new_cols= cols.split(',')
placeholders='?,'+','.join(['?']*len(names_list))
insert_query=''' INSERT INTO Field (%s) VALUES (%s) '''%(cols,placeholders)
print(''.join(tuple(cols)))
for file in files:
         if file.endswith('.csv'):
             #print(file)
             cur.execute('''INSERT INTO Csv(filename) VALUES(?)''',(file,))
             cur.execute('SELECT id FROM Csv WHERE filename = ? ', (file, ))
             csv_id = cur.fetchone()[0]
             print(csv_id)
             cur.execute("""CREATE TABLE IF NOT EXISTS """ + table_name + " (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,csv_id INTEGER," + " TEXT,".join(names_list) + " TEXT)")
             csv_list.append(csv_id)

             csv_files = os.path.join(folder, file)
             fh= open(csv_files,'r')
             csv_data = csv.reader(fh)
             names=next(csv_data) #throw away first
             #print(tuple(csv_data))
             new=''.join(tuple(cols))
             print(new)

            # csv_full = zip(itertools.repeat(csv_id,len(list(csv_data)),csv_data))
             #print(csv_full)
             #print(tuple(new_cols))
             #for v,k in zip(itertools.repeat(csv_id,len(list(csv_data))),csv_data):
            #     print(v,k)

             for row in csv_data:
                 cur.execute(insert_query,new)

#print(csv_list)




cur.close()

conn.commit()

conn.close()

print("Script has successfully run!")
