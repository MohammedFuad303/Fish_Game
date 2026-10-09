import uuid
from flask import Flask, render_template, session, request, redirect, url_for
import api_client
import game_logic
from werkzeug.security import generate_password_hash, check_password_hash
import storage

app = Flask(__name__)
app.secret_key = "dev-secret-change-later"
storage.create_tables()

games = {}  
#users = {}   

@app.route("/")
def home():
    session["visits"] = session.get("visits", 0) + 1

    puzzle = api_client.solve_puzzle()
    if puzzle is None:
        return "Could not get a puzzle from the API. Try again later."

    game_id = str(uuid.uuid4())
    games[game_id] = {"fish": puzzle["fish"], "chest": puzzle["chest"]}
    session["game_id"] = game_id

    message = session.pop("message", "")

    return render_template("index.html",
                           image_url=puzzle["image_url"],
                           score=session.get("score", 0),
                           rounds=session.get("rounds", 0),
                           visits=session["visits"],
                           username=session.get("username"), 
                           message=message)
#session.get()"username") gives the name if somebody is logged in, or None if nobody is logged in

@app.route("/guess", methods=["POST"])
def guess():

    try:
        fish = int(request.form["fish"])
        chest = int(request.form["chest"])
    except ValueError:
        return "Please return whole numbers for both fish and chests. <a href='/'>Back to the game</a>"

    answer = games.pop(session.get("game_id"), None)

    if answer is None:
        return "Game session expired or invalid. <a href='/'>Start a new game</a>"

    session["rounds"] = session.get("rounds", 0) + 1

    correct = game_logic.check_answer(answer, fish, chest)
    if correct:
        session["score"] = session.get("score", 0) + 1

    if session.get("username"):
        storage.save_score(session["username"], session.get("score", 0), session["rounds"])

    if correct:
        return "Correct! <a href='/'>Next puzzzle</a>"
    return f"Wrong. It was {answer['fish']} fish and {answer['chest']} chests. <a href='/'>Next puzzle</a>" 

    #if game_logic.check_answer(answer, fish, chest):
            #session["score"] = session.get("score", 0) + 1
            #return "Correct! <a href='/'>Next puzzle</a>"
    #else:
        #return f"Wrong. It was {answer['fish']} fish and {answer['chest']} chests. <a href='/'>Next puzzle</a>"     


@app.route("/register", methods = ["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if username == "" or password == "":
            message = "Please fill in both boxes"
        else:
            saved = storage.add_user(username, generate_password_hash(password))
            if saved:
                message = "Account created!"
            else:
                message = "The username is already taken."
    return render_template("register.html", message=message)


@app.route("/login", methods = ["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        stored_hash = storage.get_password_hash(username)

        if stored_hash is not None and check_password_hash(stored_hash, password):
            session["username"] = username  #stores who logged in
            score, rounds = storage.get_score(username) #storage.get_score(username) returns two values and score, rounds= unpacks them into two variables
            session["score"] = score
            session["rounds"] = rounds
            return redirect(url_for("home"))  #sends back to the home page
        else:
            message = "Wrong username or password"
    return render_template("login.html", message=message)

@app.route("/logout")
def logout():
    session.pop("username", None) #session.pop("username", None) removes the username from the session. The None is there so that it doesn't crash if it isn't there
    session.pop("score", None)
    session.pop("rounds", None)
    return redirect(url_for("home")) #sends the player back to the game

if __name__ == "__main__":
    app.run(debug=True)