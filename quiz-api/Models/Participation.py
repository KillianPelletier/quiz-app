
class Participation():
    def __init__(self, playerName: str, score: float, date: str):
        self.playerName = playerName
        self.score = score
        self.date = date
        self.playerAnswers = []
        self.answersSummaries = []

    def toJSON(self):
        return {"playerName": self.playerName, "score": self.score, "date": self.date, "answersSummaries": [self.summaryToJSON(s) for s in self.answersSummaries]}

    def summaryToJSON(self,answer):
        #test = list(answer)
        return{"correctAnswerPosition":answer[0], "wasCorrect":answer[1]}