from flask import Flask
import api_client

app = Flask(__name__)


@app.route("/")
def home():
    puzzle = api_client.solve_puzzle()

    if puzzle is None:
        return "Could not get a puzzle from the API. Try again later."

    print("Answer (for testing):", puzzle["fish"], "fish,", puzzle["chest"], "chests")

    return f"""
    <h1>Fish Game</h1>
    <p>Count the fish and the chests:</p>
    <img src="{puzzle['image_url']}" width="500">
    """


if __name__ == "__main__":
    app.run(debug=True)