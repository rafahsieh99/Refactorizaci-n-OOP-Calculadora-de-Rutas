import heapq  # Importa la biblioteca heapq para trabajar con colas de prioridad

# Define la clase Mapa
class Mapa:
    def __init__(self, filas, columnas):
        # Inicializa el mapa creando una matriz de ceros con las dimensiones dadas
        self.mapa = self.crear_mapa(filas, columnas)

    def crear_mapa(self, filas, columnas):
        # Crea una matriz de ceros con las dimensiones especificadas
        return [[0 for _ in range(columnas)] for _ in range(filas)]

    def mostrar_mapa(self, inicio=None, fin=None, camino=None):
        # Muestra el mapa en la consola
        for i, fila in enumerate(self.mapa):
            for j, celda in enumerate(fila):
                if inicio and (i, j) == inicio:
                    print("E", end="")  # Marca el punto de inicio con "E"
                elif fin and (i, j) == fin:
                    print("S", end="")  # Marca el punto final con "S"
                elif celda == 999:
                    print("X", end="")  # Marca los edificios con "X"
                elif celda == 2:
                    print("#", end="")  # Marca los baches con "#"
                elif celda == 3:
                    print("!", end="")  # Marca el agua con "!"
                elif camino and (i, j) in camino:
                    print("*", end="")  # Marca el camino con "*"
                else:
                    print(".", end="")  # Marca los espacios libres con "."
            print()  # Nueva línea al final de cada fila

    def agregar_obstaculos(self):
        # Permite al usuario agregar obstáculos al mapa
        while True:
            # Solicita el tipo de obstáculo al usuario
            tipo_obstaculo = input("Ingrese el tipo de obstáculo (X para edificio, # para bache, ! para agua) o basta para continuar ")
            tipo_obstaculo = tipo_obstaculo.lower()  # Convertir la entrada a minúsculas
            if tipo_obstaculo == 'basta':
                break  # Termina si el usuario ingresa "basta"
            if tipo_obstaculo not in ["x", "#", "!"]:
                print("Tipo de obstáculo inválido, pruebe de nuevo")
                continue

            # Bandera para verificar si se ha agregado un obstáculo
            obstaculo_agregado = False  
            while not obstaculo_agregado:
                # Solicita las coordenadas del obstáculo al usuario
                coord = input("Ingrese las coordenadas del obstáculo (x,y): ")
                try:
                    # Convierte la entrada del usuario en coordenadas x, y
                    x, y = map(int, coord.split(","))
                    if 0 <= x < len(self.mapa) and 0 <= y < len(self.mapa[0]):
                        if self.mapa[x][y] == 0:  # Verifica que no haya ya un obstáculo
                            if tipo_obstaculo == "x":
                                self.mapa[x][y] = 999  # Edificio, costo muy alto
                            elif tipo_obstaculo == "#":
                                self.mapa[x][y] = 2  # Bache, costo medio
                            elif tipo_obstaculo == "!":
                                self.mapa[x][y] = 3  # Agua, costo medio
                            obstaculo_agregado = True  # Establecer la bandera a True para salir del bucle interno
                        else:
                            print("Ya existe un obstáculo en esa coordenada, prueba de nuevo.")
                    else:
                        print("Las coordenadas están fuera del rango del mapa, prueba de nuevo.")
                except ValueError:
                    print("El formato de coordenadas es inválido, prueba de nuevo.")
        # Muestra el mapa actualizado
        self.mostrar_mapa()
        
        # Llamar a eliminar_obstaculos después de agregar obstáculos
        self.eliminar_obstaculos()

    def eliminar_obstaculos(self):
        # Permite al usuario eliminar obstáculos del mapa
        while True:
            # Solicita al usuario si quiere eliminar obstáculos
            respuesta = input("¿Quieres eliminar obstáculos? Si, No: ").lower()
            if respuesta == 'no':
                break
            if respuesta == 'si':
                while True:
                    # Solicita las coordenadas del obstáculo que se desea eliminar
                    coord = input("Ingrese las coordenadas del obstáculo que quiere eliminar (x,y) o 'basta' para terminar: ")
                    if coord.lower() == 'basta':
                        return
                    try:
                        x, y = map(int, coord.split(","))
                        if 0 <= x < len(self.mapa) and 0 <= y < len(self.mapa[0]):
                            if self.mapa[x][y] != 0:
                                self.mapa[x][y] = 0  # Eliminar el obstáculo
                                print("Obstáculo eliminado.")
                            else:
                                print("No hay ningún obstáculo en esas coordenadas, vuelva a probar.")
                        else:
                            print("Las coordenadas están fuera del rango del mapa, vuelva a probar.")
                    except ValueError:
                        print("El formato de coordenadas es inválido, intente de nuevo.")
            else:
                print("Respuesta inválida, intente de nuevo.")
        # Muestra el mapa actualizado
        self.mostrar_mapa()

    def obtener_coordenadas(self, mensaje):
        # Permite obtener coordenadas válidas del usuario
        while True:
            coord = input(mensaje)  # Solicita al usuario que ingrese las coordenadas
            try:
                x, y = map(int, coord.split(","))
                if 0 <= x < len(self.mapa) and 0 <= y < len(self.mapa[0]) and self.mapa[x][y] == 0:
                    return (x, y)  # Retorna las coordenadas si son válidas y no hay un obstáculo
                else:
                    print("Coordenadas inválidas o en un obstáculo, intente de nuevo.")
            except ValueError:
                print("El formato de coordenadas es inválido, prueba de nuevo.")

    def vecinos(self, nodo):
        # Obtiene los vecinos transitables de un nodo dado
        x, y = nodo
        resultados = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]  # Posibles movimientos: abajo, arriba, derecha, izquierda
        resultados = filter(lambda pos: 0 <= pos[0] < len(self.mapa) and 0 <= pos[1] < len(self.mapa[0]), resultados)
        return filter(lambda pos: self.mapa[pos[0]][pos[1]] != 999, resultados)  # Filtra posiciones transitables

