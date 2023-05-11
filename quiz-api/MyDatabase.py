import sqlite3
from ParticipationResult import *
from Question import *
from Answer import *


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

    def getParticipationResults(self):
        cur = self.connection.cursor()
        cur.execute(
            "Select playerName, score, date from scores Order By score Desc")
        rows = cur.fetchall()
        res = []
        for r in rows:
            res.append(ParticipationResult(
                playerName=r[0], score=r[1], date=r[2]))
        return res
    
    def getQuestionByID(self, questionID):
        cur = self.connection.cursor()
        cur.execute(
            "Select id, title, image, position, text from questions Where id = {questionID}")
        result = cur.fetchall
        q = Question(id = result[0], title= result[1],image=result[2],position=result[3],text=result[4])

        cur.execute(
            "Select id, text, isCorrect, nbSips from scores Answers Where questionID = {questionID}")
        rows = cur.fetchall()
        res = []
        for r in rows:
            q.possibleAnswers.append(Answer(id = result[0], text= result[1],isCorrect=result[2],nbSips=result[3]))

        return q
