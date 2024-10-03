from tile_types import TILE_TYPES
from draw_utils import draw_tile
from command import Command
from game_state import game_state


def handle_key_input(key, shared_state, map_data, map_win):
    current_x = shared_state["selected_x"]
    current_y = shared_state["selected_y"]

    command = None

    if key == ord("w") and shared_state["selected_y"] > 0:
        shared_state["selected_y"] -= 1
    elif key == ord("s") and shared_state["selected_y"] < len(map_data) - 1:
        shared_state["selected_y"] += 1
    elif key == ord("a") and shared_state["selected_x"] > 0:
        shared_state["selected_x"] -= 1
    elif key == ord("d") and shared_state["selected_x"] < len(map_data[0]) - 1:
        shared_state["selected_x"] += 1
    elif key == ord("u"):
        command = "undo"
    elif chr(key) in TILE_TYPES:
        if game_state.player.use_action():
            tile_info = TILE_TYPES[chr(key)]
            building_icon = tile_info["symbol"]
            building_name = tile_info["name"]
            tile = map_data[shared_state["selected_y"]][shared_state["selected_x"]]
            command = Command(
                "build",
                tile,
                {"building_icon": building_icon, "building_name": building_name},
                prev_state=tile.copy(),
                draw_tile=lambda t, x, y, s: draw_tile(t, x, y, s),
                shared_state=shared_state,
            )
        else:
            print("No actions available!")

    new_x = shared_state["selected_x"]
    new_y = shared_state["selected_y"]

    if new_x != current_x or new_y != current_y:
        draw_tile(map_data[current_y][current_x], current_x, current_y, shared_state)
        draw_tile(map_data[new_y][new_x], new_x, new_y, shared_state)

    return command
