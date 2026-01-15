from flask import Flask, send_file, session, request
from kbparser import parse_kb
from logic import Fact, Rule, Subclass
from backward import backward
from domain import Domain

app = Flask(__name__)
app.config["SECRET_KEY"] = "bottomoftheocean"

rules, subclasses = parse_kb()
goal = Fact("canDive", "no")

def step(rules: list[Rule], domain: Domain, subclasses: dict[str, Subclass], goal: Fact):
    engine = backward(rules, domain, subclasses, goal)
    try:
        return next(engine)
    except StopIteration as result:
        if not result.value:
            # We have a conclusion now so if we haven't completed our last subclass yet we will do so now.
            currentSubclass = domain.getCurrentSubclass()
            if currentSubclass is not None and domain.completeSubclass(currentSubclass):
                return {"message": {"description": subclasses[currentSubclass].completeMessage}}
        return {
            "result": result.value,
            "description": result.value
                and "The diver cannot go into the water safely. Reason: " + domain.getFact("reason")
                or "The diver can go into the water safely.",
        }

@app.get("/")
def index():
    return send_file("index.html")

@app.post("/start")
def start():
    # Initialise empty domain object
    domain = Domain()

    # Execute a step
    result = step(rules, domain, subclasses, goal)

    # Store current domain in session as domain and previous domain
    session["domain"] = domain.toJson()
    session["prevDomain"] = domain.toJson()

    return result

@app.post("/answer")
def answer():
    # Save current domain for undo
    session["prevDomain"] = session["domain"]

    # Load current domain
    domain = Domain.fromJson(session["domain"])
    # Set answer from request
    domain.setFact(request.json["question"], request.json["answer"])
    # Execute a step
    result = step(rules, domain, subclasses, goal)

    # Store current domain in session
    session["domain"] = domain.toJson()

    return result

@app.post("/messageReceived")
def messageReceived():
    # Load current domain
    domain = Domain.fromJson(session["domain"])
    # Execute a step
    result = step(rules, domain, subclasses, goal)
    # Store current domain in session
    session["domain"] = domain.toJson()
    
    return result

@app.post("/undo")
def undo():
    # Restore previous domain
    session["domain"] = session["prevDomain"]

    # Load current domain
    domain = Domain.fromJson(session["domain"])
    # Execute a step
    result = step(rules, domain, subclasses, goal)

    # Store current domain in session
    session["domain"] = domain.toJson()

    return result

if __name__ == "__main__":
    app.run()
