from flask import Flask, render_template
import api_client

app = Flask(__name__)


@app.route("/")
def home():
    puzzle = api_client.solve_puzzle()

    if puzzle is None:
        return "Could not get a puzzle from the API. Try again later."

    print("Answer (for testing):", puzzle["fish"], "fish,", puzzle["chest"], "chests")

    return render_template("index.html", image_url=puzzle["image_url"], score=0)


if __name__ == "__main__":
    app.run(debug=True)