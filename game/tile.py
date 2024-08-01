# tile.py


class Tile:
    def __init__(
        self, icon, tile_type, x, y, building=None, key=None, owners=None, height=1
    ):
        self.icon = icon
        self.tile_type = tile_type
        self.x = x
        self.y = y
        self.building = building
        self.key = key
        self.owners = set() if owners is None else owners
        self.height = height

    def add_owner(self, owner):
        self.owners.add(owner)

    def remove_owner(self, owner):
        if owner in self.owners:
            self.owners.remove(owner)

    def is_contested(self):
        return len(self.owners) > 1

    def update_building(self, building_icon, building_name):
        self.building = building_name
        self.icon = building_icon

    def to_dict(self):
        return {
            "icon": self.icon,
            "tile_type": self.tile_type,
            "x": self.x,
            "y": self.y,
            "building": self.building,
            "key": self.key,
            "owners": list(self.owners),
            "height": self.height,
        }

    def copy(self):
        return Tile(
            self.icon,
            self.tile_type,
            self.x,
            self.y,
            building=self.building,
            key=self.key,
            owners=set(self.owners),
            height=self.height,
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            icon=data["icon"],
            tile_type=data["tile_type"],
            x=data["x"],
            y=data["y"],
            building=data.get("building"),
            key=data.get("key"),
            owners=set(data.get("owners", [])),
            height=data.get("height", 1),
        )

    def __str__(self):
        return self.icon
