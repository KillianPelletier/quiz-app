
class PossibleAnswer():
    def __init__(self,id:int, text: str, isCorrect: bool, nbSips: int):
        self.id = id
        self.text = text
        self.isCorrect = isCorrect
        self.nbSips = nbSips

    def toJSON(self):
        return {"id": self.id, "text": self.text, "isCorrect": self.isCorrect,"nbSips": self.nbSips}