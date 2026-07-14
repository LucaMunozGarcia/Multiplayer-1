from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

players = {}

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    players[request.sid] = {
        "x": 0, "y": 5, "z": 0,
        "rx": 0, "ry": 0
    }
    emit("init", {"id": request.sid, "players": players}, broadcast=True)
    print(f"Spieler verbunden: {request.sid}")

@socketio.on("disconnect")
def handle_disconnect():
    if request.sid in players:
        del players[request.sid]
    emit("playerLeft", {"id": request.sid}, broadcast=True)
    print(f"Spieler getrennt: {request.sid}")

@socketio.on("move")
def handle_move(data):
    if request.sid in players:
        players[request.sid] = data
        emit("playerMoved", {"id": request.sid, "pos": data}, broadcast=True, include_self=False)

@socketio.on("chat")
def handle_chat(data):
    emit("chat", {"id": request.sid, "msg": data["msg"]}, broadcast=True)

# Admin Befehle
@socketio.on("admin_cmd")
def handle_admin(data):
    cmd = data.get("cmd")
    if cmd == "kill_all":
        emit("admin_action", {"action": "kill_all"}, broadcast=True)
    elif cmd == "speed_boost":
        emit("admin_action", {"action": "speed_boost", "target": data.get("target", "all")}, broadcast=True)
    elif cmd == "tp_all":
        emit("admin_action", {"action": "tp_all", "x": 0, "y": 50, "z": 0}, broadcast=True)
    elif cmd == "gravity":
        emit("admin_action", {"action": "gravity", "value": data.get("value", 0.5)}, broadcast=True)
    elif cmd == "freeze":
        emit("admin_action", {"action": "freeze"}, broadcast=True)
    elif cmd == "nuke":
        emit("admin_action", {"action": "nuke"}, broadcast=True)
    print(f"ADMIN CMD: {cmd}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
