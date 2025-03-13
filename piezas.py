import pygame
import random

# Definición de colores
COLORES = [
    (0, 255, 255),  # Cyan - I
    (0, 0, 255),    # Azul - J
    (255, 165, 0),  # Naranja - L
    (255, 255, 0),  # Amarillo - O
    (0, 255, 0),    # Verde - S
    (128, 0, 128),  # Morado - T
    (255, 0, 0)     # Rojo - Z
]

# Definición de las formas de las piezas
FORMAS = [
    [[(0, -1), (0, 0), (0, 1), (0, 2)]],  # I
    [[(0, -1), (0, 0), (0, 1), (-1, 1)]],  # J
    [[(0, -1), (0, 0), (0, 1), (1, 1)]],  # L
    [[(0, 0), (0, 1), (1, 0), (1, 1)]],  # O
    [[(0, 0), (1, 0), (0, 1), (-1, 1)]],  # S
    [[(0, -1), (0, 0), (0, 1), (1, 0)]],  # T
    [[(0, 0), (-1, 0), (0, 1), (1, 1)]]   # Z
]

class Pieza:
    def __init__(self):
        """Inicializa una nueva pieza en la parte superior del tablero."""
        self.tipo = random.randint(0, len(FORMAS) - 1)
        self.forma = FORMAS[self.tipo][0]
        self.color = COLORES[self.tipo]
        self.x = 5  # Columna inicial
        self.y = 0  # Fila inicial

    def obtener_posiciones(self):
        """Devuelve las posiciones ocupadas por la pieza en el tablero."""
        return [(self.x + dx, self.y + dy) for dx, dy in self.forma]

    def colisiona(self, tablero, nueva_x, nueva_y, nueva_forma=None):
        """Comprueba si la pieza colisiona con los bordes o piezas fijas."""
        if nueva_forma is None:
            nueva_forma = self.forma

        for dx, dy in nueva_forma:
            x = nueva_x + dx
            y = nueva_y + dy

            if x < 0 or x >= 10 or y >= 20:
                return True
            if y >= 0 and tablero[y][x] is not None:
                return True

        return False

    def mover(self, dx, tablero):
        """Mueve la pieza a la izquierda o derecha si es posible."""
        nueva_x = self.x + dx
        if not self.colisiona(tablero, nueva_x, self.y):
            self.x = nueva_x

    def mover_abajo(self, tablero):
        """Mueve la pieza hacia abajo, devolviendo False si toca el suelo."""
        nueva_y = self.y + 1
        if not self.colisiona(tablero, self.x, nueva_y):
            self.y = nueva_y
            return True
        return False

    def rotar(self, tablero):
        """Rota la pieza si no colisiona."""
        nueva_forma = [(dy, -dx) for dx, dy in self.forma]  # Matriz de rotación 90°
        if not self.colisiona(tablero, self.x, self.y, nueva_forma):
            self.forma = nueva_forma

    def dibujar(self, ventana, TAMANO_CELDA):
        """Dibuja la pieza en la pantalla con una cuadrícula dentro de cada bloque."""
        ancho, alto = ventana.get_size()

        COLUMNAS = 10
        FILAS = 20

        x_inicio = (ancho - COLUMNAS * TAMANO_CELDA) // 2
        y_inicio = (alto - FILAS * TAMANO_CELDA) // 2

        for dx, dy in self.forma:  # ← Aquí recorremos las posiciones relativas correctas
            x_pix = x_inicio + (self.x + dx) * TAMANO_CELDA
            y_pix = y_inicio + (self.y + dy) * TAMANO_CELDA

            pygame.draw.rect(ventana, self.color, (x_pix, y_pix, TAMANO_CELDA, TAMANO_CELDA))

            # Dibujar líneas negras dentro del bloque para el efecto de cuadrícula
            borde = 2
            pygame.draw.line(ventana, (0, 0, 0), (x_pix, y_pix), (x_pix + TAMANO_CELDA, y_pix), borde)  # Superior
            pygame.draw.line(ventana, (0, 0, 0), (x_pix, y_pix), (x_pix, y_pix + TAMANO_CELDA), borde)  # Izquierda
            pygame.draw.line(ventana, (0, 0, 0), (x_pix + TAMANO_CELDA, y_pix), (x_pix + TAMANO_CELDA, y_pix + TAMANO_CELDA), borde)  # Derecha
            pygame.draw.line(ventana, (0, 0, 0), (x_pix, y_pix + TAMANO_CELDA), (x_pix + TAMANO_CELDA, y_pix + TAMANO_CELDA), borde)  # Inferior
