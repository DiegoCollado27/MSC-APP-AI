import numpy as np
import math
import random 
import matplotlib.pyplot as plt
import argparse
import sys

def generar_poblacion_suboptima(tamanio_poblacion, longitud_cromosoma):
    return [''.join(random.choice('01') for _ in range(int(longitud_cromosoma))) for _ in range(tamanio_poblacion)]

def sacar_longitud(c,m ):
    longitud = 0
    while c > 1 :
        if (c>=m):
            longitud += bits_ciudad
        else:
            longitud += bits_ciudad-1
        c -= 1
    return longitud
    
def ciudades_cercanas(ciudad):
    global tabla_costes_aux
    fila = tabla_costes_aux[ciudad]
    fila[ciudad] = 100000000
    
    minima_distancia = min(fila) 
    ciudad_cercana = np.argmin(fila)
    tabla_costes_aux[ciudad][ciudad_cercana] = 1000000000
    return int(ciudad_cercana)

def crear_tabla_distancias(ciudades):
    i = 0
    tabla = np.zeros((len(ciudades),len(ciudades)-1))
    for ciudad in ciudades:
        for j in range (0,len(ciudades)-1):
            ciudad_cercana = ciudades_cercanas(ciudad)
            tabla[i][j] = int(ciudad_cercana)
            j += 1
        i += 1
    return tabla

def decod_suboptima(num_ciudades,cromosoma,m,tabla_distancias,ciudades):
    c = num_ciudades-1
    recorrido = []
    posiciones = sacar_posiciones(num_ciudades,cromosoma,m)
    primera_ciudad = ciudades[0]
    #primera_ciudad =  ciudades[random.randint(0, num_ciudades-1)]
    recorrido.append(primera_ciudad)    
    fila = int(primera_ciudad)
    for i in range (0,len(posiciones)):
        columna = int(posiciones[i])
        siguiente_ciudad = int(tabla_distancias[fila][columna])
        while siguiente_ciudad in recorrido:
            columna += 1
            siguiente_ciudad = int(tabla_distancias[fila][columna])
        fila = int(siguiente_ciudad)           
        recorrido.append(siguiente_ciudad)
    #añadir la que falta
    for ciudad in ciudades:
        if not ciudad in recorrido:
            recorrido.append(ciudad)
    return recorrido

def sacar_posiciones(num_ciudades,cromosoma,m):
    posiciones = []
    bits_ciudad = int(np.log2(m))
    contador_ciudades = num_ciudades
    i = 0
    while contador_ciudades > m :
        bits = ""
        for j in range (i,i+(bits_ciudad)):
            bits += ((cromosoma[j]))  
            i += 1
        posiciones.append(int(bits,2))        
        contador_ciudades -= 1
    while contador_ciudades > 2:
        posiciones.append(int(cromosoma[i],2))
        i += 1
        contador_ciudades -= 1
    return posiciones


def calcular_distancia_total(individuo):
    # Aquí implementa el cálculo de la distancia total basado en el vector S
        ciudad_actual = individuo[0]  # Obtén la primera ciudad
        distancia_total = 0
    
        for i in range(1, len(tabla_costes)):
            siguiente_ciudad = individuo[i]

            distancia_total += tabla_costes[ciudad_actual][siguiente_ciudad]
            ciudad_actual = siguiente_ciudad

        # Regresa a la ciudad de inicio
        distancia_total += tabla_costes[ciudad_actual][individuo[0]]

        return distancia_total
    
    
def seleccionar_individuo_ruleta(poblacion, aptitudes):
    total_aptitud = sum(aptitudes)
    probabilidad = [aptitud / total_aptitud for aptitud in aptitudes]
    return random.choices(poblacion, probabilidad)[0]

def seleccionar_individuo_torneo(poblacion, aptitudes):
    k=20
    population_size = len(poblacion)
    tournament = random.sample(range(population_size), k)  # Selecciona 'k' individuos al azar para el torneo
    winner = min(tournament, key=lambda i: aptitudes[i])  # Elige al individuo con la menor aptitud en el torneo
    winner = poblacion[winner]
    return winner

