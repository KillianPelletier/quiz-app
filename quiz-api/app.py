from flask import Flask, request
from Utils.jwt_utils import *
from flask_cors import CORS
import hashlib

from Models.Question import Question as QuestionQuiz
from Models.Participation import Participation as ParticipationQuiz
from Models.PossibleAnswer import PossibleAnswer as PossibleAnswerQuiz

from Database.MyDatabase import *
from datetime import date
import os

# region Variable

PWD_MD5 = b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@'  # "flask2023"
DB_PATH = os.path.join(os.getcwd(), "quiz.db")
DEFAULT_NB_SIPS = 1  # Default value when nbSips not defined

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
    """Return quiz information"""
    nbQuestions = db.getNbQuestions()
    participationResults = db.getParticipationResults()
    return {"size": nbQuestions, "scores": [p.toJSON() for p in participationResults]}, 200


@app.route('/questions', methods=['GET'])
def getQuestionByPosition():
    """Return question data by quiz position"""
    position = int(request.args.get('position'))
    question = db.getQuestionByPosition(position)
    if question is None:
        return {"error": f"Question with position = {position} not found"}, 404
    return question.toJSON(), 200


@app.route('/questions/<questionId>', methods=['GET'])
def getQuestionByID(questionId):
    """Return question data by Id"""
    questionId = int(questionId)
    question = db.getQuestionByID(questionId)
    if question is None:
        return {"error": f"Question with id = {questionId} not found"}, 404
    return question.toJSON(), 200


@app.route('/login', methods=['POST'])
def login():
    """Login route"""
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
    """Submit player participation and return correct answers and score"""
    payload = request.get_json()
    participation = ParticipationQuiz(playerName=payload['playerName'], score=0,
                                      date=date.today().strftime("%d/%m/%Y"))

    for pa in payload['answers']:
        participation.answersSummaries.append(pa)

    nbQuestion = db.getNbQuestion()
    nbAnswers = len(participation.answersSummaries)

    if nbQuestion > nbAnswers:
        return 'Not enought answers', 400
    if nbQuestion < nbAnswers:
        return 'Too many questions', 400

    participation = db.addParticipation(participation)
    return participation.toJSON(), 200


# endregion

# region Private routes


@app.route('/rebuild-db', methods=['POST'])
def rebuildDb():
    """Delete then create database"""
    message, code = check_user_auth(request.authorization)
    if code != 200:
        return message, code
    db.rebuild_db()
    return "Ok", 200


@app.route('/questions', methods=['POST'])
def addQuestion():
    """Add question in quiz"""
    message, code = check_user_auth(request.authorization)
    if code != 200:
        return message, code

    payload = request.get_json()
    question = QuestionQuiz(id=None, title=payload['title'], image=payload['image'],
                            position=payload['position'], text=payload['text'])
    for pa in payload['possibleAnswers']:
        question.possibleAnswers.append(PossibleAnswerQuiz(
            id=None, text=pa['text'], isCorrect=pa['isCorrect'], nbSips=pa.get('nbSips', DEFAULT_NB_SIPS)))
    if (not question.isValid(db)):
        return {"error": "Question isn't valid : it must contain one correct answer and its position should be between 1 and number of questions."}, 400
    db.addQuestion(question)
    return {"id": question.id}, 200


@app.route('/questions/<questionId>', methods=['PUT'])
def updateQuestion(questionId):
    """Update quiz question"""
    questionId = int(questionId)
    message, code = check_user_auth(request.authorization)
    if code != 200:
        return message, code

    payload = request.get_json()
    question = QuestionQuiz(id=questionId, title=payload['title'], image=payload['image'],
                            position=payload['position'], text=payload['text'])
    for pa in payload['possibleAnswers']:
        question.possibleAnswers.append(PossibleAnswerQuiz(
            id=None, text=pa['text'], isCorrect=pa['isCorrect'], nbSips=pa.get('nbSips', DEFAULT_NB_SIPS)))
    if (not question.isValid(db)):
        return {"error": "Question isn't valid : it must contain one correct answer and its position should be between 1 and number of questions."}, 400
    success = db.updateQuestion(question)
    if success:
        return {}, 204
    else:
        return {"error": f"Question with id = {questionId} not found"}, 404


@app.route('/questions/<questionId>', methods=['DELETE'])
def deleteQuestion(questionId):
    """Delete question from quiz"""
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
    """Delete all quiz question"""
    message, code = check_user_auth(request.authorization)
    if code != 200:
        return message, code

    db.deleteAllQuestions()
    return {}, 204


@app.route('/participations/all', methods=['DELETE'])
def deleteAllParticipations():
    """Delete all player participations"""
    message, code = check_user_auth(request.authorization)
    if code != 200:
        return message, code

    db.deleteAllParticipations()
    return {}, 204

# endregion


# Keep at the end
if __name__ == "__main__":
    app.run()
