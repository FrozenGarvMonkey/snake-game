class Node:
    id = 1

    def __init__(self, position, parent=None, cost=0):
        self.id = Node.id
        self.position = position
        self.expansion_sequence = -1
        self.cost = cost
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

    def expand(self, maze_size, expansion_sequence, sB, food):
        # Generate side locations
        points = [
            [self.position[0], max(self.position[1]-1, 0)],  # North

            [self.position[0], min((self.position[1]+1),     # South
                                   maze_size[0]-1)],

            [min(self.position[0]+1, maze_size[0]-1),        # East
             self.position[1]],

            [max(self.position[0]-1, 0), self.position[1]]   # West
        ]

        actions = ["n", "s", "e", "w"]

        # Remove center duplicates
        for i in range(points.count(self.position)):
            del actions[points.index(self.position)]
            del points[points.index(self.position)]

        # Create child object and add them into the parent's children
        for point in points:
            # Manhattan Distance (sB: Snake Head, food: Nearest food location)
            hC = (abs(sB[0] - food[0]) + abs(sB[1] - food[1]))
            self.children.append(
                Node(point, self, (self.cost + hC + 1)))

        # Modify actions, and expansion sequence
        self.actions = actions
        self.expansion_sequence = expansion_sequence

        return self.children


class Player():
    name = "A* Search"
    informed = True
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
        food_locations = problem["food_locations"]

        frontiers = [Node(snake_locations[0])]
        node_list = frontiers.copy()
        checked = snake_locations.copy()
        expansion_sequence = 1
        food_found = False

        while not food_found:
            if frontiers[0].position in food_locations:
                food_found = True
                traceback = frontiers[0]
                continue

            children = frontiers[0].expand(
                Player.maze_size, expansion_sequence, snake_locations[0], food_locations[0])
            node_list.extend(children)
            checked.append(frontiers[0].position)
            del frontiers[0]

            traceback = None
            next_node = None

            for child in children:

                if child.position not in checked:

                    if child.position in [f.position for f in frontiers]:

                        index = [f.position for f in frontiers].index(
                            child.position)

                        if child.cost < frontiers[index].cost:
                            frontiers[index].remove()
                            del frontiers[index]
                            frontiers.append(child)

                        else:
                            child.remove()

                    else:
                        frontiers.append(child)

            expansion_sequence += 1
            frontiers = sorted(frontiers, key=lambda x: x.cost, reverse=False)

        while traceback.parent != None:
            next_node = traceback
            traceback = traceback.parent

        solution = traceback.actions[traceback.children.index(next_node)]
        search_tree = [node.toDict() for node in node_list]

        return solution, search_tree
