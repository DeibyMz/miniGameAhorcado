import random
import unicodedata


MAX_ERRORS = 10


def normalize(text):
    text = text.lower().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


class HangmanGame:
    def __init__(self, words):
        self.words = words
        self.new_game()

    def new_game(self):
        self.word = normalize(random.choice(self.words))
        self.guessed = set()
        self.errors = 0
        self.finished = False
        self.won = False

    def guess(self, letter):
        letter = normalize(letter)

        if len(letter) != 1 or not letter.isalpha():
            return False, "Ingresa una sola letra."

        if self.finished:
            return False, "La partida ya terminó."

        if letter in self.guessed:
            return False, "Ya utilizaste esa letra."

        self.guessed.add(letter)

        if letter not in self.word:
            self.errors += 1

        if all(char in self.guessed for char in self.word):
            self.finished = True
            self.won = True

        elif self.errors >= MAX_ERRORS:
            self.finished = True
            self.won = False

        return True, None

    def get_state(self):
        hidden_word = [
            char if char in self.guessed else "_"
            for char in self.word
        ]

        return {
            "word": " ".join(hidden_word),
            "errors": self.errors,
            "max_errors": MAX_ERRORS,
            "guessed": sorted(self.guessed),
            "finished": self.finished,
            "won": self.won,
            "answer": self.word if self.finished else None,
        }