from tile import Tile


class Command:
    def __init__(
        self,
        action,
        tile,
        data=None,
        prev_state=None,
        draw_tile=None,
        shared_state=None,
    ):
        self.action = action
        self.tile = tile
        self.data = data
        self.prev_state = prev_state
        self.draw_tile = draw_tile
        self.shared_state = shared_state

    def execute(self, map_data):
        if self.action == "build":
            self.prev_state = map_data[self.tile.y][self.tile.x].copy()
            map_data[self.tile.y][self.tile.x].update_building(
                self.data["building_icon"], self.data["building_name"]
            )
            self.draw_tile(self.tile, self.tile.x, self.tile.y, self.shared_state)

    def undo(self, map_data, player):
        if self.action == "build" and self.prev_state:
            map_data[self.tile.y][self.tile.x] = self.prev_state
            self.draw_tile(self.prev_state, self.tile.x, self.tile.y, self.shared_state)
            player.add_actions(1)

    def to_dict(self):
        return {
            "action": self.action,
            "tile": self.tile.to_dict(),
            "data": self.data,
            "prev_state": self.prev_state.to_dict() if self.prev_state else None,
        }

    @classmethod
    def from_dict(cls, data):
        prev_state_data = data.get("prev_state")
        prev_state = Tile.from_dict(prev_state_data) if prev_state_data else None
        return cls(
            action=data["action"],
            tile=Tile.from_dict(data["tile"]),
            data=data.get("data"),
            prev_state=prev_state,
        )
