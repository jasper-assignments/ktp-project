from flask import Flask, send_file, session, request, abort
from flask_session import Session
from kbparser import parse_kb
from domain import Domain
from logic import Fact, Question,Rule
from backward import backward

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

rules, questions = parse_kb()
goal = Fact("can_dive", "no")

def step(rules: list[Rule], domain: Domain, questions: dict[str, Question], goal: Fact):
    engine = backward(rules, domain, questions, goal)
    try:
        question: Question = next(engine)
        return {"question": question}
    except StopIteration as result:
        return {
            "result": result.value,
            "description": result.value
                and "The diver cannot go into the water safely."
                or "The diver can go into the water safely.",
        }

@app.get("/")
def index():
    return send_file("index.html")

@app.post("/start")
def start():
    domain = Domain()
    session["domain"] = domain
    return step(rules, domain, questions, goal)

@app.post("/answer")
def answer():
    domain = session["domain"]
    setattr(domain, request.json["question"], request.json["answer"])
    session["domain"] = domain
    return step(rules, domain, questions, goal)
