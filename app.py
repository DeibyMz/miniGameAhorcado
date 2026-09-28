from flask import Flask, render_template, request, jsonify

from game import HangmanGame
from words import WORDS


app = Flask(__name__)

game = HangmanGame(WORDS)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state")
def state():
    return jsonify(game.get_state())


@app.route("/api/guess", methods=["POST"])
def guess():
    data = request.get_json()
    letter = data.get("letter", "")

    valid, message = game.guess(letter)

    return jsonify({
        "valid": valid,
        "message": message,
        "state": game.get_state()
    })


@app.route("/api/new-game", methods=["POST"])
def new_game():
    game.new_game()

    return jsonify(game.get_state())


if __name__ == "__main__":
    app.run(debug=True)