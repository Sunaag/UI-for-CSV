#run the code and select a csv file and
# select a field or more fields on UI
# output appears on command line
#UPDATED THE CODE WITH CHECKBOXES FOR SELECTION OF MULTIPLE FIELDS AT A TIME
#AND PRINTING THEM IN THE TEXTBOXES ON THE GUI ITSELF
from tkinter import *
import sqlite3

class Buttons:
     def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        frame.grid(column=0,row=0, sticky=(N,W,E,S) )
        frame.pack(pady =10, padx = 10)
        self.text_box=Text(frame,state=DISABLED)
        self.text_box.grid(row=5,column=20,columnspan=1)
        self.tkvar= StringVar(master)
        out=self.run_query('''SELECT filename FROM Csv''')
        choices={}
        for row in out:
            choices[row[0]] = choices.get(row[0],0)+1
            #print(choices)
        self.csv_files=[]
        for k,v in choices.items():
            self.csv_files.append(k)
        #print(csv_files)
        popupMenu = OptionMenu(frame, self.tkvar, *choices)
        self.label1 = Label(frame,text='CSV :')
        self.label1.grid(row=0,sticky=N)
        popupMenu.grid(row=0,column=1,sticky=N,columnspan=5)
        self.tkvar1=StringVar(master)
        choices1={}
        out1=self.run_query('''PRAGMA table_info(Data)''' )

        for row in out1:
            if row[1].endswith('id'):
                continue
            choices1[row[1]]=choices1.get(row[1],0)+1
        self.datas=[]
        self.datas1=[]
        for k,v in choices1.items():
            self.datas1.append(k)
            self.datas.append('self.{}'.format(k))
        #print(self.datas1)
        #print(self.datas)

        popupMenu1 = OptionMenu(frame, self.tkvar1,'OPTIONS:')
        self.label2 = Label(frame,text='Fields:')
        self.label2.grid(row=1,sticky=W)
        popupMenu1.grid(row=1,column=1,sticky=W)
        #choices_dict=
        self.l=[]
    # link function to change dropdown
        for i,data in enumerate(self.datas):
            self.datas[i]=BooleanVar()
            popupMenu1['menu'].add_checkbutton(label=self.datas1[i],onvalue=True,command=self.add,offvalue=False,variable=self.datas[i])

    # function to appened all the selected checkboxes and get the output accordingly
     def add(self):
         count=''
         for i,data in enumerate(self.datas):
             if data.get==True:
                 count=','.join(self.datas1[i])
         return count
     def write(self,string):
         self.text_box.config(state=NORMAL)
         self.text_box.insert("end", string + "\n")
         self.text_box.see("end")
         self.text_box.config(state=DISABLED)

     def run_query(self,query,parameters=()):
         conn= sqlite3.connect('csv_db.sqlite')
         cur= conn.cursor()
         query_result=cur.execute(query,parameters)
         conn.commit()
         return query_result
     def on_button(self):
         self.write("SELECTED CSV FILE:\n{}".format(self.tkvar.get()))
         self.write('\n')
         for csv in self.csv_files:
             for i,data in enumerate(self.datas):
                 #self.write('Selected Fields:{}'.format(self.add()))
                 csv_id=self.csv_files.index(csv)
                 if self.tkvar.get()==csv and data.get()==True:

                     self.write('SELECTED FIELDS:{}'.format(self.datas1[i]))
                     out1=self.run_query('''SELECT [{}] FROM Data WHERE csv_id =? '''.format(self.datas1[i]),(csv_id+1,) )
                     for row in out1:
                         self.write('   {}'.format(row[0]))
         self.write('\n')

root = Tk()
b = Buttons(root)
root.title('Field Finder')
b.onbutt=Button(root,text='Ok',command=b.on_button)
b.onbutt.pack(side=BOTTOM)
b.quitButton = Button(root, text="Quit", command=root.quit)
b.quitButton.pack(side=BOTTOM)
root.mainloop()
