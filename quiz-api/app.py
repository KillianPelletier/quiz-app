from flask import Flask, request
from Utils.jwt_utils import *
from flask_cors import CORS
import hashlib
from Models import Question, Answer, Score
from Database import MyDatabase

app = Flask(__name__)
CORS(app)

# region Variable
# "flask2023"
PWD_MD5 = b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@'
DB_PATH = "quiz.db"
# endregion

# region Routes

@app.route('/')
def index():
    return "Flask API"


@app.route('/quiz-info', methods=['GET'])
#
def getQuizInfo():
    return {"size": 10, "scores": [{'playerName': 'JeanJean', 'score': 10, 'date': '09/05/2023 18:30:00'}, {'playerName': 'Marc', 'score': 5, 'date': '08/05/2023  20:35:00'}]}, 200


@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    pwd = payload['password'].encode('UTF-8')
    pwd_hashed = hashlib.md5(pwd).digest()
    if pwd_hashed == PWD_MD5:
        token = build_token()
        return {"token": token}, 200
    else:
        return 'Unauthorized', 401

# endregion


# Keep at the end
if __name__ == "__main__":
    self.db = MyDatabase(DB_PATH)
    app.logger.info("Test")
    app.run()
