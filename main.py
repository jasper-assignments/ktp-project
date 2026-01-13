from flask import Flask, send_file, session, request
from kbparser import parse_kb
from logic import Fact, Question,Rule
from backward import backward
import json

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
    # Initialise empty domain object
    domain = {}

    # Execute a step
    result = step(rules, domain, questions, goal)

    # Store current domain in session as domain and previous domain
    session["domain"] = json.dumps(domain)
    session["prevDomain"] = json.dumps(domain)

    return result

@app.post("/answer")
def answer():
    # Save current domain for undo
    session["prevDomain"] = session["domain"]

    # Load current domain
    domain = json.loads(session["domain"])
    # Set answer from request
    domain[request.json["question"]] = request.json["answer"]
    # Execute a step
    result = step(rules, domain, questions, goal)

    # Store current domain in session
    session["domain"] = json.dumps(domain)

    return result

@app.post("/undo")
def undo():
    # Restore previous domain
    session["domain"] = session["prevDomain"]

    # Load current domain
    domain = json.loads(session["domain"])
    # Execute a step
    result = step(rules, domain, questions, goal)

    # Store current domain in session
    session["domain"] = json.dumps(domain)

    return result

if __name__ == "__main__":
    app.run()
