class Node:
    id = 1

    def __init__(self, position, parent=None):
        self.id = Node.id
        self.position = position
        self.expansion_sequence = -1
        self.children = []
        self.actions = []
        self.removed = False
        self.parent = parent
        Node.id += 1

    def remove(self):
        self.removed = True

    def toDict(self):
        if self.parent != None:
            return {
                "id": self.id,
                "state": str(self.position)[1:-1],
                "expansionsequence": self.expansion_sequence,
                "children": [child.id for child in self.children],
                "actions": self.actions,
                "removed": self.removed,
                "parent": self.parent.id
            }
        else:
            return {
                "id": self.id,
                "state": str(self.position)[1:-1],
                "expansionsequence": self.expansion_sequence,
                "children": [child.id for child in self.children],
                "actions": self.actions,
                "removed": self.removed,
                "parent": None
            }

    def expand(self, maze_size, expansion_sequence):
        # Generate side locations
        points = [
            [self.position[0], max(self.position[1]-1, 0)
             ],                 # North
            [self.position[0], min((self.position[1]+1),
                                   maze_size[0]-1)],  # South
            [min(self.position[0]+1, maze_size[0]-1),
             self.position[1]],     # East
            [max(self.position[0]-1, 0), self.position[1]
             ]                   # West
        ]
        actions = ["n", "s", "e", "w"]

        # Remove center duplicates
        for i in range(points.count(self.position)):
            del actions[points.index(self.position)]
            del points[points.index(self.position)]

        # Create child object and add them into the parent's children
        for point in points:
            self.children.append(Node(point, self))

        # Modify actions, and expansion sequence
        self.actions = actions
        self.expansion_sequence = expansion_sequence

        return self.children


class Player():
    name = "Breadth-First Seach"
    informed = False
    group = "Artificial Codeine"
    members = ["Michael Lu Han Xien", "18081588",
               "Garv Sudhir Nair", "19073535",
               "Yong Tze Min", "19079748",
               "Anjali Radha Krishna", "16009847"]

    def __init__(self, setup):
        Player.maze_size = setup["maze_size"]
        self.static_length = setup["static_snake_length"]

    def run(self, problem):
        snake_locations = problem["snake_locations"]
        current_direction = problem["current_direction"]
        food_locations = problem["food_locations"]

        frontiers = [Node(snake_locations[0])]
        node_list = frontiers.copy()
        checked = snake_locations.copy()
        expansion_sequence = 1
        food_found = False

        while not food_found:
            children = frontiers[0].expand(
                Player.maze_size, expansion_sequence)
            node_list.extend(children)
            checked.append(frontiers[0].position)
            del frontiers[0]
            traceback = None
            next_node = None

            for child in children:
                if child.position in checked or child.position in [f.position for f in frontiers]:
                    child.remove()
                elif child.position in food_locations:
                    food_found = True
                    traceback = child
                else:
                    frontiers.append(child)

            expansion_sequence += 1

        if traceback.parent != None:
            next_node = traceback
            traceback = traceback.parent

        solution = traceback.actions[traceback.children.index(next_node)]
        search_tree = [node.toDict() for node in node_list]
        return solution, search_tree