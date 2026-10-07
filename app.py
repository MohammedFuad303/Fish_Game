from flask import Flask, render_template, session
import api_client
import uuid

app = Flask(__name__)
app.secret_key = "your_secret_key"  

games = {}

@app.route("/")
def home():

    session["visits"] = session.get("visits", 0) + 1

    puzzle = api_client.solve_puzzle()

    if puzzle is None:
        return "Could not get a puzzle from the API. Try again later."

    game_id = str(uuid.uuid4())
    games[game_id] = {"fish": puzzle["fish"], "chest": puzzle["chest"]}
    session["game_id"] = game_id

    print("Answers are stored on the server:", games)

    return render_template("index.html", image_url=puzzle["image_url"], visits=session["visits"], score=0, rounds=0)


if __name__ == "__main__":
    app.run(debug=True)