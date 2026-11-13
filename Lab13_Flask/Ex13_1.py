# make a simple Flask application that starts a web server

from flask import Flask

my_name = "Jordan"

app = Flask(__name__)
# set a route to /
@app.route("/")
def index():
    return f"Welcome to <strong>{my_name}’s</strong> web site!"

if __name__ == "__main__":
    app.run(debug=True)
