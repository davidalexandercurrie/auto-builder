from player import Player
import threading
import config
from tile import Tile
import random


class GameState:
    def __init__(self):
        self.player = Player()
        self.shared_state = {}
        self.input_allowed = threading.Event()
        self.input_allowed.set()

    def initialize(self):
        """Initialize all game state components."""
        self.shared_state["selected_x"] = 0
        self.shared_state["selected_y"] = 0
        self.player.add_resource("wood", 10)
        self.player.add_resource("metal", 5)
        self.commands_history = []
        self.map_data = [
            [
                (
                    Tile(["🌴", "0"], "forest", x, y)
                    if random.random() > 0.8
                    else Tile(["🌾", "0"], "empty", x, y)
                )
                for x in range(config.MAP_WIDTH)
            ]
            for y in range(config.MAP_HEIGHT)
        ]


game_state = GameState()
