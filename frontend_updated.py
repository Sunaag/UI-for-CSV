#run the code and select a csv file and
# select a field or more fields on UI
# output appears on command line

#UPDATED CHANGE_DROPDOWN FUNCTION
from tkinter import *
import sqlite3

class Buttons:
     def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        frame.grid(column=0,row=0, sticky=(N,W,E,S) )
        frame.pack(pady = 100, padx = 200)
        tkvar= StringVar(master)
        out=self.run_query('''SELECT filename FROM Csv''')
        choices={}
        for row in out:
            choices[row[0]] = choices.get(row[0],0)+1
            #print(choices)
        csv_files=[]
        for k,v in choices.items():
            csv_files.append(k)
        #print(csv_files)
        popupMenu = OptionMenu(frame, tkvar, *choices)
        self.label1 = Label(frame,text='CSV :')
        self.label1.grid(row=0,sticky=E)
        popupMenu.grid(row=0,column=1)
        tkvar1=StringVar(master)
        choices1={}
        out1=self.run_query('''PRAGMA table_info(Data)''' )

        for row in out1:
            if row[1].endswith('id'):
                continue
            choices1[row[1]]=choices1.get(row[1],0)+1
        datas=[]
        for k,v in choices1.items():
            datas.append(k)
        #print(datas)
        popupMenu1 = OptionMenu(frame, tkvar1, *choices1)
        self.label2 = Label(frame,text='Fields:')
        self.label2.grid(row=1,sticky=E)
        popupMenu1.grid(row=1,column=1)
    # link function to change dropdown
        def change_dropdown1(*args):
            for csv in csv_files:
                for data in datas:
                    csv_id = csv_files.index(csv)
                    if tkvar.get()==csv and tkvar1.get()==data:
                        out1=self.run_query('''SELECT [{}] FROM Data WHERE csv_id =? '''.format(data),(csv_id+1,) )
                        for row in out1:
                            print(row[0])

        tkvar1.trace('w', change_dropdown1)
     def run_query(self,query,parameters=()):
         conn= sqlite3.connect('csv_db.sqlite')
         cur= conn.cursor()
         query_result=cur.execute(query,parameters)
         conn.commit()
         return query_result
root = Tk()
b = Buttons(root)
b.quitButton = Button(root, text="Quit", command=root.quit)
b.quitButton.pack(side=BOTTOM)
root.mainloop()
