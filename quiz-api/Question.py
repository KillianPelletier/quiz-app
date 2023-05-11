
class Question():

    def __init__(self, title: str, urlImage: str, position: int, text: str):
        self.title = title
        self.urlImage = urlImage
        self.position = position
        self.text = text
        self.answers = []
