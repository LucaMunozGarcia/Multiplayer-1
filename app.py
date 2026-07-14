from flask import Flask, render_template_string, request
from flask_cors import CORS
from flask_socketio import SocketIO
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

players = {}

HTML = open("index.html", "r", encoding="utf-8").read()

@app.route("/")
def home():
    return HTML

@socketio.on("connect")
def handle_connect():
    players[request.sid] = {"x": 0, "y": 5, "z": 0, "ry": 0}
    socketio.emit("init", {"id": request.sid, "players": players})

@socketio.on("disconnect")
def handle_disconnect():
    if request.sid in players:
        del players[request.sid]
    socketio.emit("playerLeft", {"id": request.sid})

@socketio.on("move")
def handle_move(data):
    if request.sid in players:
        players[request.sid] = data
        socketio.emit("playerMoved", {"id": request.sid, "pos": data}, skip_sid=request.sid)

@socketio.on("chat")
def handle_chat(data):
    socketio.emit("chat", {"id": request.sid, "msg": data["msg"]})

@socketio.on("admin_cmd")
def handle_admin(data):
    cmd = data.get("cmd")
    if cmd == "kill_all":
        socketio.emit("admin_action", {"action": "kill_all"})
    elif cmd == "speed_boost":
        socketio.emit("admin_action", {"action": "speed_boost"})
    elif cmd == "tp_all":
        socketio.emit("admin_action", {"action": "tp_all", "x": 0, "y": 50, "z": 0})
    elif cmd == "gravity":
        socketio.emit("admin_action", {"action": "gravity", "value": data.get("value", 0.5)})
    elif cmd == "freeze":
        socketio.emit("admin_action", {"action": "freeze"})
    elif cmd == "nuke":
        socketio.emit("admin_action", {"action": "nuke"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
