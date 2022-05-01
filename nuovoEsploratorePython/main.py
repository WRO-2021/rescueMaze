import queue
from typing import List

"""
    @author: Samuele Facenda
    @contact: samuele.facenda@gmail.com
    @contact: samuele.facenda@buonarroti.tn.it
    @github: SamueleFacenda
    
    premessa: tutti i commenti di questo codice sono fatti da me, per scriverli mi baso solo
    sulla mia personale e non tanto lunga esperienza, per cui cercherò di fare in modo da sembrare
    deciso per non dover sottolineare ogni volta che sono andato più o meno ad intuito. Per cui le mie 
    affermazioni possono essere talvolta prive di senso o errate.
    
    
    Questo codice è progettato per essere un'integrazione ad alto livello per un robot che esplora il
    labirinto di una rescue maze, non contiene controlli e se usato all'infuori del suo contesto può, molto
    probabilmente, non funzionare correttamente o crashare. 
    
    Per un corretto funzionamento è necessatio che il robot ogni volta comunichi lo stato dei 4 muri adiacenti
    e i movimenti fatti, una volta compltati(avanti, gira a destra...).
    è inoltre possibile usare i vari flag delle celle, come danger e checkpoint, per avere un percorso sicuro
    e poter usare i luck-of-progress(non so se è scritto giusto) in modo ottimale.
    
    
    Funzionameto:
    Il labirinto viene salvato come una specie di grafo, ad accesso sequenziale. Dico una specie perchè 
    i collegamenti tra le celle non sono casuali e per ogni nodo salvo i 4 nodi vicini nelle 4 direzioni, se ce
    ne sono. Per le direzioni uso la(mia) notazione standard, che risulta molto comoda anche nell'implementazione.
    Il nord(su) è lo 0, l'est(destra) è l'1, l'ovest(sinistra) è il 2, il sud(giù) è il 3.
    Anche i movimenti vengono segnalati così.
    Ogni nodo inoltre ha le informazioni sui muri vicini, e le scambia con i nodi adiacenti.
    Per generare mano a mano i nodi, faccio in modo di generarne uno nuovo ogni volta che aggiungo
    un'informazione su un muro che dietro non ha nessun nodo, poi, essendo che la forma esplorata puù non essere
    regolare(ad esempio circonferenza senza un punto) devo scorrere tutti i nodi per controllare se ce ne sono
    di virtualmente adiacenti a quello appena istanziato, per completare i collegamenti. 
    Per questo ogno nodo ha anche una coordinata, classe Coor, con la quale è facile calcoltare l'adiacenza e 
    la rispettiva direzione di due nodi.
    
    
    
       
"""


class Coor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isAdiacent(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) == 1

    # funziona ammettendo che le celle siano adiacenti, ritorna la direzione della cella other rispetto a self
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

    # numero da sommare a una x per ottenere la x della cella adiacente nella direzione data
    @staticmethod
    def ix(direction):
        if direction == 1:
            return 1
        elif direction == 3:
            return -1
        else:
            return 0

    # idem con le y
    @staticmethod
    def iy(direction):
        if direction == 0:
            return 1
        elif direction == 2:
            return -1
        else:
            return 0

    # ritorna una coordinata spostata di uno in direzione data
    def move(self, direction):
        return Coor(self.x + Coor.ix(direction), self.y + Coor.iy(direction))

    @staticmethod
    def opposite(direction):
        return (direction + 2) % 4


"""
    classe principale per il funzionamento, è completamente incapsulata
"""


