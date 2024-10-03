from flask import Flask, request
from flask_socketio import SocketIO, emit
import eventlet
import time

app = Flask(__name__)
socketio = SocketIO(app)

port = 3000


# Define the structure of a single tile
class Tile:
    def __init__(self, icon, tile_type, building=None, key=None, owners=None, height=0):
        self.icon = icon
        self.tile_type = tile_type
        self.building = building
        self.key = key
        self.owners = owners if owners is not None else []
        self.height = height


# Define the structure for the entire map data
# MapData is a list of list of Tile objects
MapData = [[Tile(icon="example_icon", tile_type="example_type")]]


# Routes
@app.route("/")
def hello_world():
    return "Hello, World!"


# Socket.IO
@socketio.on("connect")
def handle_connect():
    print("A user connected:", request.sid)


@socketio.on("disconnect")
def handle_disconnect():
    print("A user disconnected:", request.sid)


@socketio.on("map_data")
def handle_map_data(data):
    print("Received map data:", data)
    time.sleep(3)
    print("waited 3 seconds")
    emit("updated_map_data", {"data": data}, to=request.sid)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=port)
    print(f"Running on {port}")
