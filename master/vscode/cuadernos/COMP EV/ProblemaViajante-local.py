import numpy as np
import math
import random 
import matplotlib.pyplot as plt


def sacar_posiciones(num_ciudades,cromosoma):
    posiciones = []
    elegir_ciudades = num_ciudades-1
    num_bits = (math.ceil(np.log2(elegir_ciudades)))
    i = 0    
    while elegir_ciudades > 1:
        bits = ''
        if(int(math.ceil(np.log2(elegir_ciudades))) < num_bits):
            num_bits -= 1
        for i in range (i,i+num_bits):
            bits += (cromosoma[i])
            i+=1
        posiciones.append(int(bits,2))        
        elegir_ciudades -= 1
    return posiciones

def decod_bin_local(num_ciudades,cromosoma,ciudades):
    ciudades_elegir = ciudades.copy()
    recorrido = [ciudades_elegir[0]]
    ciudades_elegir.remove(ciudades_elegir[0])
    posiciones = sacar_posiciones(num_ciudades,cromosoma)
    for pos in posiciones:
        if pos > len(ciudades_elegir)-1:
            pos -= len(ciudades_elegir)        
        siguiente_ciudad = ciudades_elegir[pos]
        ciudades_elegir.remove(siguiente_ciudad)
        recorrido.append(siguiente_ciudad)
    for ciudad in ciudades:
        if not ciudad in recorrido:
            recorrido.append(ciudad)
    return recorrido

def calcular_distancia_total(recorrido_ciudades):
    ciudad_actual = recorrido_ciudades[0]  # Obtén la primera ciudad 
    distancia_total = 0
    for i in range(1, len(recorrido_ciudades)):
        siguiente_ciudad = recorrido_ciudades[i]
        distancia_total += tabla_costes[ciudad_actual][siguiente_ciudad]
        ciudad_actual = siguiente_ciudad
    # Regresa a la ciudad de inicio
    distancia_total += tabla_costes[ciudad_actual][recorrido_ciudades[0]]
    return (distancia_total)


def generar_poblacion(tamanio_poblacion, longitud_cromosoma):
    return [''.join(random.choice('01') for _ in range(int(longitud_cromosoma))) for _ in range(tamanio_poblacion)]

def calcular_long_cromosoma(num_ciudades):
    longitud = 0
    num_bits = (math.ceil(np.log2(num_ciudades)))
    num_ciudades -= 1
    while num_ciudades > 1:
        if(int(math.ceil(np.log2(num_ciudades))) < num_bits):
            num_bits -= 1
        longitud += num_bits
        num_ciudades -=1
    return longitud


def seleccion_por_ruleta(poblacion,distancias_poblacion):
    conjunto = []
    for i in range(0,len(poblacion)-1):
        conjunto.append([poblacion[i],distancias_poblacion[i]])
    suma_distancias = sum(distancia for _, distancia in conjunto)
    # Generar una lista de rangos proporcionales a las aptitudes
    rangos = [distancia / suma_distancias for _, distancia in conjunto]  
    seleccionado = None
    r = random.uniform(0, 1)
    acumulado = 0
    for i, rango in enumerate(rangos):
        acumulado += rango
        if acumulado >= r:
            seleccionado = poblacion[i]
            break
    return seleccionado

def mutacion(individuo):
    mutado = list(individuo)
    for i in range(len(individuo)):
        if random.random() < prob_mutacion:
            # Cambia el bit si la probabilidad de mutación se cumple
            mutado[i] = '0' if individuo[i] == '1' else '1'
    mutado = ''.join(mutado)
    return (mutado)

def cruzar_un_punto(padre1,padre2):
    punto_cruce = random.randint(0, len(padre1)-1)
    hijo1 = padre1[0:punto_cruce] + padre2[punto_cruce:len(padre1)]
    hijo2 = padre2[0:punto_cruce] + padre1[punto_cruce:len(padre1)]
    return hijo1,hijo2

