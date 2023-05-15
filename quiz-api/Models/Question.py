
class Question():

    def __init__(self, id: int, title: str, image: str, position: int, text: str):
        self.id = id
        self.title = title
        self.image = image
        self.position = position
        self.text = text
        self.possibleAnswers = []

    def toJSON(self):
        return {"id": self.id, "title": self.title, "image": self.image, "position": self.position, "text": self.text, "possibleAnswers": [p.toJSON() for p in self.possibleAnswers]}
