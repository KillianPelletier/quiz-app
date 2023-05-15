from flask import Flask, request
from Utils.jwt_utils import *
from flask_cors import CORS
import hashlib
from Participation import *
from Question import *
from PossibleAnswer import *
from MyDatabase import *
import os
from datetime import date

# region Variable
# "flask2023"
PWD_MD5 = b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@'
DB_PATH = os. getcwd() + "\\Database\\quiz.db"
# endregion

app = Flask(__name__)
CORS(app)

db = MyDatabase(DB_PATH)


# region Public routes


@app.route('/')
def index():
    return "Flask API"


@app.route('/quiz-info', methods=['GET'])
def getQuizInfo():
    participationResults = db.getParticipationResults()
    return {"size": len(participationResults), "scores": [p.toJSON() for p in participationResults]}, 200


@app.route('/questions', methods=['GET'])
def getQuestionByPosition():
    position = int(request.args.get('position'))
    question = db.getQuestionByPosition(position)
    if question is None:
        return {"error": f"Question with position = {position} not found"}, 404
    else:
        return question.toJSON(), 200


@app.route('/questions/<questionId>', methods=['GET'])
def getQuestionByID(questionId):
    questionId = int(questionId)
    question = db.getQuestionByID(questionId)
    if question is None:
        return {"error": f"Question with id = {questionId} not found"}, 404
    else:
        return question.toJSON(), 200


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

@app.route('/participations', methods=['POST'])
def participations():
    # message, code = check_user_auth(request.authorization)
    # if code != 200:
    #     return message, code

    payload = request.get_json()
    participation = Participation(playerName=payload['playerName'], score=0,
                         date=date.today().strftime("%d/%m/%Y"))
    
    for pa in payload['answers']:
        participation.answersSummaries.append(pa)

    nbQuestion = db.getNbQuestion()
    nbAnswers = len(participation.answersSummaries)
    if(nbQuestion ==nbAnswers ):
        participation =db.addParticipation(participation) 
        return participation.toJSON(), 200
    elif(nbQuestion > nbAnswers):
        return 'Not enought answers', 400
    else:
        return 'Too many questions', 400    
    
    
        

# endregion

# region Private routes


@app.route('/questions', methods=['POST'])
def addQuestion():
    message, code = check_user_auth(request.authorization)
    if code != 200:
        return message, code

    payload = request.get_json()
    question = Question(id=None, title=payload['title'], image=payload['image'],
                        position=payload['position'], text=payload['text'])
    for pa in payload['possibleAnswers']:
        question.possibleAnswers.append(PossibleAnswer(
            id=None, text=pa['text'], isCorrect=pa['isCorrect'], nbSips=pa.get('nbSips', 1)))
    db.addQuestion(question)
    return {"id": question.id}, 200


@app.route('/questions/<questionId>', methods=['DELETE'])
def deleteQuestion(questionId):
    questionId = int(questionId)
    message, code = check_user_auth(request.authorization)
    if code != 200:
        return message, code

    success = db.deleteQuestion(questionId)
    if success:
        return {}, 204
    else:
        return {"error": f"Question with id = {questionId} not found"}, 404


@app.route('/questions/all', methods=['DELETE'])
def deleteAllQuestions():
    message, code = check_user_auth(request.authorization)
    if code != 200:
        return message, code

    db.deleteAllQuestions()
    return {}, 204


@app.route('/participations/all', methods=['DELETE'])
def deleteAllParticipations():
    message, code = check_user_auth(request.authorization)
    if code != 200:
        return message, code

    db.deleteAllParticipations()
    return {}, 204


# endregion


# Keep at the end
if __name__ == "__main__":
    app.run()
