from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

# Erlaube Zugriffe von anderer Website
CORS(app)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Hallo Website</title>
</head>
<body style="font-family:Arial;text-align:center;margin-top:100px;">
    <h1>Hallo!</h1>
    <button onclick="sendenHallo()">Hallo senden</button>
    <p id="antwort"></p>

    <script>
        async function sendenHallo() {
            const res = await fetch('/api/hallo', {
                method: 'POST'
            });
            const data = await res.json();
            document.getElementById('antwort').innerText = data.message;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/api/hallo", methods=["POST"])
def api_hallo():
    print("SERVER HAT EMPFANGEN: Hallo von Website")
    return jsonify({"message": "Hallo wurde an den Server gesendet!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
