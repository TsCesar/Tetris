import pygame
from piezas import Pieza

pygame.init()

# Configuración de la pantalla
ANCHO_VENTANA = 600
ALTO_VENTANA = 800
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
pygame.display.set_caption("Tetris")

# Colores
NEGRO = (0, 0, 0)
GRIS = (50, 50, 50)

# Parámetros del juego
COLUMNAS = 10
FILAS = 20
MARGEN_X = 150
MARGEN_Y = 50

# Matriz del tablero
tablero = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]  # Guarda piezas fijas

def calcular_tamano_celda(ancho, alto):
    """Calcula el tamaño de cada celda dinámicamente."""
    return min((ancho - MARGEN_X * 2) // COLUMNAS, (alto - MARGEN_Y * 2) // FILAS)

def dibujar_cuadricula(TAMANO_CELDA):
    """Dibuja la cuadrícula del Tetris."""
    ancho, alto = ventana.get_size()
    x_inicio = (ancho - COLUMNAS * TAMANO_CELDA) // 2
    y_inicio = (alto - FILAS * TAMANO_CELDA) // 2

    for x in range(COLUMNAS + 1):
        pygame.draw.line(ventana, GRIS, 
                         (x_inicio + x * TAMANO_CELDA, y_inicio), 
                         (x_inicio + x * TAMANO_CELDA, y_inicio + FILAS * TAMANO_CELDA))

    for y in range(FILAS + 1):
        pygame.draw.line(ventana, GRIS, 
                         (x_inicio, y_inicio + y * TAMANO_CELDA), 
                         (x_inicio + COLUMNAS * TAMANO_CELDA, y_inicio + y * TAMANO_CELDA))

def fijar_pieza(tablero, pieza):
    """Fija la pieza en la matriz del tablero cuando toca el suelo."""
    for x, y in pieza.obtener_posiciones():
        if y >= 0:  # Asegurarse de no llenar fuera del tablero
            tablero[y][x] = pieza.color  # Guarda el color de la pieza

def limpiar_filas(tablero):
    """Elimina las filas completas y baja las superiores."""
    filas_completas = [i for i in range(FILAS) if all(tablero[i])]
    
    for fila in filas_completas:
        del tablero[fila]  # Borra la fila completa
        tablero.insert(0, [None] * COLUMNAS)  # Inserta una fila vacía arriba

def main():
    reloj = pygame.time.Clock()
    corriendo = True
    pieza = Pieza()
    teclas_presionadas = {"izquierda": False, "derecha": False}
    tiempo_movimiento = 0.1
    tiempo_ultimo_mov = 0

    while corriendo:
        dt = reloj.tick(60) / 1000
        ancho, alto = ventana.get_size()
        TAMANO_CELDA = calcular_tamano_celda(ancho, alto)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    teclas_presionadas["izquierda"] = True
                elif evento.key == pygame.K_RIGHT:
                    teclas_presionadas["derecha"] = True
                elif evento.key == pygame.K_UP:
                    pieza.rotar(tablero)  # La rotación ahora verifica colisiones
                elif evento.key == pygame.K_DOWN:
                    pieza.mover_abajo(tablero)  # Mueve la pieza más rápido
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    teclas_presionadas["izquierda"] = False
                elif evento.key == pygame.K_RIGHT:
                    teclas_presionadas["derecha"] = False

        # Movimiento continuo de la pieza
        tiempo_ultimo_mov += dt
        if tiempo_ultimo_mov >= tiempo_movimiento:
            if teclas_presionadas["izquierda"]:
                pieza.mover(-1, tablero)
            if teclas_presionadas["derecha"]:
                pieza.mover(1, tablero)
            tiempo_ultimo_mov = 0

        # Mover la pieza hacia abajo
        if not pieza.mover_abajo(tablero):
            fijar_pieza(tablero, pieza)
            limpiar_filas(tablero)
            pieza = Pieza()  # Nueva pieza

        # Dibujar la pantalla
        ventana.fill(NEGRO)
        dibujar_cuadricula(TAMANO_CELDA)

        # Dibujar piezas fijas
        for y, fila in enumerate(tablero):
            for x, color in enumerate(fila):
                if color:
                    pygame.draw.rect(ventana, color, 
                                     ((ancho - COLUMNAS * TAMANO_CELDA) // 2 + x * TAMANO_CELDA, 
                                      (alto - FILAS * TAMANO_CELDA) // 2 + y * TAMANO_CELDA, 
                                      TAMANO_CELDA, TAMANO_CELDA))

        # Dibujar la pieza actual
        pieza.dibujar(ventana, TAMANO_CELDA)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
