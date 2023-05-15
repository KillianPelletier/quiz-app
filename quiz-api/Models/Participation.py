
class Participation():
    def __init__(self, playerName: str, score: float, date: str):
        self.playerName = playerName
        self.score = score
        self.date = date
        self.answersSummaries = []

    def toJSON(self):
        return {"playerName": self.playerName, "score": self.score, "date": self.date, "answersSummaries": self.answersSummaries}
