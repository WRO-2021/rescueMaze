import queue


class Coor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isAdiacent(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) == 1

    def getDirection(self, other):
        if self.x == other.x:
            if self.y > other.y:
                return 0
            else:
                return 2
        else:
            if self.x > other.x:
                return 3
            else:
                return 1

    @staticmethod
    def ix(direction):
        if direction == 1:
            return 1
        elif direction == 3:
            return -1
        else:
            return 0

    # funziona ammettendo che le celle siano adiacenti
    @staticmethod
    def iy(direction):
        if direction == 0:
            return 1
        elif direction == 2:
            return -1
        else:
            return 0

    def move(self, direction):
        return Coor(self.x + Coor.ix(direction), self.y + Coor.iy(direction))

    @staticmethod
    def opposite(direction):
        return (direction + 2) % 4


class MapNode:
    alls = []

    def __init__(self, coor):
        self.coor = coor
        self.neighbors = [None, None, None, None]
        self.isVisited = False
        self.isDanger = False
        self.isCheckpoint = False
        self.bfs = False
        self.walls = ['u', 'u', 'u', 'u']
        MapNode.alls.append(self)

    def getNeighbor(self, direction):
        return self.neighbors[direction]

    def addWall(self, direction, wall):
        if self.walls[direction] == 'u':
            self.walls[direction] = wall
            if self.neighbors[direction] is None:
                MapNode.insertNode(MapNode(self.coor.move(direction)))

    def addNeighbor(self, direction, node):
        if self.neighbors[direction] is None:
            self.neighbors[direction] = node
            node.addNeighbor(Coor.opposite(direction), self)
            node.addWall(Coor.opposite(direction), self.walls[direction])

    @staticmethod
    def insertNode(nuovo):
        for node in MapNode.alls:
            if node.coor.isAdiacent(nuovo.coor):
                node.addNeighbor(nuovo.coor.getDirection(node.coor), nuovo)

    def track_to(self, condition):
        # ricerca di una cella che alla condizione dia true
        # bfs
        self.bfs = True
        current_track = queue.Queue()
        current_track.put(self.coor)
        current_node = self

        nodes_queue = queue.Queue()
        nodes_queue.put(current_node)

        tracks_queue = queue.Queue()
        tracks_queue.put(current_track)

        while not nodes_queue.empty() and not condition(current_node):
            current_node = nodes_queue.get()
            current_track = tracks_queue.get()

            for i in range(4):
                tmp = current_node.getNeighbor(i)
                if tmp is not None and not tmp.bfs and not tmp.isDanger and tmp.walls[i] != 'u':
                    tmp.bfs = True
                    nodes_queue.put(tmp)

                    tmp_track = queue.Queue(current_track)
                    tmp_track.put(tmp.coor)
                    tracks_queue.put(tmp_track)

        if not condition(current_node):
            return None # se la bfs si è conclusa senza trovare la condizione in nessuna cella
        else:
            return current_track

    def get_track_to_unknown(self):

        track = self.track_to(lambda x: not x.visited)
        # cerco una cella non visitata

        if track is None:
            return self.track_to(lambda x: x.coor.x == 0 and x.coor.y == 0)
            # cerco una cella con coordinate (0,0)
            # return track to start cell if no unexplored cell is found
        else:
            out = []
            while not track.qsize() == 1:
                tmp_coor = track.get()
                out.append(tmp_coor.getDirection(track[0]))
            return out

    def to_string(self, direction=None):
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for node in MapNode.alls:
            coor = node.coor
            if coor.x < min_x:
                min_x = coor.x
            if coor.y < min_y:
                min_y = coor.y
            if coor.x > max_x:
                max_x = coor.x
            if coor.y > max_y:
                max_y = coor.y

        x_len = (max_x - min_x + 1) * 2 + 1
        y_len = (max_y - min_y + 1) * 2 + 1
        griglia = [' ' * x_len] * y_len

        delta_x = min_x * -2
        delta_y = min_y * -2

        for node in MapNode.alls:
            c = node.coor
            x = c.x * 2 + 1 + delta_x
            y = c.y * 2 + 1 + delta_y
            if c.x == self.coor.x and c.y == self.coor.y:
                if direction is None:
                    tmp_char = '@'
                else:
                    if direction == 0:
                        tmp_char = '^'
                    elif direction == 1:
                        tmp_char = '>'
                    elif direction == 2:
                        tmp_char = 'v'
                    elif direction == 3:
                        tmp_char = '<'
                    else:
                        tmp_char = '?'
            elif c.x == 0 and c.y == 0:
                tmp_char = 'S'
            elif node.isDanger:
                tmp_char = 'X'
            elif node.isCheckpoint:
                tmp_char = 'C'
            elif node.isVisited:
                tmp_char = u'\u2500'
            else:
                tmp_char = ' '
            griglia[y][x] = tmp_char

            if node.walls[0] != 'u':
                griglia[y + 1][x] = u'\u2550'
            if node.walls[1] != 'u':
                griglia[y][x + 1] = u'\u2551'
            if node.walls[2] != 'u':
                griglia[y - 1][x] = u'\u2550'
            if node.walls[3] != 'u':
                griglia[y][x - 1] = u'\u2551'

            griglia[y+1][x+1] = u'\u256c'
            griglia[y+1][x-1] = u'\u256c'
            griglia[y-1][x+1] = u'\u256c'
            griglia[y-1][x-1] = u'\u256c'

        out = ''
        for i in range(y_len-1, -1, -1):
            for char in griglia[i]:
                out += char
            out += '\n'
        return out


class Explorator:

    def __init__(self):
        self.current = MapNode(Coor(0, 0))
        self.direction = 0
        self.last_checkpoint = self.current
        self.current.isCheckpoint = True

    def get_movements(self):
        raw = self.current.get_track_to_unknown()
        out = []
        tmp_dir = self.direction
        for move in raw:
            tmp_move = (4 + tmp_dir - move) % 4
            if tmp_move != 0:
                out.append(tmp_move)
            out.append(0)
            tmp_dir = raw
        return out

    def __str__(self):
        return 'Direzione attuale: ' + str(self.direction) + '\n' + self.current.to_string(direction=self.direction)

    def forward(self):
        self.current = self.current.getNeighbor(self.direction)
        self.current.isVisited = True

    def turn_left(self):
        self.direction = (self.direction + 3) % 4

    def turn_right(self):
        self.direction = (self.direction + 1) % 4

    def turn_around(self):
        self.direction = (self.direction + 2) % 4

    def move(self, direction):
        if direction == 0:
            self.forward()
        elif direction == 1:
            self.turn_right()
        elif direction == 2:
            self.turn_around()
        elif direction == 3:
            self.turn_left()

    def move_to_last_checkpoint(self):
        self.current = self.last_checkpoint
        self.direction = 0

    def set_checkpoint(self):
        self.last_checkpoint = self.current
        self.current.isCheckpoint = True

    def set_danger(self, direction):
        if direction < 0:
            self.current.isDanger = True
        elif direction > 3:
            self.current.getNeighbor(self.direction).isDanger = True
        else:
            self.current.getNeighbor(direction).isDanger = True

    def set_wall(self, is_wall, direction):
        if direction is not None:
            self.current.addWall(direction, is_wall)
        elif is_wall is list or is_wall is tuple:
            for i in range(4):
                self.current.addWall(i, is_wall[i])


