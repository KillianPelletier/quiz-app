import sqlite3
from ParticipationResult import *
from Question import *
from PossibleAnswer import *


class MyDatabase():

    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(
            db_path, check_same_thread=False, isolation_level=None)

    def close(self):
        self.connection.close()

    def exec(self, request):
        self.cur.execute("begin")
        self.cur.execute(request)
        self.cur.execute("commit")

        # IF ERROR THEN cur.execute('rollback')
    def getNbQuestions(self):
        cur = self.connection.cursor()
        cur.execute(
            "Select Count(id) from questions")
        return cur.fetchone()[0]

    def getParticipationResults(self):
        cur = self.connection.cursor()
        cur.execute(
            "Select playerName, score, date from participation_results Order By score Desc")
        rows = cur.fetchall()
        res = []
        for r in rows:
            res.append(ParticipationResult(
                playerName=r[0], score=r[1], date=r[2]))
        return res

    def getQuestionByID(self, questionID):
        cur = self.connection.cursor()
        cur.execute(
            f"Select id, title, image, position, text from questions Where id = {questionID}")
        result = cur.fetchone()
        if result is None:
            return None
        q = Question(id=result[0], title=result[1],
                     image=result[2], position=result[3], text=result[4])

        cur.execute(
            f"Select id, text, isCorrect, nbSips from possible_answers Answers Where questionID = {questionID}")
        rows = cur.fetchall()
        for pa in rows:
            q.possibleAnswers.append(PossibleAnswer(
                id=pa[0], text=pa[1], isCorrect=pa[2], nbSips=pa[3]))

        return q

    def getQuestionByPosition(self, position):
        cur = self.connection.cursor()
        cur.execute(
            f"Select id, title, image, position, text from questions Where position = {position}")
        result = cur.fetchone()
        if result is None:
            return None
        q = Question(id=result[0], title=result[1],
                     image=result[2], position=result[3], text=result[4])

        cur.execute(
            f"Select id, text, isCorrect, nbSips from possible_answers Answers Where questionID = {q.id}")
        rows = cur.fetchall()
        for pa in rows:
            q.possibleAnswers.append(PossibleAnswer(
                id=pa[0], text=pa[1], isCorrect=pa[2], nbSips=pa[3]))

        return q

    def addQuestion(self, q: Question):
        cur = self.connection.cursor()
        cur.execute("Begin")
        # Add 1 to position to all questions to which their position is equal or greater than q.position
        self.updateQuestionPosition(1, q.position)
        cur.execute(
            "Insert into questions (title, image, position, text) values (?, ?, ?, ?)",
            (q.title, q.image, q.position, q.text))
        q.id = cur.lastrowid
        cur.executemany(
            "Insert into possible_answers (text, isCorrect, nbSips, questionId) values (?, ?, ?, ?)", [(pa.text, pa.isCorrect, pa.nbSips, q.id) for pa in q.possibleAnswers])
        cur.execute('Commit')

    def updateQuestion(self, q: Question):
        cur = self.connection.cursor()
        cur.execute(f"Select position from questions where id = {q.id}")
        res = cur.fetchone()
        if res is None:
            return False
        currentPos = res[0]

        cur.execute("Begin")
        newPos = q.position
        if currentPos >= newPos:
            self.updateQuestionPosition(1, newPos, currentPos)
        else:
            self.updateQuestionPosition(-1, currentPos, newPos)

        cur.execute(
            "Update questions Set title=?, image=?, position=?, text=? Where id=?",
            (q.title, q.image, q.position, q.text, q.id))
        # Delete possible_answers of the question as we don't have their ids to directly update them
        cur.execute(f"Delete from possible_answers Where questionId={q.id}")
        # Add new possible_answers
        cur.executemany(
            "Insert into possible_answers (text, isCorrect, nbSips, questionId) values (?, ?, ?, ?)", [(pa.text, pa.isCorrect, pa.nbSips, q.id) for pa in q.possibleAnswers])

        cur.execute('Commit')
        return True

    def deleteQuestion(self, questionId: int):
        cur = self.connection.cursor()
        cur.execute(f"Select position from questions where id = {questionId}")
        res = cur.fetchone()
        if res is None:
            return False

        position = res[0]

        cur.execute("Begin")
        cur.execute(
            f"Delete from possible_answers Where questionId = {questionId}")
        cur.execute(
            f"Delete from questions Where id = {questionId}")
        # Decrement 1 to position to all questions to which their position is equal or greater than q.position
        self.updateQuestionPosition(-1, position)
        cur.execute('Commit')
        return True

    def deleteAllQuestions(self):
        cur = self.connection.cursor()
        cur.execute("Begin")
        cur.execute("Delete From possible_answers")
        cur.execute("Delete From questions")
        cur.execute('Commit')

    def deleteAllParticipations(self):
        cur = self.connection.cursor()
        cur.execute("Begin")
        cur.execute("Delete From participation_results")
        cur.execute('Commit')

    # increment : 1 or -1
    def updateQuestionPosition(self, increment: int, startAtPos: int, endAtPos: int = -1):
        cur = self.connection.cursor()
        sqlRequest = f"Update questions set position = position + {increment} Where position >= {startAtPos}"
        if endAtPos != -1:
            sqlRequest += f" and position <= {endAtPos}"
        cur.execute(sqlRequest)
