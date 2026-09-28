const letterInput = document.getElementById("letter");
const guessButton = document.getElementById("guessButton");
const newGameButton = document.getElementById("newGameButton");

const wordElement = document.getElementById("word");
const errorsElement = document.getElementById("errors");
const guessedElement = document.getElementById("guessed");
const messageElement = document.getElementById("message");


async function loadState() {
    const response = await fetch("/api/state");
    const state = await response.json();

    updateInterface(state);
}


async function guessLetter() {
    const letter = letterInput.value.trim();

    if (!letter) {
        return;
    }

    const response = await fetch("/api/guess", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            letter: letter
        })
    });

    const data = await response.json();

    if (data.message) {
        messageElement.textContent = data.message;
    } else {
        messageElement.textContent = "";
    }

    updateInterface(data.state);

    letterInput.value = "";
    letterInput.focus();
}


async function newGame() {
    const response = await fetch("/api/new-game", {
        method: "POST"
    });

    const state = await response.json();

    messageElement.textContent = "";
    updateInterface(state);

    letterInput.value = "";
    letterInput.focus();
}


function updateInterface(state) {

    wordElement.textContent = state.word;

    errorsElement.textContent = state.errors;

    guessedElement.textContent = state.guessed.join(", ");

    for (let i = 1; i <= state.max_errors; i++) {
        const part = document.getElementById(`part-${i}`);

        if (i <= state.errors) {
            part.classList.add("visible");
        } else {
            part.classList.remove("visible");
        }
    }

    if (state.finished) {

        if (state.won) {
            messageElement.textContent = "¡Ganaste!";
        } else {
            messageElement.textContent =
                `Perdiste. La palabra era: ${state.answer}`;
        }
    }
}


guessButton.addEventListener("click", guessLetter);

newGameButton.addEventListener("click", newGame);

letterInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        guessLetter();
    }
});


loadState();