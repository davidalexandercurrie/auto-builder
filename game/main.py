# main.py

import curses
import sys
import threading
from tile import Tile
from network import sio, setup_network_deps, connect_to_server
from draw_utils import draw_map, draw_keys, draw_status
from input_handler import handle_key_input
import config
import colors
import random
import setup
import datetime
import time

sys.stdout = open("game.log", "w", buffering=1)


map_data = [
    [
        (
            Tile("🌴", "forest", x, y)
            if random.random() > 0.8
            else Tile(".", "empty", x, y)
        )
        for x in range(config.MAP_WIDTH)
    ]
    for y in range(config.MAP_HEIGHT)
]

shared_state = {
    "selected_x": 0,
    "selected_y": 0,
}

commands = []
commands_history = []

input_allowed = threading.Event()
input_allowed.set()


def map_data_to_dict(map_data):
    return [[tile.to_dict() for tile in row] for row in map_data]


def send_map_data_and_reset_timer():
    global commands_history
    print("input disabled")
    draw_status(line1="Get Ready!", line2="Here we go again...")
    input_allowed.clear()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] Map data sent", flush=True)
    command_list = [command.to_dict() for command in commands_history]
    sio.emit("map_data", {"commands": command_list})
    commands_history.clear()
    timer = threading.Timer(10.0, send_map_data_and_reset_timer)
    timer.start()


def play(stdscr):
    draw_map(map_data, shared_state)
    draw_keys()

    stdscr.nodelay(True)

    while True:
        key = stdscr.getch()
        if key != -1 and input_allowed.is_set():
            command = handle_key_input(key, shared_state, map_data, config.map_win)
            if command == "undo":
                if commands_history:
                    last_command = commands_history.pop()
                    last_command.undo(map_data)
            elif command:
                command.execute(map_data)
                commands_history.append(command)

            draw_keys()
            stdscr.refresh()


def main(stdscr):
    setup.initialize_windows()
    shared_state["stdscr"] = stdscr
    curses.curs_set(0)
    colors.init_colors()
    stdscr.bkgd(" ", curses.color_pair(colors.WHITE_ON_BLUE))
    stdscr.clear()
    draw_status("Connecting to server...")
    time.sleep(3)
    stdscr.refresh()

    setup_network_deps(
        {
            "map_data_to_dict": map_data_to_dict,
            "draw_map": draw_map,
            "Tile": Tile,
            "curses": curses,
            "server_url": "http://localhost:3000",
            "shared_state": shared_state,
            "map_data": map_data,
            "input_allowed": input_allowed,
        }
    )

    connect_to_server()

    stdscr.getch()
    timer = threading.Timer(10.0, send_map_data_and_reset_timer)
    timer.start()
    draw_status(line1="Prepare Yourself!", line2="The game will begin shortly")
    input_allowed.set()

    draw_keys()
    draw_map(map_data, shared_state)

    play(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
