from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML Template direkt im Code
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hallo Website</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            text-align: center;
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            font-size: 3em;
            margin-bottom: 30px;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.2em;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.2s, background 0.2s;
        }
        button:hover {
            background: #764ba2;
            transform: scale(1.05);
        }
        .message {
            margin-top: 20px;
            color: green;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>👋 Hallo!</h1>
        <form method="POST" action="/senden">
            <button type="submit">Hallo senden</button>
        </form>
        {% if nachricht %}
        <p class="message">{{ nachricht }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/senden", methods=["POST"])
def senden():
    # Hier kommt "Hallo" am Server an
    print("🔔 SERVER HAT EMPFANGEN: Hallo!")
    return render_template_string(HTML_PAGE, nachricht="✅ Hallo wurde an Server gesendet!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