def cruzar_dos_puntos(padre1,padre2):
    punto_cruce = random.randint(0, len(padre1)//2)
    punto_cruce2 = random.randint(len(padre1)//2, 40)
    hijo1 = padre1[0:punto_cruce] + padre2[punto_cruce:punto_cruce2] + padre1[punto_cruce2:len(padre1)]
    hijo2 = padre2[0:punto_cruce] + padre1[punto_cruce:punto_cruce2] + padre2[punto_cruce2:len(padre1)]
    return hijo1,hijo2


def seleccionar_mejor(poblacion,distancias_poblacion):
    mejor_individuo = poblacion[distancias_poblacion.index(min(distancias_poblacion))]
    poblacion.remove(mejor_individuo)
    mejor_distancia = min(distancias_poblacion)
    distancias_poblacion.remove(min(distancias_poblacion))
    return mejor_individuo,mejor_distancia


tabla_costes = np.load('ulises.npy') 
tamanio_poblacion = 40
num_ciudades = len(tabla_costes)
longitud_cromosoma = calcular_long_cromosoma(num_ciudades)
ciudades = list(range(0,num_ciudades))
parar = False
num_generaciones = 0
max_gen_sin_evol = 500
prob_mutacion = 0.27
prob_cruce = 0.6
minimo = 100000
gen_sin_evol = 0
mejores_soluciones = []
mejores_individuos = []
datos = []

#crear poblacion inicial
poblacion = generar_poblacion(tamanio_poblacion,longitud_cromosoma)

while not parar:
    # Evaluación de fitness
    distancias_poblacion = []
    for cromosoma in poblacion:
        recorrido = decod_bin_local(num_ciudades,cromosoma,ciudades)
        distancia = calcular_distancia_total(recorrido)
        distancias_poblacion.append(distancia)
        datos.append((cromosoma,distancia))

    # Selección
    progenitores_nueva_poblacion = []
    while(len(progenitores_nueva_poblacion)<tamanio_poblacion):        
        nuevo_progenitor = (seleccion_por_ruleta(poblacion,distancias_poblacion))
        progenitores_nueva_poblacion.append(nuevo_progenitor)
    #cruce
    nueva_poblacion = []
    for i in range(tamanio_poblacion // 2 ):
        progenitor1 = progenitores_nueva_poblacion[i]
        progenitor2 = progenitores_nueva_poblacion[i + tamanio_poblacion // 2]     
        if random.random() > prob_cruce:
            hijo1, hijo2 = cruzar_un_punto(progenitor1, progenitor2)
        else:
            hijo1 = progenitor1
            hijo2 = progenitor2
        
        nueva_poblacion.extend([hijo1, hijo2])
    
    # Mutación
    nueva_poblacion = [mutacion(individuo) for individuo in nueva_poblacion]
    #me quedo con los cuatro mejores individuos de la poblacion anterior   
    poblacion_aux = poblacion.copy()
    dist_aux = distancias_poblacion.copy()
    mejor,dist1 = seleccionar_mejor(poblacion_aux,dist_aux)
    segundo,dist2 = seleccionar_mejor(poblacion_aux,dist_aux)
    tercero,dist3 = seleccionar_mejor(poblacion_aux,dist_aux)
    cuarto,dist4 = seleccionar_mejor(poblacion_aux,dist_aux)
    
    # Reemplazar la población anterior con la nueva población y me quedo con los cuatro de la anterior
    
    poblacion = nueva_poblacion   
    poblacion[0] = mejor    
    poblacion[1] = segundo
    poblacion[2] = tercero
    poblacion[3] = cuarto
   
    recorrido = decod_bin_local(num_ciudades,mejor,ciudades)
    # Mostrar la aptitud del mejor individuo en esta generación
    #print(f"Generación {num_generaciones}, Mejor individuo: {mejor}, Aptitud: {dist1}, Recorrido: {(recorrido)}")

    #si no mejora en x generaciones, gen_sin_evol iteraciones
    if(dist1 >=  minimo):
        gen_sin_evol += 1
    else:
        minimo = dist1
        gen_sin_evol = 0
    if(gen_sin_evol > max_gen_sin_evol):
        parar = True
    num_generaciones += 1
    if(num_generaciones%1000 == 0):
        if (prob_mutacion<0.0001):
            pass
        else:
            prob_mutacion = prob_mutacion/2
    mejores_soluciones.append(dist1)
    mejores_individuos.append(mejor)

mejor_aptitud_total = min(mejores_soluciones)
mejor_individuo_total = mejores_individuos[mejores_soluciones.index(mejor_aptitud_total)]
recorrido = (decod_bin_local(num_ciudades,mejor_individuo_total,ciudades))
print(f"mejor solucion: {(mejor_individuo_total)}, Aptitud: {mejor_aptitud_total}, Recorrido: {(recorrido)}")
plt.plot(mejores_soluciones)
plt.show()