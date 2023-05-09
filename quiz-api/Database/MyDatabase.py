import sqlite3
from Models import *


class MyDatabase():

    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)

        # set the sqlite connection in "manual transaction mode"
        # (by default, all execute calls are performed in their own transactions, not what we want)
        self.connection.isolation_level = None
        self.cur = self.connection.cursor()

    def close(self):
        self.connection.close()

    def exec(self, request):
        self.cur.execute("begin")
        self.cur.execute(request)
        self.cur.execute("commit")

        # IF ERROR THEN cur.execute('rollback')

    def addScore(self, username: str, value: float):
        exec(
            f"Insert into scores (username, value) values ( {username}, {value})"
        )

    def getScores(self, count: int):
        cur = self.connection.cursor()
        cur.execute("Select * from scores Order By value Desc")
        rows = cur.fetchall()
        return rows
