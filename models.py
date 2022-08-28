import logging
from exceptions import *
import os
import json
import telebot
from config import TELEGRAM_TOKEN
import sqlite3

bot=telebot.TeleBot(TELEGRAM_TOKEN)


class RecurrentMessage:
    def __init__(self):
        self.con=sqlite3.connect("MessagesDatabase.db")
        self.cur=self.con.cursor()
        self.create_table()
    
    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            message TEXT,
            delay TEXT,
            only_in TEXT,
            time TEXT,
            days TEXT,
            notification TEXT,
            destruction TEXT,
            type TEXT)""")

    def insert(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO messages VALUES(?,?,?,?,?,?,?,?,?,?)""", item)
        self.con.commit()

    def read(self):
        self.cur.execute("SELECT * FROM messages")
        rows=self.cur.fetchall()
        return rows

    def edit(self, column, row_id, new_cell):
        try:
            print(column, row_id, new_cell)
            self.cur.execute(f"UPDATE messages SET '{column}'='{new_cell}' WHERE id like {row_id}")
            self.con.commit()
            return True

        except Exception as e:
            print(e)
            return False

    def delete(self, row_id):
        try:

            result=self.cur.execute(f"DELETE FROM messages WHERE id={row_id}")
            self.con.commit()
            print(result)
            return True

        except Exception as e:
            print(e)
            return False




# class MessagesDatabase:
#     def __init__(self, location):
#         self.location=os.path.expanduser(location)
#         self.load(self.location)

#     def load(self, location):
#         if os.path.exists(location):
#             self._load()
#         else:
#             self.db={}
#         return True

#     def _load(self):
#         self.db=json.load(open(self.location, 'r'))

#     def dumpdb(self):
#         try:
#             json.dump(self.db, open(self.location, "w+"))
#             return True
#         except:
#             return False

#     def _set(self , key , value):
#         try:
#             self.db[str(key)] = value
#             self.dumpdb()
#             return True
#         except Exception as e:
#             print("[X] Error Saving Values to Database : " + str(e))
#             return False

#     def get(self , key):
#         try:
#             return self.db[key]
#         except KeyError:
#             print("No Value Can Be Found for " + str(key))  
#             return False

#     def delete(self , key):
#         if not key in self.db:
#             return False
#         del self.db[key]
#         self.dumpdb()
#         return True
    
#     def resetdb(self):
#         self.db={}
#         self.dumpdb()
#         return True


# class RecurrentMessage:
#     def __init__(self, title, message, time, only_in):
#         self._id=len(db)+1
#         self.title=title
#         self.message=message
#         self.time=time
#         self.only_in=only_in