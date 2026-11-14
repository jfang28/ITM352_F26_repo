from datetime import datetime
import os
from pathlib import Path
import secrets
import sys

from flask import (
    Flask,
    flash,
    redirect,
    render_template_string,
    request,
    session,
    url_for,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSIGNMENT1_DIR = PROJECT_ROOT / "Assignment1"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Assignment1.questions import questions


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))

HOME_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Assignment 1 Quiz</title>
</head>
<body>
    <main>
        <h1>Welcome to the Assignment 1 Quiz</h1>
        <p>Answer each question by selecting its letter. You can request up to three hints per question.</p>
        <p>Each correct answer earns one point. Incorrect answers deduct one point, down to zero.</p>
        <form method="post">
            <button type="submit">Begin quiz</button>
        </form>
    </main>
</body>
</html>
"""

QUIZ_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Assignment 1 Quiz - Question {{ question_number }}</title>
</head>
<body>
    <main>
        <p>Question {{ question_number }} of {{ total_questions }}</p>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <ul aria-live="polite">
                    {% for message in messages %}
                        <li>{{ message }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
        <h1>{{ question.question }}</h1>
        <form method="post">
            {% for option in question.options %}
                {% set answer_letter = option.split(':', 1)[0].strip() %}
                <label>
                    <input type="radio" name="answer" value="{{ answer_letter }}" required>
                    {{ option }}
                </label>
                <br>
            {% endfor %}
            <button type="submit" name="action" value="answer">Submit answer</button>
            <button type="submit" name="action" value="hint" formnovalidate>Get a hint</button>
        </form>
    </main>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Quiz Results</title>
</head>
<body>
    <main>
        <h1>Quiz complete!</h1>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <ul aria-live="polite">
                    {% for message in messages %}
                        <li>{{ message }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
        <p>Your final score is {{ points }} points.</p>
        <p>You used {{ hints_used }} hints.</p>
        <p>Your score was saved to score_history.txt.</p>
        <p><a href="{{ url_for('home') }}">Take the quiz again</a></p>
    </main>
</body>
</html>
"""


def current_question():
    question_index = session.get("question_index", 0)
    if 0 <= question_index < len(questions):
        return questions[question_index]
    return None


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session.clear()
        session["question_index"] = 0
        session["points"] = 0
        session["hints_used"] = 0
        session["hint_index"] = 0
        return redirect(url_for("quiz"))
    return render_template_string(HOME_TEMPLATE)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    question = current_question()
    if question is None:
        if session.get("quiz_complete"):
            return redirect(url_for("result"))
        return redirect(url_for("home"))

    if request.method == "POST":
        if request.form.get("action") == "hint":
            hint_index = session.get("hint_index", 0)
            hints = question["hint"]
            if hint_index < len(hints):
                flash(f"Hint: {hints[hint_index]}")
                session["hint_index"] = hint_index + 1
                session["hints_used"] = session.get("hints_used", 0) + 1
            else:
                flash("You have used all available hints.")
            return redirect(url_for("quiz"))

        answer = request.form.get("answer", "").strip().upper()
        valid_answers = {
            option.split(":", 1)[0].strip().upper()
            for option in question["options"]
        }
        if answer not in valid_answers:
            flash("Please select one of the listed answer choices.")
            return redirect(url_for("quiz"))

        if answer == question["answer"]:
            session["points"] = session.get("points", 0) + 1
            flash("Correct!")
        else:
            session["points"] = max(0, session.get("points", 0) - 1)
            flash(f"Sorry, the correct answer is {question['answer']}.")

        question_index = session.get("question_index", 0) + 1
        session["question_index"] = question_index
        session["hint_index"] = 0
        if question_index == len(questions):
            session["quiz_complete"] = True
            score_history = ASSIGNMENT1_DIR / "score_history.txt"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with score_history.open("a", encoding="utf-8") as score_file:
                score_file.write(f"{timestamp} - {session['points']} points\n")
            return redirect(url_for("result"))
        return redirect(url_for("quiz"))

    return render_template_string(
        QUIZ_TEMPLATE,
        question=question,
        question_number=session.get("question_index", 0) + 1,
        total_questions=len(questions),
    )


@app.route("/result")
def result():
    if not session.get("quiz_complete"):
        return redirect(url_for("home"))
    return render_template_string(
        RESULT_TEMPLATE,
        points=session.get("points", 0),
        hints_used=session.get("hints_used", 0),
    )


if __name__ == "__main__":
    app.run(debug=True)
