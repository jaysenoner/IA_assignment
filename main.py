import math
from random import random
import numpy
import numpy as np
import shapely
from shapely.geometry import LineString
import warnings

"""
Istruzioni
Il lavoro sarà oggetto di discussione durante l’esame orale e dovrà essere sottomesso almeno 48 ore prima dell’esame, includendo:
1. Sorgenti e materiale sviluppato in autonomia (senza includere datasets o librerie sviluppate da altri: basta fornire un link);
2. Un file README che spieghi il ruolo di ciascun file sorgente e la sequenza di comandi che permette di riprodurre i risultati sottomessi.
3. Una breve relazione (massimo 4 pagine in formato pdf) che descriva il lavoro e analizzi i risultati sperimentali. Non è necessario
ripetere in dettaglio i contenuti del libro di testo o di eventuali articoli, è invece necessario che vengano fornite informazioni
sufficienti a riprodurre il metodo utilizzato ed i risultati ottenuti. Eventuali porzioni riprese da altre fonti devono essere evidenziate
con le relative citazioni.
La sottomissione va effettuata preferibilmente creando un repository privato su codeberg con Project name “Nome Cognome” e condividendolo con l’utente ai-unifi (da project information->members->invite members). In alternativa, è accettabile inviare
per email a ai.unifi@pm.me un singolo file zip (di dimensioni non superiori ad 1MB); tale file deve contenere solo i sorgenti e la
relazione in pdf (senza altri files binari).



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


def intersect(A, B, C, D):
    pointA = shapely.Point(A[0], A[1])
    pointB = shapely.Point(B[0], B[1])
    pointC = shapely.Point(C[0], C[1])
    pointD = shapely.Point(D[0], D[1])
    S1 = LineString([pointA, pointB])
    S2 = LineString([pointC, pointD])

    intersection = shapely.intersection(S1, S2)

    if intersection.is_empty:
        return False
    if intersection == pointA or intersection == pointB \
            or intersection == pointC or intersection == pointD:
        return False
    return S1.intersects(S2)

"""
Pseudocode of the algorithm that generates random map coloring problems.

generate_random_csp(n) n: the number of variables in the csp problem.
    points = n tuples of rand values in [0,1)
    while points is not EMPTY:
        random_point = random point in points
        do
            nearest_point = nearest point 

"""
#np.delete( array, index)
def generate_random_map_coloring_csp(n):
    created_constraints = []
    created_variables = []
    points = np.random.random((n, 2))




def min_distance(points, idx):
    distances = np.linalg.norm(points - points[idx],
                               axis=1)  # Calcola le distanze euclidee tra tutti i punti
    distances[idx] = np.inf             # Escludi la distanza del punto selezionato stesso

    min_index = np.argmin(distances)    # Ottieni l'indice del punto con la distanza minima

    return min_index





def main():
    A = (0, 0)
    B = (0, 1)
    C = (1, 1)
    D = (3, 1)
    print(intersect(A, B, C, D))





if __name__ == '__main__':
    main()