# Define la clase Calculadora_Ruta
class Calculadora_Ruta:
    def __init__(self, mapa):
        self.mapa = mapa

    def heuristica(self, a, b):
        # Calcula la distancia de Manhattan entre dos puntos
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_estrella(self, inicio, fin):
        # Implementa el algoritmo A* para encontrar la ruta más corta
        cola = []
        heapq.heappush(cola, (0, inicio))  # Agregar el nodo de inicio con costo inicial 0 a la cola
        costos = {inicio: 0}  # Diccionario para almacenar los costos mínimos conocidos para cada nodo
        caminos = {inicio: None}  # Diccionario para almacenar el camino hacia cada nodo

        while cola:
            costo, actual = heapq.heappop(cola)  # Obtener el nodo actual de la cola según su costo estimado
            if actual == fin:
                camino = []
                while actual:
                    camino.append(actual)  # Construir el camino desde el fin hasta el inicio
                    actual = caminos[actual]
                camino.reverse()  # Invertir el camino para mostrarlo desde el inicio hasta el fin
                return camino, costo  # Retornar el camino y su costo total

            for vecino in self.mapa.vecinos(actual):
                nuevo_costo = costos[actual] + (self.mapa.mapa[vecino[0]][vecino[1]] if self.mapa.mapa[vecino[0]][vecino[1]] != 0 else 1)
                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo  # Actualizar el costo mínimo conocido para el vecino
                    prioridad = nuevo_costo + self.heuristica(fin, vecino)  # Calcular la prioridad para el vecino
                    heapq.heappush(cola, (prioridad, vecino))  # Agregar el vecino a la cola con su prioridad
                    caminos[vecino] = actual  # Registrar el camino hacia el vecino

        return None, 0  # Retornar None si no se encontró ruta, con costo 0
    
# Crear el mapa
mapa = Mapa(10, 10)
mapa.mostrar_mapa()  # Muestra el mapa vacío

# Permitir al usuario agregar obstáculos
mapa.agregar_obstaculos()

# Obtener coordenadas de inicio y fin
inicio = mapa.obtener_coordenadas("Ingrese las coordenadas del inicio (x,y): ")
fin = mapa.obtener_coordenadas("Ingrese las coordenadas del final (x,y): ")

# Crear una instancia del algoritmo y encontrar la ruta
algoritmo = Calculadora_Ruta(mapa)
ruta, costo = algoritmo.a_estrella(inicio, fin)

# Mostrar resultados
if ruta:
    print(f"Se encontró una ruta, el costo total de la ruta será de: {costo}")
    for paso in ruta:
        print(paso)
else:
    print("Lastimosamente no se encontró ninguna ruta.")
# Mostrar el mapa con el inicio, fin y la ruta encontrada
mapa.mostrar_mapa(inicio, fin, ruta)
