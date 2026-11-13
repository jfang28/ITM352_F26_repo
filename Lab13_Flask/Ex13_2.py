from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

USERS = {
    "port": "port123",
    "kazman": "kazman123",
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if USERS.get(username) == password:
            return redirect(url_for("success"))

        return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html")


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)