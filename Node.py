BLOCKED_NODE = "#"
START_NODE = "A"
GOAL_NODE = "B"

WATER_NODE = "w"
MOUNTAIN_NODE = "m"
FOREST_NODE = "f"
GRASS_NODE = "g"
ROAD_NODE = "r"

ON_PATH_CHAR = "*"
VISITED_NODE_CHAR = "X"


class Node:
    def __init__(self, char, heuristic_cost=0):
        self.char = char
        self.blocked = char == BLOCKED_NODE
        self.start_node = char == START_NODE
        self.goal_node = char == GOAL_NODE

        # Variables used for debug and printing
        self.row = None
        self.column = None
        self.on_path = False
        self.visited = False

        self.neighbours = []  # Neighbour nodes

        if char == WATER_NODE:
            self.cost = 100
        elif char == MOUNTAIN_NODE:
            self.cost = 50
        elif char == FOREST_NODE:
            self.cost = 10
        elif char == GOAL_NODE:
            self.cost = 5
        elif char == ROAD_NODE:
            self.cost = 1
        else:
            self.cost = 1

        self.travel_cost = None
        self.heuristic_cost = heuristic_cost

    def __gt__(self, other):
        return self.travel_cost + self.heuristic_cost > other.travel_cost + other.heuristic_cost

    def __str__(self):
        if self.on_path:
            return ON_PATH_CHAR
        elif self.visited:
            return VISITED_NODE_CHAR
        else:
            return self.char
