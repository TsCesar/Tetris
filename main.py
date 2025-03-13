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
ROJO = (200, 0, 0)

# Parámetros del juego
COLUMNAS = 10
FILAS = 20
MARGEN_X = 150
MARGEN_Y = 50
TIEMPO_CAIDA = 0.5  # Tiempo en segundos entre caídas automáticas

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
        if y >= 0:
            tablero[y][x] = pieza.color

def limpiar_filas(tablero):
    """Elimina las filas completas y baja las superiores."""
    filas_completas = [i for i in range(FILAS) if all(tablero[i])]
    
    for fila in filas_completas:
        del tablero[fila]  # Borra la fila completa
        tablero.insert(0, [None] * COLUMNAS)  # Inserta una fila vacía arriba

def verificar_game_over(tablero):
    """Devuelve True si el tablero está lleno y no se pueden generar nuevas piezas."""
    return any(tablero[0])  # Si la fila superior tiene piezas, el juego termina

def main():
    reloj = pygame.time.Clock()
    corriendo = True
    pieza = Pieza()
    tiempo_ultimo_mov = 0
    tiempo_ultimo_descenso = 0
    game_over = False

    while corriendo:
        dt = reloj.tick(60) / 1000  # Tiempo en segundos desde la última iteración
        ancho, alto = ventana.get_size()
        TAMANO_CELDA = calcular_tamano_celda(ancho, alto)

        # Capturar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    pieza.rotar(tablero)  # Rotar solo al presionar la tecla

        # Detectar teclas presionadas
        teclas = pygame.key.get_pressed()
    
        # Movimiento lateral con retardo para repetición
        if teclas[pygame.K_LEFT]:
            if tiempo_ultimo_mov <= 0:
                pieza.mover(-1, tablero)
                tiempo_ultimo_mov = 0.1  # Tiempo de espera entre repeticiones
        elif teclas[pygame.K_RIGHT]:
            if tiempo_ultimo_mov <= 0:
                pieza.mover(1, tablero)
                tiempo_ultimo_mov = 0.1
        else:
            tiempo_ultimo_mov = 0  # Reiniciar el temporizador si no hay movimiento

        # Movimiento hacia abajo más rápido al mantener ↓
        if teclas[pygame.K_DOWN]:
            tiempo_caida_actual = 0.05  # Aumenta la velocidad de caída
        else:
            tiempo_caida_actual = TIEMPO_CAIDA  # Vuelve a la velocidad normal

        # Movimiento automático hacia abajo
        tiempo_ultimo_descenso += dt
        if tiempo_ultimo_descenso >= tiempo_caida_actual:
            if not pieza.mover_abajo(tablero):
                fijar_pieza(tablero, pieza)
                limpiar_filas(tablero)
                if verificar_game_over(tablero):
                    game_over = True
                else:
                    pieza = Pieza()
            tiempo_ultimo_descenso = 0

        tiempo_ultimo_mov -= dt  # Reducir el contador de repetición

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

        # Mostrar "Game Over" si el juego ha terminado
        if game_over:
            fuente = pygame.font.Font(None, 50)
            texto = fuente.render("GAME OVER", True, ROJO)
            ventana.blit(texto, ((ANCHO_VENTANA - texto.get_width()) // 2, ALTO_VENTANA // 2))

        pygame.display.flip()


if __name__ == "__main__":
    main()