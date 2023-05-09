import sqlite3


class MyDatabase():

    def __init__(db_path: str):
        self.connection = sqlite3.connect(db_path)

        # set the sqlite connection in "manual transaction mode"
        # (by default, all execute calls are performed in their own transactions, not what we want)
        self.connection.isolation_level = None
        self.cur = self.connection.cursor()

    def close(self):
        self.connection.close()

    def exec(request):
        cur.execute("begin")
        cur.execute(request)
        cur.execute("commit")

        # IF ERROR THEN cur.execute('rollback')
