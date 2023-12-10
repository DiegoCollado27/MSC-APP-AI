# Aquí está el script completo de Python que utilizamos para descifrar el mensaje:

from itertools import zip_longest

# Función para crear la matriz Playfair a partir de una clave dada
def crear_matriz_playfair(clave):
    # La letra 'J' se omite en el cifrado Playfair
    clave = clave.upper().replace("J", "I")
    # Crear un alfabeto sin la letra 'J'
    alfabeto = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    # Eliminar letras duplicadas en la clave
    clave_sin_duplicados = "".join(dict.fromkeys(clave))
    # Combinar la clave sin duplicados con el alfabeto y eliminar duplicados nuevamente
    clave_alfabeto = clave_sin_duplicados + ''.join([c for c in alfabeto if c not in clave_sin_duplicados])
    # Crear la matriz Playfair en una lista de listas (5x5)
    matriz = list(zip_longest(*[iter(clave_alfabeto)]*5, fillvalue=""))
    return matriz

# Función para descifrar usando la matriz Playfair
def descifrar_playfair(mensaje_cifrado, matriz):
    # Separar el mensaje cifrado en digrafos
    digrafos = [mensaje_cifrado[i:i+2] for i in range(0, len(mensaje_cifrado), 2)]
    texto_descifrado = ""
    # Localizar cada digrafo en la matriz
    for digrafo in digrafos:
        posiciones = []
        for letra in digrafo:
            for fila in matriz:
                if letra in fila:
                    posiciones.append((matriz.index(fila), fila.index(letra)))
        # Descifrar de acuerdo a las reglas del cifrado Playfair
        fila1, col1 = posiciones[0]
        fila2, col2 = posiciones[1]
        # Si los digrafos están en la misma fila, se mueven a la izquierda
        if fila1 == fila2:
            col1_new = (col1 - 1) % 5
            col2_new = (col2 - 1) % 5
            texto_descifrado += matriz[fila1][col1_new] + matriz[fila2][col2_new]
        # Si los digrafos están en la misma columna, se mueven hacia arriba
        elif col1 == col2:
            fila1_new = (fila1 - 1) % 5
            fila2_new = (fila2 - 1) % 5
            texto_descifrado += matriz[fila1_new][col1] + matriz[fila2_new][col2]
        # Si los digrafos forman un rectángulo, se intercambian las columnas
        else:
            texto_descifrado += matriz[fila1][col2] + matriz[fila2][col1]
    return texto_descifrado

# Clave y mensaje cifrado proporcionados para el descifrado
clave_greenlakeia = "GREENLAKEAI"
mensaje_cifrado = "DSLIHPSNIOIOCGGNLRIXPBNQGH"

# Crear la matriz Playfair con la clave "GREENLAKEIA"
matriz_playfair_greenlakeia = crear_matriz_playfair(clave_greenlakeia)

# Descifrar el mensaje con la matriz Playfair y la clave "GREENLAKEIA"
mensaje_descifrado = descifrar_playfair(mensaje_cifrado, matriz_playfair_greenlakeia)

print(f"El mensaje descifrado es: {mensaje_descifrado}")
