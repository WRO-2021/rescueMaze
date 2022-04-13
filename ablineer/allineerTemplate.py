"""
non so bene come dovrebbe essere il codice, per questo faccio questo con un po'
di metodi vuoti, oltre ad alcune costanti come la velocità di rotazione del robot,
le varie unità di misura, la precisione del lidar e la precisione di alcune cose

in più faccio tutto generico, niente destra e sinistra, poi va implementato tutto
"""

import time
from math import *

PASSI_LIDAR = 360.0
# numero di punti esaminati dal

CELLA = 30.0  # cm

VELOCITA_ROTAZIONE = 90.0  # grad/s


def get_lidar():
    return {}


def start_move(move_forward):
    if move_forward:
        # move forward
        pass
    else:
        # move backward
        pass


def keep_moving(move_forward):
    if move_forward:
        # move forward
        pass
    else:
        # move backward
        pass


def stop_move():
    pass


def start_turn():
    pass


def keep_turning():
    pass


def stop_turn():
    pass


def mean(numbers):
    sum = 0
    for i in numbers:
        sum += i
    return sum / len(numbers)


def variancy(numbers):
    sum = 0
    for i in numbers:
        sum += i * i
    return sum / len(numbers) - mean(numbers) ** 2


def standard_deviation(numbers):
    return sqrt(variancy(numbers))


def median(numbers):
    numbers.sort()
    return numbers[len(numbers) // 2]


# prendo la distanza in una data direzione, faccio un po' di confronti con quelli vicini e calcolo un valore accettabile
def get_int_grad(grad, dist):
    pos = int(grad / 360 * PASSI_LIDAR)
    distances = [dist[pos - 1], dist[pos], dist[(pos + 1) % PASSI_LIDAR]]
    st_dev = standard_deviation(dist)
    media = mean(distances)
    if st_dev > 5:
        maxima = max(distances)
        minima = min(distances)
        mediana = median(distances)
        diff_max = abs(media - maxima)
        diff_min = abs(media - minima)
        diff_med = abs(media - mediana)
        if diff_max > diff_min:
            if diff_max > diff_med:
                return mean([minima, mediana])
            else:
                return mean([minima, maxima])
        else:
            if diff_min > diff_med:
                return mean([mediana, maxima])
            else:
                return mean([maxima, minima])
    return media


# invece di gradi usa 90 gradi a botta
def get_int_quarter(quart, dist):
    return get_int_grad(quart * 90, dist)


# controllo il numero di celle in mezzo tra il robo e il muro in ogni direzione
def get_walls():
    distances = get_lidar()
    walls = []
    for i in range(4):
        dist = get_int_quarter(i, distances)
        walls.append(dist / CELLA)
    return walls


# controllo la distanza dal bordo della cella in ogni direzione
def get_dist_mod(distances, forward):
    if forward:
        return get_int_quarter(0, distances) % CELLA
    else:
        return get_int_quarter(2, distances) % CELLA


# centra il robot davanti e dietro
def center_robot():
    distances = get_lidar()
    is_greater_forward = get_dist_mod(distances, True) > get_dist_mod(distances, False)

    def continue_cycle():
        forw = get_dist_mod(distances, True)
        back = get_dist_mod(distances, False)
        return not forw > back ^ is_greater_forward # nxor, quando non varia il valore continua il ciclo

    start_move(is_greater_forward)
    while continue_cycle():
        keep_moving(is_greater_forward)

    stop_move()


# centimetri di cui cambia la distanza girando nell'angolo della cella a n_celle di distanza
def get_precision_cm(n_celles):
    dis = CELLA / 2 + n_celles * CELLA
    max_deg = atan(CELLA / 2 / dis)
    return dis * sin(max_deg) - dis / sin(max_deg - 2 * pi / PASSI_LIDAR)


# gradianti di ampiezza dell'angolo tra il centro di una cella e l'angolo della cella a n_celle di distanza(radice di
# 2 senza celle di distanza)
def get_grad_dista_cell(n_cell):
    dis = CELLA / 2 + n_cell * CELLA
    return atan(CELLA / 2 / dis)


# controllo che la distanza tra gli angoli di una cella a direzione data e distanza di celle data non sia uguale,
# con la giusta precisione
def check_turning(n_cell, precision, direction):
    distances = get_lidar()
    angulus = get_grad_dista_cell(n_cell) / 2 * pi * 360 # angolo in gradi
    angulus *= 0.9 # diminuisco un po' per prendere i muri di sicuro nella misura
    # conronto i valori delle distanze nelle direzioni simmetriche, con scarto appena calcolato
    difference = get_int_grad(90 * direction + angulus, distances) - get_int_grad(90 * direction - angulus, distances)
    return abs(difference) < precision


# gira a destra(?) allineandosi con il lidar
def turn():
    distances = get_lidar()
    walls = get_walls()
    wall_distances_in_cell = 0
    wall_dir = 0
    # trovo il muro più vicino, la sua distanza in numero di celle e la sua direzione
    while True:
        if walls[wall_dir] == wall_distances_in_cell:
            break
        wall_dir += 1
        if wall_dir == 4:
            wall_dir = 0
            wall_distances_in_cell += 1
    precision = get_precision_cm(wall_distances_in_cell)
    time_to_80 = 80 / VELOCITA_ROTAZIONE
    start_turn_time = time.time()
    start_turn()
    while time.time() - start_turn_time < time_to_80:
        keep_turning()

    # inizio a prendere le distanze per fermarmi al momento giusto
    while check_turning(wall_distances_in_cell, precision, (wall_dir + 1) % 4):  # controllo con il muro a destra di 90
        # gradi, come se girasse da quella
        keep_turning()
    stop_turn()