def mutar_individuo(individuo, num_generaciones):
    probabilidad_mutacion = 0.6
    if num_generaciones > 1000:
        probabilidad_mutacion = probabilidad_mutacion/2
    if num_generaciones > 2000:
        probabilidad_mutacion = probabilidad_mutacion/4
    if num_generaciones > 4000:
        probabilidad_mutacion = probabilidad_mutacion/8
    if num_generaciones > 8000:
        probabilidad_mutacion = probabilidad_mutacion/10    
    if num_generaciones > 15000:
        probabilidad_mutacion = probabilidad_mutacion/20
                   
    mutado = list(individuo)
    for i in range(len(individuo)):
        if random.random() < probabilidad_mutacion:
            # Cambia el bit si la probabilidad de mutación se cumple
            mutado[i] = '0' if individuo[i] == '1' else '1'
    return ''.join(mutado)

def find_best_individual(population, fitness_values):
    # Encontrar y registrar al mejor individuo en la población.
    best_index = fitness_values.index(min(fitness_values))
    best_individual = population[best_index]

    return best_individual

def replace_worst_with_best(population, fitness_values, best_individual):
    # Encontrar el peor individuo y sustituirlo por el mejor individuo si es superior.
    worst_index = fitness_values.index(min(fitness_values))
    if evaluar_aptitud(best_individual) > fitness_values[worst_index]:
        population[worst_index] = best_individual

def cruzamiento_un_punto(padre1, padre2, longitud_cromosoma):
    medio = int(longitud_cromosoma/2)
    punto_cruzamiento = random.randint(medio-10, medio+10)  # Se elige un punto de cruzamiento aleatorio (excepto el primer y último bit)
   
    hijo1 = padre1[:punto_cruzamiento] + padre2[punto_cruzamiento:]
    hijo2 = padre2[:punto_cruzamiento] + padre1[punto_cruzamiento:]

    return hijo1, hijo2



parser = argparse.ArgumentParser()
parser.add_argument('file', help='Path to the data file.')
args = parser.parse_args()

# Read the argument and load the data.
try:
    tabla_costes = np.load(args.file)
    
except:
    print("Error: the input file does not have a valid format.", file=sys.stderr)
    exit(1)


tabla_costes_aux = tabla_costes.copy()

num_ciudades = len(tabla_costes)
tamanio_poblacion = 100
c = num_ciudades-1
ciudades = list(range(0,num_ciudades))
m = 4
bits_ciudad = np.log2(m)
aptitudgraph = []
longitud_cromosoma = sacar_longitud(c,m)
tabla_distancias = crear_tabla_distancias(ciudades)
poblacion = generar_poblacion_suboptima(tamanio_poblacion,longitud_cromosoma)
indx = 0
num_generaciones = 0

try:
    while indx < 1:
        # Evaluación de aptitud
        aptitudes = [calcular_distancia_total(decod_suboptima(num_ciudades,cromosoma,m,tabla_distancias,ciudades)) for cromosoma in poblacion]
        mejor_individuo = find_best_individual(poblacion, aptitudes)
        # Selección
        nueva_poblacion = []
        

        for _ in range(tamanio_poblacion // 2):
            padre1 = seleccionar_individuo_torneo(poblacion, aptitudes)
            padre2 = seleccionar_individuo_torneo(poblacion, aptitudes)

            hijo1, hijo2 = cruzamiento_un_punto(padre1, padre2,longitud_cromosoma)
            nueva_poblacion.extend([hijo1, hijo2])

        #for _ in range(tamano_poblacion // 2):
            #selected_parents = tournament_selection(poblacion, aptitudes)
            #hijo1, hijo2 = cruzamiento_un_punto(selected_parents[0], selected_parents[1])
            #nueva_poblacion.extend([hijo1, hijo2])
        # Mutación
        nueva_poblacion = [mutar_individuo(individuo,num_generaciones) for individuo in nueva_poblacion]

        # Reemplazar la población anterior con la nueva población
        poblacion = nueva_poblacion
        
        poblacion[aptitudes.index(max(aptitudes))] = mejor_individuo
        #replace_worst_with_best(poblacion, aptitudes, mejor_individuo)

        # Mostrar la aptitud del mejor individuo en esta generación
        aptitudes = [calcular_distancia_total(decod_suboptima(num_ciudades,cromosoma,m,tabla_distancias,ciudades)) for cromosoma in poblacion]
        
        mejor_individuo_generacion = poblacion[aptitudes.index(min(aptitudes))]
        mejor_aptitud_generacion = min(aptitudes)


except KeyboardInterrupt:
     
    mejor_individuo_generacion = poblacion[aptitudes.index(min(aptitudes))]
    mejor_aptitud_generacion = min(aptitudes)
    recorrido = decod_suboptima(num_ciudades,mejor_individuo_generacion,m,tabla_distancias,ciudades)
    print(recorrido)