class MapNode:
    alls = []

    def __init__(self, coor):
        self.coor = coor
        self.neighbors = [None, None, None, None]
        self.isVisited = False
        self.isDanger = False
        self.isCheckpoint = False
        self.bfs = False  # flag per bfs
        self.walls = ['u', 'u', 'u', 'u']  # i muri sono tutti unknown
        MapNode.alls.append(self)

    def getNeighbor(self, direction):
        return self.neighbors[direction]

    # aggiunge un muro in una direzione, se non esiste già un nodo adiacente, lo crea
    def addWall(self, direction, wall):
        if self.walls[direction] == 'u':
            self.walls[direction] = wall
            if self.neighbors[direction] is None:
                MapNode.insertNode(MapNode(self.coor.move(direction)))
                # così facendo scambia anche le informazioni sul muro
            else:
                self.getNeighbor(direction).addWall(Coor.opposite(direction), wall)

    def addNeighbor(self, direction, node):
        if self.neighbors[direction] is None:
            self.neighbors[direction] = node
            node.addNeighbor(Coor.opposite(direction), self)
            if self.walls[direction] != 'u':
                node.addWall(Coor.opposite(direction), self.walls[direction])

    # aggiunge il nodo nuovo come vicino a tutti i nodi adiacenti
    @staticmethod
    def insertNode(nuovo):
        for node in MapNode.alls:
            if node.coor.isAdiacent(nuovo.coor):
                node.addNeighbor(nuovo.coor.getDirection(node.coor), nuovo)
                # faccio così e non l'opposto così si scambiano le informazioni sul muro in mezzo

    def track_to(self, condition):
        # ricerca di una cella che alla condizione dia true
        # ho bisogno del percorso per la cella, oltre alla queue di nodi ne ho una parallela di
        # coordinate, sono le coordinate adiacenti per arrivare a quel nodo da self(self è compresa nella lista)

        # bfs(breadth first search)
        self.bfs = True  # flag isExplored
        current_track = queue.Queue()  # queue di coordinate
        current_track.put(self.coor)
        current_node = self

        # queue di nodi per la bfs
        nodes_queue = queue.Queue()
        nodes_queue.put(current_node)

        # queue parallela di tracks
        tracks_queue = queue.Queue()
        tracks_queue.put(current_track)

        # continua finchè o non finiscono i nodi o ho raggiunto una cella che soddisfa la condizione
        while not nodes_queue.empty() and not condition(current_node):
            current_node = nodes_queue.get()
            current_track = tracks_queue.get()

            # aggiungo i nodi vicini, non devono essere danger, già passati nella bfe e il muro debe essere free
            for i in range(4):
                tmp = current_node.getNeighbor(i)
                if tmp is not None and not tmp.bfs and not tmp.isDanger and current_node.walls[i] == 'f':
                    tmp.bfs = True
                    nodes_queue.put(tmp)

                    tmp_track = queue.Queue(current_track)
                    tmp_track.put(tmp.coor)
                    tracks_queue.put(tmp_track)

        if not condition(current_node):
            return None  # se la bfs si è conclusa senza trovare la condizione in nessuna cella
        else:
            return current_track

    # calcolo il percorso per la più vicina cella sconosciuta, se non ce ne sono ritorno il percorso per la cella
    # iniziale. Il percorso è ritornato come lista di coordinate assolute(0 nord, 1 est...)
    def get_track_to_unknown(self):

        track = self.track_to(lambda x: not x.visited)
        # cerco una cella non visitata

        # controllo che sia stata trovata una cella non visitata
        if track is None:
            track = self.track_to(lambda x: x.coor.x == 0 and x.coor.y == 0)
            # cerco una cella con coordinate (0,0)
            # return track to start cell if no unexplored cell is found

        # converto le coordinate in direzioni per la coordinata dopo
        out = []
        while not track.qsize() == 1:
            tmp_coor = track.get()
            out.append(tmp_coor.getDirection(track[0]))
        return out

    # stapa il labirinto, non è bello come metodo
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

            griglia[y + 1][x + 1] = u'\u256c'
            griglia[y + 1][x - 1] = u'\u256c'
            griglia[y - 1][x + 1] = u'\u256c'
            griglia[y - 1][x - 1] = u'\u256c'

        out = ''
        for i in range(y_len - 1, -1, -1):  # va scorsa dalle y più grandi fino allo 0
            for char in griglia[i]:
                out += char
            out += '\n'
        return out


# contenitore, contiene anche la direzione del robot, converte le direzioni input in direzioni assolute della mappa
class Explorator:

    def __init__(self):
        self.current = MapNode(Coor(0, 0))
        self.current.isVisited = True
        self.direction = 0
        self.last_checkpoint = self.current

    # calcolo i movimenti da fare per procedere nell'esplorazione, 0 è avanti, 1 è 90° a destra...
    def get_movements(self):
        raw = self.current.get_track_to_unknown()
        out = []
        tmp_dir = self.direction
        for move in raw:
            # calcolo il movimento da fare rispetto alla direzione ottenuta dall'ultimo movimento
            tmp_move = (4 + move - tmp_dir) % 4
            if tmp_move != 0:
                out.append(tmp_move)
            out.append(0)  # aggiungo un movimento in avanti
            tmp_dir = move  # aggiorno l'ultima direzione
        return out

    def __str__(self):
        return 'Direzione attuale: ' + str(self.direction) + '\n' + self.current.to_string(direction=self.direction)

    # direzione nel labirinto da direzione relativa(direzione per il robot)
    def dir_abs(self, dire):
        return (self.direction + dire) % 4

    # sposto nel labirinto il robot avanti di una cella, anche i metodi dopo sono simili a questo
    def forward(self):
        self.current = self.current.getNeighbor(self.direction)
        self.current.isVisited = True
        if self.current.isCheckpoint:
            self.last_checkpoint = self.current

    def turn_left(self):
        self.direction = (self.direction + 3) % 4

    def turn_right(self):
        self.direction = (self.direction + 1) % 4

    def turn_around(self):
        self.direction = (self.direction + 2) % 4

    # decodifica il comando di movimento
    def move(self, direction):
        if direction == 0:
            self.forward()
        elif direction == 1:
            self.turn_right()
        elif direction == 2:
            self.turn_around()
        elif direction == 3:
            self.turn_left()

    # luck-of-progress, mi muovo all'ultimo checkpoint e aggiorno la direzione a quella attuale
    def move_to_last_checkpoint(self):
        self.current = self.last_checkpoint
        self.direction = 0

    # la cella corrante è un checkpoint
    def set_checkpoint(self):
        self.last_checkpoint = self.current
        self.current.isCheckpoint = True

    # setto il danger, se la direzione è minore di 0 allora lo setto nella cella corrente, se è maggiore di 3
    # lo setto davanti, se no nella direzione indicata
    def set_danger(self, direction):
        if direction < 0:
            self.current.isDanger = True
        elif direction > 3:
            self.current.getNeighbor(self.direction).isDanger = True
        else:
            self.current.getNeighbor(self.dir_abs(direction)).isDanger = True

    # setto i muri, se indico una direzione allora lo setto in quella direzione in base al bool is_wall,
    # altrimenti controllo che is_wall sia una lista e setto tutti i nodi nelle direzioni
    def set_wall(self, is_wall, direction):
        if direction is not None:
            self.current.addWall(self.dir_abs(direction), 'w' if is_wall else 'f')
        elif is_wall is list or is_wall is tuple:
            for i in range(4):
                self.current.addWall(self.dir_abs(i), 'w' if is_wall[i] else 'f')
