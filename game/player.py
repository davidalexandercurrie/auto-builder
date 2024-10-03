from resource_types import RESOURCE_TYPES
from draw_utils import draw_turn_timer


class Player:
    def __init__(self) -> None:
        self.actions = 10
        self.resources = {resource: 0 for resource in RESOURCE_TYPES}

    def reset_actions(self):
        self.actions = 10
        draw_turn_timer(self.actions)

    def add_resource(self, resource_name, amount):
        if resource_name in RESOURCE_TYPES:
            self.resources[resource_name] += amount
            return self.resources[resource_name]
        else:
            print("Resource type does not exist")
            return None

    def use_resource(self, resource_name, amount):
        if resource_name in self.resources:
            if self.resources[resource_name] >= amount:
                self.resources[resource_name] -= amount
                return self.resources[resource_name]
            else:
                print(f"Not enough {resource_name} available to consume")
                return False
        else:
            print("Resource type does not exist")
            return False

    def use_action(self):
        if self.actions > 0:
            self.actions -= 1
            draw_turn_timer(self.actions)
            return True
        else:
            return False

    def add_actions(self, amount):
        self.actions += amount
        draw_turn_timer(self.actions)

    def initialize(self):
        """Setup initial player resources and actions."""
        self.reset_actions()
        self.add_resource("wood", 10)
        self.add_resource("metal", 5)
