from flask import Flask, send_file, session, request, abort
from flask_session import Session
from kbparser import parse_kb
from domain import Domain
from logic import Fact
from backward import backward

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

rules, questions = parse_kb()
# print(f"Original parsed goal: {goal}")

def test_backward() -> None:
    domain = Domain()
    goal = Fact(name="can_dive", value="no")
    result = backward(rules, domain, questions, goal)
    print(f"goal: {goal.name}={goal.value}, result: {result}")

test_backward()

@app.get("/")
def index():
    return send_file("index.html")

@app.get("/questions")
def questions():
    if ("questions" not in session):
        session["questions"] = {
            "example": {"question": "Is this an example question?", "answer": None}
        }
    return session.get("questions")

@app.post("/questions/<question_id>")
def answer(question_id):
    if ("questions" not in session):
        # Hasn't triggered start before answering
        abort(400)
    if (question_id not in session.get("questions")):
        # Bad question id
        abort(400)
    session["questions"][question_id]["answer"] = True
    return session.get("questions")
