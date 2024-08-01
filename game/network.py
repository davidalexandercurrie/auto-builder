import socketio
from draw_utils import draw_status

sio = socketio.Client()


def setup_network_deps(deps):
    global external_deps
    global server_url
    external_deps = deps
    server_url = deps["server_url"]


def on_connect():
    stdscr = external_deps["shared_state"].get("stdscr")
    if stdscr:
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, "Connected to server. Press any key to continue.")
        stdscr.refresh()


def on_disconnect():
    stdscr = external_deps["shared_state"].get("stdscr")
    if stdscr:
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, "Disconnected from server")
        stdscr.refresh()


def on_data(data):
    print("map_update_received")
    external_deps["input_allowed"].set()
    print("input enabled")
    draw_status(line1="Turn Starts now", line2="Let's Go!")


def connect_to_server():
    try:
        sio.connect(server_url)
    except socketio.exceptions.ConnectionError as e:
        stdscr = external_deps["shared_state"].get("stdscr")
        if stdscr:
            stdscr.addstr(1, 0, f"Connection error: {e}")
            stdscr.refresh()
            stdscr.getch()
            return


sio.on("connect", on_connect)
sio.on("disconnect", on_disconnect)
sio.on("updated_map_data", on_data)
