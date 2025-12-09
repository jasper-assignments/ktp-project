from flask import Flask, send_file, session, request, abort
from flask_session import Session
from kbparser import parse_kb
from logic import Fact, Question,Rule
from backward import backward

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

rules, questions = parse_kb()
goal = Fact("can_dive", "no")

def step(rules: list[Rule], domain: dict, questions: dict[str, Question], goal: Fact):
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

def ask_user(question: Question) -> str:
  options = [f"{i}: {a.label}" for i, a in enumerate(question.answers)]
  return question.answers[int(input(f"{question.description} ({", ".join(options)}) > "))].value

def test_backward() -> None:
    domain = {}
    goal = Fact(name="can_dive", value="no")
    result = None
    while True:
        result = step(rules, domain, questions, goal)
        if ("result" in result):
            break
        if ("question" in result):
            question = result["question"]
            answer = ask_user(question)
            domain[question.name] = answer
    print(f"goal: {goal.name}={goal.value}, result: {result["result"]}")
    print(result)

if __name__ == "__main__":
    test_backward()

@app.get("/")
def index():
    return send_file("index.html")

@app.post("/start")
def start():
    domain = {}
    session["domain"] = domain
    return step(rules, domain, questions, goal)

@app.post("/answer")
def answer():
    domain = session["domain"]
    domain[request.json["question"]] = request.json["answer"]
    session["domain"] = domain
    return step(rules, domain, questions, goal)

@app.post("/undo")
def undo():
    domain = session["domain"]
    domain[request.json["question"]] = None
    domain[goal.name] = None
    session["domain"] = domain
    return step(rules, domain, questions, goal)
