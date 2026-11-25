import os
from datetime import datetime
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for

try:
    from .questions import questions
except ImportError:
    from questions import questions

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "development-only-change-this")
score_history = Path(__file__).with_name("score_history.txt")


def reset_quiz():
    session.clear()
    session["points"] = 0
    session["hints_used"] = 0
    session["question_index"] = 0
    session["hint_count"] = 0
    session["feedback"] = None
    session["saved"] = False


@app.route("/")
def index():
    return render_template("welcome.html", total=len(questions))


@app.post("/start")
def start():
    reset_quiz()
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "question_index" not in session:
        return redirect(url_for("index"))

    index = session["question_index"]
    if index >= len(questions):
        return redirect(url_for("result"))

    question = questions[index]

    if request.method == "POST":
        if request.form.get("action") == "hint":
            hint_count = session["hint_count"]
            if hint_count < len(question["hint"]):
                session["hint_count"] = hint_count + 1
                session["hints_used"] += 1
            return redirect(url_for("quiz"))

        answer = request.form.get("answer", "").strip().upper()
        valid_answers = [option.split(":", 1)[0] for option in question["options"]]
        if answer not in valid_answers:
            session["feedback"] = "Please choose one of the available answers."
            return redirect(url_for("quiz"))

        if answer == question["answer"]:
            session["points"] += 1
            session["feedback"] = "Correct!"
        else:
            if session["points"] > 0:
                session["points"] -= 1
            session["feedback"] = f"Incorrect. The correct answer is {question['answer']}."

        session["question_index"] += 1
        session["hint_count"] = 0
        return redirect(url_for("result" if session["question_index"] >= len(questions) else "quiz"))

    hints = question["hint"][:session["hint_count"]]
    feedback = session["feedback"]
    session["feedback"] = None

    return render_template(
        "quiz.html",
        question=question,
        question_number=index + 1,
        total=len(questions),
        hints=hints,
        hint_count=session["hint_count"],
        hint_total=len(question["hint"]),
        feedback=feedback,
    )


@app.route("/result")
def result():
    if "question_index" not in session:
        return redirect(url_for("index"))

    points = session["points"]
    hints_used = session["hints_used"]

    if not session["saved"]:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with score_history.open("a", encoding="utf-8") as score_file:
            score_file.write(f"{timestamp} - {points} points - {hints_used} hints used\n")
        session["saved"] = True

    return render_template("result.html", points=points, hints_used=hints_used, total=len(questions))


@app.post("/restart")
def restart():
    reset_quiz()
    return redirect(url_for("quiz"))


if __name__ == "__main__":
    app.run(debug=True)
