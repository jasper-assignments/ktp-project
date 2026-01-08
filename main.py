from flask import Flask, send_file, session, request
from kbparser import parse_kb
from logic import Fact, Question,Rule
from backward import backward

app = Flask(__name__)
app.config["SECRET_KEY"] = "bottomoftheocean"

rules, questions = parse_kb()
goal = Fact("canDive", "no")

def step(rules: list[Rule], domain: dict, questions: dict[str, Question], goal: Fact):
    engine = backward(rules, domain, questions, goal)
    try:
        question: Question = next(engine)
        return {"question": question}
    except StopIteration as result:
        return {
            "result": result.value,
            "description": result.value
                and "The diver cannot go into the water safely. Reason: " + domain.get("reason")
                or "The diver can go into the water safely.",
        }

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

if __name__ == "__main__":
    app.run()
