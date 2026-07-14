from flask import Flask, render_template_string, request
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

players = {}
scores = {}

HTML = open("index.html", "r", encoding="utf-8").read()

@app.route("/")
def home():
    return HTML

@socketio.on("connect")
def handle_connect():
    players[request.sid] = {
        "x": 0, "y": 10, "z": 0, "ry": 0,
        "name": f"Spieler_{request.sid[:6]}",
        "state": "idle",
        "anim": "idle"
    }
    scores[request.sid] = {"score": 0, "time": 0, "deaths": 0}
    socketio.emit("init", {
        "id": request.sid,
        "players": players,
        "scores": scores
    })
    socketio.emit("playerJoined", {
        "id": request.sid,
        "name": players[request.sid]["name"]
    }, skip_sid=request.sid)

@socketio.on("disconnect")
def handle_disconnect():
    name = players.get(request.sid, {}).get("name", "???")
    if request.sid in players:
        del players[request.sid]
    if request.sid in scores:
        del scores[request.sid]
    socketio.emit("playerLeft", {"id": request.sid, "name": name})

@socketio.on("move")
def handle_move(data):
    if request.sid in players:
        players[request.sid].update({
            "x": data.get("x", 0),
            "y": data.get("y", 0),
            "z": data.get("z", 0),
            "ry": data.get("ry", 0),
            "vx": data.get("vx", 0),
            "vy": data.get("vy", 0),
            "vz": data.get("vz", 0),
            "state": data.get("state", "idle"),
            "anim": data.get("anim", "idle"),
            "grounded": data.get("grounded", False)
        })
        socketio.emit("playerMoved", {
            "id": request.sid,
            "pos": {
                "x": data.get("x", 0),
                "y": data.get("y", 0),
                "z": data.get("z", 0),
                "ry": data.get("ry", 0),
                "vx": data.get("vx", 0),
                "vy": data.get("vy", 0),
                "vz": data.get("vz", 0),
                "state": data.get("state", "idle"),
                "anim": data.get("anim", "idle"),
                "grounded": data.get("grounded", False)
            },
            "name": players[request.sid]["name"]
        }, skip_sid=request.sid)

@socketio.on("checkpoint")
def handle_checkpoint(data):
    if request.sid in players:
        socketio.emit("checkpointReached", {
            "id": request.sid,
            "checkpoint": data.get("id", 0),
            "name": players[request.sid]["name"]
        })

@socketio.on("finish")
def handle_finish(data):
    if request.sid in players:
        scores[request.sid]["time"] = data.get("time", 0)
        socketio.emit("playerFinished", {
            "id": request.sid,
            "time": data.get("time", 0),
            "name": players[request.sid]["name"]
        })

@socketio.on("death")
def handle_death():
    if request.sid in players:
        scores[request.sid]["deaths"] += 1
        socketio.emit("playerDied", {
            "id": request.sid,
            "name": players[request.sid]["name"]
        })

@socketio.on("chat")
def handle_chat(data):
    msg = str(data.get("msg", "")).strip()[:200]
    if msg:
        socketio.emit("chat", {
            "id": request.sid,
            "name": players.get(request.sid, {}).get("name", "???"),
            "msg": msg
        })

@socketio.on("setName")
def handle_set_name(data):
    if request.sid in players:
        name = str(data.get("name", ""))[:20].strip()
        if name:
            old = players[request.sid]["name"]
            players[request.sid]["name"] = name
            socketio.emit("nameChanged", {
                "id": request.sid,
                "name": name,
                "oldName": old
            })

@socketio.on("admin_cmd")
def handle_admin(data):
    cmd = data.get("cmd")
    actions = {
        "kill_all": lambda: socketio.emit("admin_action", {"action": "kill_all"}),
        "speed_boost": lambda: socketio.emit("admin_action", {"action": "speed_boost"}),
        "tp_all": lambda: socketio.emit("admin_action", {"action": "tp_all", "x": 0, "y": 50, "z": 0}),
        "gravity": lambda: socketio.emit("admin_action", {"action": "gravity", "value": data.get("value", 0.5)}),
        "freeze": lambda: socketio.emit("admin_action", {"action": "freeze"}),
        "nuke": lambda: socketio.emit("admin_action", {"action": "nuke"}),
    }
    if cmd in actions:
        actions[cmd]()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
