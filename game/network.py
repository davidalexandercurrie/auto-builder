import socketio
from turn_manager import update_game_state_for_new_turn
from game_state import game_state
import config

sio = socketio.Client()


def on_connect():
    stdscr = game_state.shared_state.get("stdscr")
    if stdscr:
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, "Connected to server. Press any key to continue.")
        stdscr.refresh()


def on_disconnect():
    stdscr = game_state.shared_state.get("stdscr")
    if stdscr:
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, "Disconnected from server")
        stdscr.refresh()


def on_data(data):
    update_game_state_for_new_turn(data)


def connect_to_server():
    try:
        sio.connect(config.server_url)
    except socketio.exceptions.ConnectionError as e:
        stdscr = game_state.shared_state.get("stdscr")
        if stdscr:
            stdscr.addstr(1, 0, f"Connection error: {e}")
            stdscr.refresh()
            stdscr.getch()
            return


sio.on("connect", on_connect)
sio.on("disconnect", on_disconnect)
sio.on("updated_map_data", on_data)
