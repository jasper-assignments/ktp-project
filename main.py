from flask import Flask, send_file, session, request, abort

app = Flask(__name__)
app.secret_key = "verysecretkey"

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
    if (not session.get("questions")):
        # Hasn't triggered start before answering
        abort(400)
    if (not question_id in session.get("questions")):
        # Bad question id
        abort(400)
    session["questions"][question_id]["answer"] = True
    return session.get("questions")
