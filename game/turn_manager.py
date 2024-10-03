from game_state import game_state
from draw_utils import draw_status


def update_game_state_for_new_turn(data):
    print("Updating game state for new turn")
    print("map_update_received")
    game_state.input_allowed.set()
    print("input enabled")
    draw_status(line1="Turn Starts now", line2="Let's Go!")
    game_state.player.reset_actions()
