import random
import numpy as np
from numpy import math


def crear_tabla_distancias(tabla_costes, ciudades):
    i = 0
    tabla = np.zeros((len(ciudades),len(ciudades)-1))
    for ciudad in ciudades:
        for j in range (0,len(ciudades)-1):
            ciudad_cercana = ciudades_cercanas(ciudad,tabla_costes)
            tabla[i][j] = int(ciudad_cercana)
            j += 1
        i += 1
    return tabla


def ciudades_cercanas(ciudad,tabla_costes):
    fila = tabla_costes[ciudad]
    fila[ciudad] = 100000000
    minima_distancia = min(tabla_costes[ciudad])
    ciudad_cercana = np.where(fila == minima_distancia)
    ciudad_cercana = ciudad_cercana[0]

    if(len(ciudad_cercana)>1):
        ciudad_cercana = ciudad_cercana[0]
        fila[ciudad_cercana] = 10000000
    else:
        fila[ciudad_cercana] = 10000000
    return int(ciudad_cercana)


def generar_poblacion_suboptima(tamanio_poblacion, longitud_cromosoma):
    return [''.join(random.choice('01') for _ in range(int(longitud_cromosoma))) for _ in range(tamanio_poblacion)]

def decod_suboptima(num_ciudades,cromosoma,m,tabla_distancias,ciudades):
    c = num_ciudades-1
    recorrido = []
    posiciones = sacar_posiciones(num_ciudades,cromosoma,m)
    print(posiciones)
    print(tabla_distancias)
    primera_ciudad =  ciudades[random.randint(0, num_ciudades-1)]
    print(primera_ciudad)
    recorrido.append(primera_ciudad)    
    fila = int(primera_ciudad)
    for i in range (0,len(posiciones)):
        columna = int(posiciones[i])
        print(tabla_distancias[fila][columna])
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
    print("tamaño recorrido "+ str(len(recorrido)))
    return recorrido
    


def sacar_posiciones(num_ciudades,cromosoma,m):
    posiciones = []
    bits_ciudad = int(np.log2(m))
    print(bits_ciudad)
    print("tamaño cromosoma "+str(len(cromosoma)))
    contador_ciudades = num_ciudades
    i = 0
    while contador_ciudades > m :
        bits = ""
        for j in range (i,i+(bits_ciudad)):
            bits += ((cromosoma[j]))  
            i += 1
        print("Grupo bits  "+str(bits))
        posiciones.append(int(bits,2))        
        contador_ciudades -= 1
        print("posiciones "+str(i))
        print("contdor "+str(contador_ciudades))
    while contador_ciudades > 2:
        print("Grupo bits  "+str(cromosoma[i]))
        posiciones.append(int(cromosoma[i],2))
        contador_ciudades -= 1
    return posiciones

tabla_costes = np.load('Computación Evolutiva/Práctica/ulises.npy') 
tamanio_poblacion = 80
num_ciudades = len(tabla_costes)
print("numero ciudades : "+ str(num_ciudades))
c = num_ciudades-1
m = 4
bits_ciudad = np.log2(m)
longitud_cromosoma = 0
while c > 1 :
    if (c>=m):
        longitud_cromosoma += bits_ciudad
    else:
        longitud_cromosoma += bits_ciudad-1
    c -= 1
ciudades = list(range(0,num_ciudades))
#crear poblacion
tabla_distancias = crear_tabla_distancias(tabla_costes,ciudades)
poblacion = generar_poblacion_suboptima(tamanio_poblacion,longitud_cromosoma)
cromosoma = poblacion[0]
print(cromosoma)
recorrido_ciudades = decod_suboptima(num_ciudades,cromosoma,m,tabla_distancias,ciudades)
print(recorrido_ciudades)