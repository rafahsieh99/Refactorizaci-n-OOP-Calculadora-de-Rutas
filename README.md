# Refactorizacion-OOP-Calculadora-de-Rutas
# Algoritmo de Búsqueda de Rutas con A*

Este proyecto implementa un algoritmo de búsqueda de rutas utilizando el algoritmo A* en un mapa. El mapa puede contener diferentes tipos de obstáculos, como edificios, baches y agua, que afectan el costo de la ruta.

## Características
- Crear un mapa de tamaño personalizado.
- Agregar diferentes tipos de obstáculos al mapa.
- Eliminar obstáculos del mapa.
- Encontrar la ruta más corta desde un punto de inicio hasta un punto final utilizando el algoritmo A*.
- Visualizar el mapa con el camino encontrado.
- 
## Uso
### 1. Crear el mapa

El programa comienza creando un mapa vacío de 10x10 (puede ser configurado modificando las dimensiones en el código).

```python
mapa = Mapa(10, 10)
mapa.mostrar_mapa()
```

### Agregar Obstaculos

El usuario puede agregar diferentes tipos de obstaculos al mapa.
- X para edificios (costo muy alto)
- #para baches (costo medio)
- ! para agua (costo medio)

### Eliminar Obstaculos

El usuario puede elegir eliminar obstaculos previamente agregados.

### Definir puntos de inicio y fin.

El usuario debe ingresar las coordenadas del punto de incio y del punto final.
- inicio = mapa.obtener_coordenadas("Ingrese las coordenadas del inicio (x,y): ")
- fin = mapa.obtener_coordenadas("Ingrese las coordenadas del final (x,y): ")
