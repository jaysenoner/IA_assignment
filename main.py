import numpy as np
import shapely
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from shapely.geometry import Point

"""Istruzioni:
Il lavoro sarà oggetto di discussione durante l’esame orale e dovrà essere sottomesso almeno 48 ore 
prima dell’esame, includendo: 1. Sorgenti e materiale sviluppato in autonomia (senza includere datasets o librerie 
sviluppate da altri: basta fornire un link); 2. Un file README che spieghi il ruolo di ciascun file sorgente e la 
sequenza di comandi che permette di riprodurre i risultati sottomessi. 3. Una breve relazione (massimo 4 pagine in 
formato pdf) che descriva il lavoro e analizzi i risultati sperimentali. Non è necessario ripetere in dettaglio i 
contenuti del libro di testo o di eventuali articoli, è invece necessario che vengano fornite informazioni 
sufficienti a riprodurre il metodo utilizzato ed i risultati ottenuti. Eventuali porzioni riprese da altre fonti 
devono essere evidenziate con le relative citazioni. La sottomissione va effettuata preferibilmente creando un 
repository privato su codeberg con Project name “Nome Cognome” e condividendolo con l’utente ai-unifi (da project 
information->members->invite members). In alternativa, è accettabile inviare per email a ai.unifi@pm.me un singolo 
file zip (di dimensioni non superiori ad 1MB); tale file deve contenere solo i sorgenti e la relazione in pdf (senza 
altri files binari).



Ricerca locale per problemi di sodisfacimento di vincoli
In questo esercizio si implementano (in un linguaggio di programmazione a scelta) le strategie di ricerca locale min-conflicts
e constraint weighting descritte in in R&N 2021 6.4. Si comparano quindi le due strategie sul problema della colorazione
di mappe, (si possono generare problemi casuali con la strategia suggerita nell’esercizio 6.10 in R&N 2021), studiando
empiricamente il tempo di esecuzione in funzione del numero di variabili n del problema, facendo crescere n quanto più
possibile (nei limiti ragionevoli imposti dall’hardware disponibile).
"""

# Algoritmi e tecniche da utilizzare:


# Generazione di problemi di colorazione di mappe casuali:

"""
Generate random instances of map-coloring problems as follows: scatter 
n points on the unit square; select a point X at random, connect X by a straight line to the nearest point Y such that 
X is not already connected to Y and the line crosses no other line; 
repeat the previous step until no more connections are possible. 
The points represent regions on the map and the lines connect neighbors. 
"""

# Algoritmo min_conflicts

"""
function MIN-CONFLICTS(csp, max_steps) returns a solution of failure
inputs: csp, a constraint satisfaction problem
        max_steps, the number of steps allowed before giving up

    current ← an initial complete assignment for csp
    for i = 1 to max_steps do
            if current is a solution for csp then return current
            var ← a randomly chosen conflicted variable from csp.VARIABLES
            value ← the value v for var that minimizes CONFLICTS(var, v, current, csp)
            set var = value in current
    return failure

The MIN-CONFLICTS algorithm for solving CSPs by local search. 
The initial state may be chosen randomly or by a greedy assignment process that chooses a minimal-conflict value 
for each variable in turn. The CONFLICTS function counts the number of constraints violated by a particular value, given the rest of the current assignment.
"""


# s1:Line that already exist in the graph
# s2. Line that we are creating between 2 points of the graph


def line_intersects(existing_line, new_line, points):
    existing_line_first = Point(existing_line.coords[0])
    existing_line_last = Point(existing_line.coords[-1])
    new_line_first = Point(new_line.coords[0])
    new_line_last = Point(new_line.coords[-1])

    intersection = shapely.intersection(existing_line, new_line)
    # Check if the intersection is one of the points of the graph. if that is the case, we check if
    # there is any connection between segments that generated such intersection and we return false
    # if we find out that the 2 segment are connected by one of their endpoints. Otherwise, we return True
    if any(intersection.equals(point) for point in points):
        if existing_line_first.equals(new_line_first) or existing_line_first.equals(new_line_last) \
                or existing_line_last.equals(new_line_first) or existing_line_last.equals(new_line_last):
            return False
        else:
            return True
    # Here we check if the line that we are creating passes through a point in the graph, excluding the points of
    # the new line
    all_points_except_endpoints = [point for point in points if
                                   not (point.equals(new_line_first) or point.equals(new_line_last))]
    if any(new_line.distance(point) < 0.0001 for point in all_points_except_endpoints):
        return True

    return existing_line.intersects(new_line)


"""
Generate random instances of map-coloring problems as follows: scatter 
n points on the unit square; select a point X at random, connect X by a straight line to the nearest point Y such that 
X is not already connected to Y and the line crosses no other line; 
repeat the previous step until no more connections are possible. 
The points represent regions on the map and the lines connect neighbors. 
"""


def generate_random_map_coloring_csp(n):
    created_constraints = []

    points = np.random.random((n, 2))
    shapely_points = [shapely.Point(point[0], point[1]) for point in points]

    i = 0
    calculate_distances = True
    distances = []
    while True:
        if i > len(shapely_points) - 1:
            break
        if calculate_distances:
            distances = [shapely_points[i].distance(other_point) for other_point in shapely_points]
        distances[i] = np.inf
        nearest_point = shapely_points[np.argmin(distances)]
        expected_line = LineString([shapely_points[i], nearest_point])

        if not any(line.equals(expected_line) or line_intersects(line, expected_line, shapely_points) for line in
                   created_constraints):
            created_constraints.append(expected_line)
            i += 1
            calculate_distances = True
        else:
            distances[shapely_points.index(nearest_point)] = np.inf
            calculate_distances = False

        if all(distance == np.inf for distance in distances):
            i += 1
            calculate_distances = True

    return shapely_points, created_constraints


def main():
    n = 50
    created_variables, created_constraints = generate_random_map_coloring_csp(n)
    print(created_variables, created_constraints)

    xs = [point.x for point in created_variables]
    ys = [point.y for point in created_variables]
    for i in range(len(created_constraints)):
        x, y = created_constraints[i].xy
        plt.plot(x, y)
    plt.scatter(xs, ys)
    plt.show()


if __name__ == '__main__':
    main()