import random

def move(vertex):
    # Diccionario de vértices y sus conexiones correspondientes
    graph = {
        1: [2, 3, 5],
        2: [1, 3, 4],
        3: [1, 2, 7],
        4: [2, 5, 8],  # Estado de "muerte"
        5: [1, 4, 6],
        6: [5, 7, 8],
        7: [3, 6, 8],
        8: [4, 6, 7],  # Estado de "muerte"
    }
    return random.choice(graph[vertex])

def simulate(ant_position, steps):
    deaths = {4: 0, 8: 0}
    
    for _ in range(steps):
        while ant_position not in deaths:
            ant_position = move(ant_position)
        
        # Registrar la muerte y reiniciar la posición de la hormiga
        deaths[ant_position] += 1
        ant_position = 1  # La hormiga siempre comienza en la posición 1

    return deaths

# Parámetros de la simulación
number_of_simulations = 100000
starting_vertex = 1

# Realizar las simulaciones
results = simulate(starting_vertex, number_of_simulations)

# Imprimir los resultados
print(f"Probabilidad de muerte en la arista 4: {results[4] / number_of_simulations}")
print(f"Probabilidad de muerte en la arista 8: {results[8] / number_of_simulations}")
