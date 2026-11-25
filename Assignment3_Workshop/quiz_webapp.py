from flask import Flask, redirect, render_template, request, session, url_for

try:
    from .questions import questions
except ImportError:
    from questions import questions

app = Flask(__name__)
app.secret_key = "development-only-change-this"


@app.route("/")
def index():
    return render_template("index.html")


def start_quiz():
    session["score"] = 0
    session["question_index"] = 0
    session["hints_used"] = 0
    session["hint_index"] = 0
    session["feedback"] = ""


def grade_answer(question, answer):
    if answer == question["answer"]:
        session["score"] += 1
        return "Correct!"

    if session["score"] > 0:
        session["score"] -= 1
    return f"Incorrect. The correct answer is {question['answer']}."


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "question_index" not in session or session["question_index"] >= len(questions):
        start_quiz()

    question_index = session["question_index"]
    question = questions[question_index]

    if request.method == "POST":
        if request.form.get("action") == "hint":
            hint_index = session["hint_index"]
            if hint_index < len(question["hint"]):
                session["hint_index"] = hint_index + 1
                session["hints_used"] += 1
            return redirect(url_for("quiz"))

        answer = request.form.get("answer", "").strip().upper()
        valid_answers = [option.split(":", 1)[0] for option in question["options"]]
        if answer not in valid_answers:
            session["feedback"] = "Please choose one of the available answers."
            return redirect(url_for("quiz"))

        session["feedback"] = grade_answer(question, answer)
        session["question_index"] += 1
        session["hint_index"] = 0
        if session["question_index"] >= len(questions):
            return redirect(url_for("result"))
        return redirect(url_for("quiz"))

    feedback = session.pop("feedback", "")
    return render_template(
        "quiz.html",
        question=question,
        question_number=question_index + 1,
        total_questions=len(questions),
        hints=question["hint"][:session["hint_index"]],
        hints_remaining=len(question["hint"]) - session["hint_index"],
        feedback=feedback,
    )


@app.route("/result")
def result():
    if session.get("question_index") != len(questions):
        return redirect(url_for("index"))
    return render_template(
        "result.html",
        score=session["score"],
        total_questions=len(questions),
        hints_used=session["hints_used"],
    )


if __name__ == "__main__":
    app.run(debug=True)
