from flask import Flask, jsonify, render_template_string
import random

app = Flask(__name__)

secret_number = None
attempts = 0

# Updated styling starts here
html_code = """
<!DOCTYPE html>
<html>
<head>
  <title>🚀 Neon Guess Master</title>
  <style>
    :root {
      --primary: #00f2ff;
      --secondary: #7000ff;
      --accent: #ff007b;
      --bg: #0a0a12;
    }

    body {
      margin: 0;
      font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: var(--bg);
      background-image: 
        radial-gradient(circle at 20% 30%, rgba(112, 0, 255, 0.2) 0%, transparent 40%),
        radial-gradient(circle at 80% 70%, rgba(0, 242, 255, 0.15) 0%, transparent 40%);
      overflow: hidden;
    }

    .box {
      background: rgba(20, 20, 35, 0.8);
      backdrop-filter: blur(15px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 40px;
      border-radius: 24px;
      width: 380px;
      text-align: center;
      color: white;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    h2 {
      font-size: 2rem;
      margin-bottom: 20px;
      background: linear-gradient(to right, var(--primary), var(--secondary));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-transform: uppercase;
      letter-spacing: 2px;
    }

    input {
      padding: 15px;
      width: 80%;
      border-radius: 12px;
      border: 2px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.3);
      color: var(--primary);
      font-size: 1.2rem;
      font-weight: bold;
      text-align: center;
      margin-bottom: 15px;
      outline: none;
      transition: 0.3s;
    }

    input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }

    button {
      padding: 15px;
      width: 100%;
      border: none;
      border-radius: 12px;
      margin-bottom: 12px;
      cursor: pointer;
      font-weight: 800;
      text-transform: uppercase;
      transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    #startBtn {
      background: linear-gradient(45deg, var(--secondary), #480091);
      color: white;
      box-shadow: 0 4px 15px rgba(112, 0, 255, 0.4);
    }

    #guessBtn {
      background: linear-gradient(45deg, var(--primary), #00a8b1);
      color: #0a0a12;
      box-shadow: 0 4px 15px rgba(0, 242, 255, 0.4);
    }

    button:hover:not(:disabled) {
      transform: translateY(-3px);
      filter: brightness(1.2);
    }

    button:active {
      transform: scale(0.98);
    }

    button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      filter: grayscale(1);
    }

    #message {
      margin: 15px 0;
      padding: 12px;
      border-radius: 12px;
      font-size: 0.95rem;
      min-height: 20px;
      transition: 0.3s;
    }

    /* Message States */
    .low { color: #00d4ff; border-left: 4px solid #00d4ff; background: rgba(0, 212, 255, 0.1); }
    .high { color: #ffbc00; border-left: 4px solid #ffbc00; background: rgba(255, 188, 0, 0.1); }
    .win { color: #00ff88; border-left: 4px solid #00ff88; background: rgba(0, 255, 136, 0.1); animation: pulse 1.5s infinite; }
    .error { color: #ff4d4d; border-left: 4px solid #ff4d4d; background: rgba(255, 77, 77, 0.1); }

    @keyframes pulse {
      0% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.4); }
      70% { box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
      100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
    }

    #attempts {
      font-size: 0.8rem;
      color: rgba(255, 255, 255, 0.5);
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    #historyBox {
      margin-top: 20px;
      text-align: left;
      height: 180px;
      overflow-y: auto;
      background: rgba(0, 0, 0, 0.2);
      padding: 15px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }

    #historyBox b {
      color: var(--primary);
      font-size: 0.8rem;
      display: block;
      margin-bottom: 10px;
    }

    #historyList {
      list-style: none;
      padding: 0;
      margin: 0;
    }

    #historyList li {
      margin-bottom: 8px;
      padding: 8px 12px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.03);
      font-size: 0.9rem;
      border-right: 2px solid var(--secondary);
      animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
      from { opacity: 0; transform: translateX(10px); }
      to { opacity: 1; transform: translateX(0); }
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--secondary); border-radius: 10px; }
  </style>
</head>
<body>

<div class="box">
  <h2>🎯 Guess Master</h2>

  <button id="startBtn" onclick="startGame()">Initialize Game</button>

  <input type="number" id="guessInput" placeholder="1 - 100" disabled>
  <button id="guessBtn" onclick="makeGuess()" disabled>Submit Guess</button>

  <p id="attempts">System Ready</p>
  <div id="message"></div>

  <div id="historyBox">
    <b>LOG_HISTORY</b>
    <ul id="historyList"></ul>
  </div>
</div>

<script>
async function startGame() {
  const res = await fetch("/start");
  const data = await res.json();

  document.getElementById("guessInput").disabled = false;
  document.getElementById("guessBtn").disabled = false;

  document.getElementById("attempts").innerText = "Attempts: 0";
  document.getElementById("historyList").innerHTML = "";

  showMessage(data.message, "low");
}

async function makeGuess() {
  const num = document.getElementById("guessInput").value;

  if (!num) {
    showMessage("Input required!", "error");
    return;
  }

  const res = await fetch("/guess/" + num);
  const data = await res.json();

  showMessage(data.message, data.result);

  document.getElementById("attempts").innerText = 
    "Attempts Counter: " + data.attempts;

  const list = document.getElementById("historyList");

  const li = document.createElement("li");
  li.innerText = "> Guess: " + num;
  list.prepend(li); // Put newest on top for better UX

  if (data.result === "win") {
    document.getElementById("guessInput").disabled = true;
    document.getElementById("guessBtn").disabled = true;
  }

  document.getElementById("guessInput").value = "";
}

function showMessage(text, type) {
  const msg = document.getElementById("message");
  msg.innerText = text;
  msg.className = type;
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_code)

@app.route("/start")
def start_game():
    global secret_number, attempts
    secret_number = random.randint(1, 100)
    attempts = 0
    return jsonify({"message": "Target locked. Guess between 1-100."})

@app.route("/guess/<int:num>")
def guess(num):
    global secret_number, attempts
    attempts += 1
    if num < secret_number:
        return jsonify({"message": "🔼 TOO LOW! INCREASE POWER.", "result": "low", "attempts": attempts})
    elif num > secret_number:
        return jsonify({"message": "🔽 TOO HIGH! REDUCE POWER.", "result": "high", "attempts": attempts})
    else:
        return jsonify({"message": f"🏆 MISSION SUCCESS! FOUND IN {attempts} TRIES.", "result": "win", "attempts": attempts})

if __name__ == "__main__":
    app.run(debug=True)