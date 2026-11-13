#Create a simple Flask application to retrieve memes from https://meme-api.com/gimme/wholesomememes.  To get the memes you will need to issue a requests.request("GET", url) command.Present the meme and the meme source (subreddit) to the user. Refresh the meme every 10 seconds.  You can accomplish this by including the following <meta> tags in the <head> of your HTML page.

from flask import Flask, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def index():
    response = requests.request("GET", "https://meme-api.com/gimme/wholesomememes")
    data = response.json()
    meme = data['url']
    subreddit = data['subreddit']
    html = f"""
    <html>
    <head>
       <title>Memes'R'Us</title>
       <meta charset="UTF-8" name="viewport" content="width=device-width, initial-scale=0.8">
       <meta http-equiv="refresh" content="10; url=http://127.0.0.1:5000" />
    </head>
    <body>
       <h1>{subreddit}</h1>
       <img src="{meme}" alt="Meme">
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)