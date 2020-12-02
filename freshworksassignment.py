from tkinter import *
import os
import sqlite3
from datetime import datetime

class keyvalue:
    def __init__(self):
        name="keyvaluepair"

        def connect():
            self.conn=sqlite3.connect(name)
            self.cur=self.conn.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS keyvaluepair(key text,value text,timen text,timetolive text)")
            self.conn.commit()
            self.conn.close()

        def create():
            connect()
            self.key=e2.get()
            self.value=e3.get()
            self.ttl=e4.get()
            if self.ttl=="":
                self.ttl='NA'
            
            self.conn=sqlite3.connect(name)
            self.cur=self.conn.cursor()
            self.cur.execute("SELECT value FROM keyvaluepair WHERE key=?",(self.key,))
            self.val=self.cur.fetchall()
            self.conn.close()
            if self.key=="" or len(self.key)>32:
                e5.delete(0,'end')
                e5.insert(0,"Error: invalid key")
            elif self.value=="":
                e5.delete(0,'end')
                e5.insert(0,"Error: invalid value")
            elif len(self.val)!=0:
                e5.delete(0,'end')
                e5.insert(0,"Error: this key is already defined")
            else:
                self.conn=sqlite3.connect(name)
                self.cur=self.conn.cursor()
                self.cur.execute("INSERT INTO keyvaluepair VALUES(?,?,?,?)",(self.key,self.value,datetime.now(),self.ttl,))
                self.conn.commit()
                self.conn.close()
                e5.delete(0,'end')
                e5.insert(0,"new entry successfull created")

        def read():
            connect()
            self.key1=e2.get()
            self.conn=sqlite3.connect(name)
            self.cur=self.conn.cursor()
            self.cur.execute("SELECT value FROM keyvaluepair WHERE key=?",(self.key1,))
            self.val=self.cur.fetchall()
            self.conn.close()
            if len(self.val)==0:
                e5.delete(0,'end')
                e5.insert(0,"Error: no such key exists")
                return None
            if check():
                self.temp=self.val
                self.val=self.key1+':'+self.val[0][0]
                e3.delete(0,'end')
                e3.insert(0,self.temp)
                e5.delete(0,'end')
                e5.insert(0,"the key value pair of "+self.key1+" is "+self.val)
            else:
                e5.delete(0,'end')
                e5.insert(0,"This operation is no longer valid")

        def delete():
            self.key1=e2.get()
            self.conn=sqlite3.connect(name)
            self.cur=self.conn.cursor()
            self.cur.execute("SELECT value FROM keyvaluepair WHERE key=?",(self.key1,))
            self.val=self.cur.fetchall()
            self.conn.commit()
            self.conn.close()
            if len(self.val)==0:
                e5.delete(0,'end')
                e5.insert(0,"Error: no such key exists")
                return  None
            if check():
                self.conn=sqlite3.connect(name)
                self.cur=self.conn.cursor()
                self.cur.execute("DELETE FROM keyvaluepair WHERE key=?",(self.key1,))
                self.conn.commit()
                self.conn.close()
                e5.delete(0,'end')
                e5.insert(0,"key value pair is successfully deleted")
            else:
                e5.delete(0,'end')
                e5.insert(0,"This operation is no longer valid")

        def check():
            self.key=e2.get()
            self.conn=sqlite3.connect(name)
            self.cur=self.conn.cursor()
            self.cur.execute("SELECT timetolive FROM keyvaluepair WHERE key=?",(self.key,))
            self.ttl=self.cur.fetchall()
            self.conn.close()
            if self.ttl[0][0]=='NA':
                return True
            else:
                self.conn=sqlite3.connect(name)
                self.cur=self.conn.cursor()
                self.cur.execute("SELECT timen FROM keyvaluepair WHERE key=?",(self.key,))
                self.tn=self.cur.fetchall()
                self.conn.close()
                self.temp=self.tn[0][0]
                self.temp1=datetime(int(self.temp[0:4]),int(self.temp[5:7]),int(self.temp[8:10]),int(self.temp[11:13]),int(self.temp[14:16]),int(self.temp[17:19]),int(self.temp[20:-1]))
                if (datetime.now()-self.temp1).total_seconds()<int(self.ttl[0][0]):
                    return True
                else:
                    return False
            
        def changepath():
            self.text=e1.get()
            if self.text!="":
                os.chdir(self.text)
            return None

        window=Tk()

        l1=Label(window,text="file path(optional)",width=20)
        l1.grid(row=0,column=0)

        e1=Entry(window,width=20)
        e1.grid(row=0,column=1)

        b1=Button(window,text="save path",width=20,command=changepath)
        b1.grid(row=1,column=0)

        b2=Button(window,text="next",width=20,command=window.destroy)
        b2.grid(row=1,column=1)

        window.mainloop()

        window1=Tk()
        
        l2=Label(window1,text="Key",width=20)
        l2.grid(row=0,column=0)

        e2=Entry(window1,width=40)
        e2.grid(row=0,column=1,columnspan=2)

        l3=Label(window1,text="Value",width=20)
        l3.grid(row=1,column=0)

        e3=Entry(window1,width=40)
        e3.grid(row=1,column=1,columnspan=2)

        l4=Label(window1,text="Time to live(in seconds)",width=20)
        l4.grid(row=2,column=0)

        e4=Entry(window1,width=40)
        e4.grid(row=2,column=1,columnspan=2)

        b3=Button(window1,text="create",width=20,command=create)
        b3.grid(row=3,column=0)

        b4=Button(window1,text="read",width=20,command=read)
        b4.grid(row=3,column=1)

        b5=Button(window1,text="delete",width=20,command=delete)
        b5.grid(row=3,column=2)

        e5=Entry(window1,width=70)
        e5.grid(row=4,column=0,columnspan=3)

        window1.mainloop()

ganesh=keyvalue()
