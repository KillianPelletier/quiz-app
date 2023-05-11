
class ParticipationResult():
    def __init__(self, playerName: str, score: float, date: str):
        self.playerName = playerName
        self.score = score
        self.date = date

    def toJSON(self):
        return {"playerName": self.playerName, "score": self.score, "date": self.date}
