#!/usr/bin/python3
import sys
import os
import time
from datetime import datetime

commands=["add","remove","list","toggle","purge"]
def parse_item(item):
    return {"todo":item,"status":0,"timestamp":time.time_ns()}

class toDo():
    def __init__(self,data):
        self.THEME='36m'
        self.longest_todo=0
        if len(data)==0:
            self.todos=[]
        tds=[]
        for i in data: 
            i=i.replace("\n","")
            if len(i)==0:
                continue
            vals=i.split(",")
            tdlen=len(vals[0])+len(vals[1])+len(vals[2])
            td={"todo":vals[0],"status":int(vals[1]),"timestamp":int(vals[2]),"tdlen":tdlen}
            if tdlen>self.longest_todo:
                self.longest_todo=tdlen
            tds.append(td)
        self.todos=tds
    def write_to_db(self):
        with open("td.db","w") as file:
            for item in self.todos:
                file.writelines(f"{item['todo']},{item['status']},{item['timestamp']}\n")
    def add(self,item):
        self.todos.append(item)
        self.write_to_db()
    def remove(self,index):
        del self.todos[index]
        self.write_to_db()
    def list(self):
        print(f"\033[{self.THEME}╔\033[0m"+f"\033[{self.THEME}═\033[0m"*(self.longest_todo+1)+f"\033[{self.THEME}╗\033[0m")
        for index,t in enumerate(self.todos):
            todo=t["todo"]
            if bool(t["status"]):
                stat="✅"
            else:
                stat="❌"
            ts=datetime.fromtimestamp(t["timestamp"]/1e9)
            offset=self.longest_todo-t["tdlen"]
            print(f"\033[{self.THEME}║\033[0m",f"\033[{self.THEME}{ts.date()}\033[0m",index,".",f"\033[1m{todo}\033[0m",stat," "*(offset),f"\033[{self.THEME}║\033[0m")
            print(f"\033[{self.THEME}║\033[0m",f"\033[{self.THEME}═\033[0m"*(self.longest_todo-1),f"\033[{self.THEME}║\033[0m")
        print(f"\033[{self.THEME}╚\033[0m"+f"\033[{self.THEME}═\033[0m"*(self.longest_todo+1)+f"\033[{self.THEME}╝\033[0m")
    def toggle(self,index):
        if self.todos[index]["status"]==1:
            self.todos[index]["status"]=0
        else:
            self.todos[index]["status"]=1
        self.write_to_db()

path=os.getcwd()
if not os.path.isfile(f"{path}/td.db"):
    open(f"{path}/td.db","w")
if os.stat(f"{path}/td.db").st_size!=0:
    with open("td.db","r") as readfile:
        data=readfile.readlines()
        TD=toDo(data)
else:
    TD=toDo([])

args=sys.argv[1:]

if len(args)==0:
    print("enter a command")
    exit(1)

command=args[0]
if command in commands:
    if command=="add":
        TD.add(parse_item(" ".join(i for i in args[1:])))
    if command=="remove":
        TD.remove(int(args[1]))
    if command=="list":
        TD.list()
    if command=="purge":
        with open("td.db","w") as f:
            f.truncate(0)
    if command=="toggle":
        index=int(args[1])
        if index>len(TD.todos)-1:
            print("index not found")
            exit(1)
        TD.toggle(index)
        TD.list()
    exit(0)

print("command not found")
exit(1)