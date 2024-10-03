import curses
import sys
import threading
from network import sio, connect_to_server
from draw_utils import draw_map, draw_keys, draw_status
from input_handler import handle_key_input
from game_state import game_state
import config
import colors
import setup
import datetime
import time

sys.stdout = open("game.log", "w", buffering=1)


def map_data_to_dict():
    return [[tile.to_dict() for tile in row] for row in game_state.map_data]


def send_map_data_and_reset_timer():
    print("input disabled")
    draw_status(line1="Get Ready!", line2="Here we go again...")
    game_state.input_allowed.clear()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] Map data sent", flush=True)
    command_list = [command.to_dict() for command in game_state.commands_history]
    sio.emit("map_data", {"commands": command_list})
    game_state.commands_history.clear()
    timer = threading.Timer(10.0, send_map_data_and_reset_timer)
    timer.start()


def play(stdscr):
    send_map_data_and_reset_timer()
    draw_map(game_state.map_data, game_state.shared_state)
    draw_keys()

    stdscr.nodelay(True)

    while True:
        key = stdscr.getch()
        if key != -1 and game_state.input_allowed.is_set():
            command = handle_key_input(
                key, game_state.shared_state, game_state.map_data, config.map_win
            )
            if command == "undo":
                if game_state.commands_history:
                    last_command = game_state.commands_history.pop()
                    last_command.undo(game_state.map_data, game_state.player)
            elif command:
                command.execute(game_state.map_data)
                game_state.commands_history.append(command)

            draw_keys()
            stdscr.refresh()


def main(stdscr):
    setup.initialize_windows()
    game_state.initialize()

    game_state.shared_state["stdscr"] = stdscr
    curses.curs_set(0)
    colors.init_colors()
    stdscr.bkgd(" ", curses.color_pair(colors.WHITE_ON_BLUE))
    stdscr.clear()
    draw_status("Connecting to server...")
    time.sleep(3)
    stdscr.refresh()

    connect_to_server()

    stdscr.getch()
    draw_status(line1="Prepare Yourself!", line2="The game will begin shortly")
    game_state.input_allowed.set()

    draw_keys()
    draw_map(game_state.map_data, game_state.shared_state)

    play(stdscr)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        curses.endwin()
        print("\nGame interrupted. Terminal reset.")
