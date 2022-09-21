import telebot
from config import TELEGRAM_TOKEN
import sqlite3

bot=telebot.TeleBot(TELEGRAM_TOKEN)

#CLASS TO HANDLE DATABASE
class RecurrentMessage:
    def __init__(self):
        self.con=sqlite3.connect("./MessagesDatabase.db")
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
            type TEXT,
            next_message TEXT,
            destruction_ids TEXT,
            next_destruction TEXT)""")

    def ups(self):
        self.cur.execute("""UPDATE messages SET next_message=null WHERE messages.type='daily'""")
        self.con.commit()

    def insert(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO messages VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", item)
        self.con.commit()

    def read(self):
        self.cur.execute("SELECT * FROM messages")
        rows=self.cur.fetchall()
        return rows

    def edit(self, column, row_id, new_cell):
        try:
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
            return True

        except Exception as e:
            print(e)
            return False

