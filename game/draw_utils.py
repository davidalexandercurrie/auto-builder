# draw_utils.py
import curses
import config
from tile_types import TILE_TYPES


def draw_tile(tile, x, y, shared_state):
    selected = x == shared_state["selected_x"] and y == shared_state["selected_y"]
    offset = 1 if y % 2 == 0 else 0
    if selected:
        config.map_win.addstr(y, x * 2 + offset, str(tile), curses.A_REVERSE)
    else:
        config.map_win.addstr(y, x * 2 + offset, str(tile))
    config.map_win.refresh()


def draw_map(map_data, shared_state):
    config.map_win.clear()
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            draw_tile(tile, x, y, shared_state)
    config.map_win.refresh()


def draw_keys():
    key_descriptions = [
        "Controls:",
        "WASD: Move cursor",
    ]

    for key, (icon, name) in TILE_TYPES.items():
        key_descriptions.append(f"{key}: {name} {icon}")

    config.key_win.clear()
    for i, description in enumerate(key_descriptions):
        config.key_win.addstr(i, 0, description)
    config.key_win.refresh()


def draw_status(line1=None, line2=None):
    config.status_win.clear()
    if line1:
        config.status_win.addstr(0, 0, line1)
    if line2:
        config.status_win.addstr(1, 0, line2)
    config.status_win.refresh()
