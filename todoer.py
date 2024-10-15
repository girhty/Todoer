#!/usr/bin/python3
import sys
import os
import time
from datetime import datetime

commands=["add","remove","todos","toggle"]

def parse(data):
    if len(data)==0:
        return []
    tds=[]
    for i in data: 
        i=i.replace("\n","")
        if len(i)==0:
            continue
        vals=i.split(",")
        td={"todo":vals[0],"status":int(vals[1]),"timestamp":int(vals[2])}
        tds.append(td)
    return tds

def write_todos(items):
    with open("td.db","w") as file:
        for item in items:
            file.writelines(f"{item['todo']},{item['status']},{item['timestamp']}\n")
    
def parse_item(item):
    return {"todo":item,"status":0,"timestamp":time.time_ns()}

def print_todo(todo,index):
    td=todo["todo"]
    space=len(td)+45
    if bool(todo["status"]):
        stat="✅"
    else:
        stat="❌"
    ts=datetime.fromtimestamp(todo["timestamp"]/1e9)
    print("╔"+"═"*space+"╗")
    print("║",index,"-",td," ┃ ",stat," ┃",ts,"  ║")
    print("╚"+"═"*space+"╝")

class toDo():
    def __init__(self,items):
        self.todos=parse(items)
    def add(self,item):
        self.todos.append(item)
        write_todos(self.todos)
    def remove(self,index):
        del self.todos[index]
        write_todos(self.todos)
    def list(self):
        return self.todos
    def toggle(self,index):
        if self.todos[index]["status"]==1:
            self.todos[index]["status"]=0
        else:
            self.todos[index]["status"]=1
        write_todos(self.todos)    

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
    if command=="todos":
        tds=TD.list()
        for index,item in enumerate(tds):
            print_todo(item,index)
    if command=="toggle":
        index=int(args[1])
        if index>len(TD.todos)-1:
            print("index not found")
            exit(1)
        TD.toggle(index)
        print_todo(TD.todos[index],index)
    exit(0)

print("command not found")
exit(1)