import pygame
import random
import sys

# Configuración inicial
ANCHO_VENTANA = 600
FILAS = 10
COLUMNAS = 10
MINAS = 15

MARGEN_SUPERIOR = 50
TAM_CASILLA = ANCHO_VENTANA // COLUMNAS
ALTO_VENTANA = TAM_CASILLA * FILAS + MARGEN_SUPERIOR

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (189, 189, 189)
GRIS_OSCURO = (120, 120, 120)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AZUL_CLARO = (100, 149, 237)

pygame.init()
pygame.display.set_caption("Buscaminas")
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

TAM_CASILLA = min(ANCHO_VENTANA // COLUMNAS, ALTO_VENTANA // FILAS)
FUENTE = pygame.font.SysFont(None, TAM_CASILLA // 2)
FUENTE_MENU = pygame.font.SysFont(None, 48)


def crear_tablero():
    tablero = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
    minas_colocadas = 0

    while minas_colocadas < MINAS:
        fila = random.randint(0, FILAS - 1)
        col = random.randint(0, COLUMNAS - 1)
        if tablero[fila][col] != -1:
            tablero[fila][col] = -1
            minas_colocadas += 1

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            if tablero[fila][col] == -1:
                continue
            contador = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nf, nc = fila + dr, col + dc
                    if 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
                        if tablero[nf][nc] == -1:
                            contador += 1
            tablero[fila][col] = contador
    return tablero


def dibujar_tablero(ventana, tablero, descubiertas, marcadas):
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x = col * TAM_CASILLA
            y = fila * TAM_CASILLA + MARGEN_SUPERIOR  # Se ajusta la posición Y
            rect = pygame.Rect(x, y, TAM_CASILLA, TAM_CASILLA)

            if (fila, col) in descubiertas:
                pygame.draw.rect(ventana, GRIS_OSCURO, rect)
                valor = tablero[fila][col]
                if valor == -1:
                    pygame.draw.circle(ventana, ROJO, rect.center, TAM_CASILLA // 3)
                elif valor > 0:
                    texto = FUENTE.render(str(valor), True, NEGRO)
                    texto_rect = texto.get_rect(center=rect.center)
                    ventana.blit(texto, texto_rect)
            else:
                pygame.draw.rect(ventana, GRIS, rect)
                if (fila, col) in marcadas:
                    pygame.draw.polygon(ventana, ROJO, [
                        (x + TAM_CASILLA * 0.3, y + TAM_CASILLA * 0.2),
                        (x + TAM_CASILLA * 0.7, y + TAM_CASILLA * 0.5),
                        (x + TAM_CASILLA * 0.3, y + TAM_CASILLA * 0.8),
                    ])

            pygame.draw.rect(ventana, NEGRO, rect, 1)


def revelar_casilla(tablero, descubiertas, fila, col):
    if (fila, col) in descubiertas:
        return
    descubiertas.add((fila, col))
    if tablero[fila][col] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nf, nc = fila + dr, col + dc
                if 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
                    if (nf, nc) not in descubiertas:
                        revelar_casilla(tablero, descubiertas, nf, nc)


def verificar_victoria(tablero, descubiertas):
    total_sin_minas = FILAS * COLUMNAS - MINAS
    return len(descubiertas) == total_sin_minas


def obtener_vecinos(fila, col):
    vecinos = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nf, nc = fila + dr, col + dc
            if 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
                vecinos.append((nf, nc))
    return vecinos


def descubrir_seguro(tablero, descubiertas, fila, col, marcadas):
    if (fila, col) in descubiertas or (fila, col) in marcadas:
        return None, None
    if tablero[fila][col] == -1:
        # Revela todo (fin de juego)
        descubiertas.update({(r, c) for r in range(FILAS) for c in range(COLUMNAS)})
        juego_terminado = True
        gano = False
        return juego_terminado, gano
    else:
        revelar_casilla(tablero, descubiertas, fila, col)
        return None, None


def bot_jugar(tablero, descubiertas, marcadas):
    if len(descubiertas) == 0:
        fila = random.randint(0, FILAS - 1)
        col = random.randint(0, COLUMNAS - 1)
        jgt, g = descubrir_seguro(tablero, descubiertas, fila, col, marcadas)
        if jgt:
            return g 

    cambiado = False
    for (fila, col) in list(descubiertas):
        valor = tablero[fila][col]
        if valor <= 0:
            continue
        vecinos = obtener_vecinos(fila, col)
        marcadas_vecinas = [v for v in vecinos if v in marcadas]
        ocultas_vecinas = [v for v in vecinos if v not in descubiertas and v not in marcadas]

        if len(marcadas_vecinas) == valor and len(ocultas_vecinas) > 0:
            for casilla in ocultas_vecinas:
                jgt, g =  descubrir_seguro(tablero, descubiertas, casilla[0], casilla[1], marcadas)
                cambiado = True
                if jgt:
                    return g

        if len(ocultas_vecinas) > 0 and len(marcadas_vecinas) + len(ocultas_vecinas) == valor:
            for casilla in ocultas_vecinas:
                if casilla not in marcadas:
                    marcadas.add(casilla)
                    cambiado = True

    if not cambiado:
        posibles = [(r, c) for r in range(FILAS) for c in range(COLUMNAS)
                    if (r, c) not in descubiertas and (r, c) not in marcadas]
        if posibles:
            casilla = random.choice(posibles)
            jgt, g =  descubrir_seguro(tablero, descubiertas, casilla[0], casilla[1], marcadas)
            if jgt:
                return g

def dibujar_barra_estado(ventana, total_minas, marcadas):
    rect = pygame.Rect(0, 0, ANCHO_VENTANA, MARGEN_SUPERIOR)
    pygame.draw.rect(ventana, GRIS_OSCURO, rect)

    minas_restantes = total_minas - len(marcadas)
    texto = FUENTE_MENU.render(f"Minas activas restantes: {minas_restantes}", True, NEGRO)
    ventana.blit(texto, (10, 10))

def dibujar_menu(ventana, opciones, seleccion):
    ventana.fill(BLANCO)
    titulo = FUENTE_MENU.render("Buscaminas - Elige modo", True, NEGRO)
    ventana.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 100))

    for i, opcion in enumerate(opciones):
        color = AZUL_CLARO if i == seleccion else NEGRO
        texto = FUENTE_MENU.render(opcion, True, color)
        ventana.blit(texto, (ANCHO_VENTANA // 2 - texto.get_width() // 2, 200 + i * 60))

    pygame.display.flip()


def juego(modo_bot=False):
    tablero = crear_tablero()
    descubiertas = set()
    marcadas = set()
    juego_terminado = False
    gano = False

    reloj = pygame.time.Clock()
    tiempo_bot = 0
    intervalo_bot = 3000  # ms
    

    while True:
        dt = reloj.tick(30)
        tiempo_bot += dt
        ventana.fill(BLANCO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if juego_terminado:
                # Al presionar cualquier tecla o clic, salimos del juego para volver al menú
                if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                    return  # Salir a menú

            if not modo_bot and not juego_terminado:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    fila = y // TAM_CASILLA
                    col = x // TAM_CASILLA
                    if evento.button == 1:
                        if (fila, col) not in marcadas:
                            if tablero[fila][col] == -1:
                                descubiertas = {(r, c) for r in range(FILAS) for c in range(COLUMNAS)}
                                juego_terminado = True
                                gano = False
                            else:
                                revelar_casilla(tablero, descubiertas, fila, col)
                                if verificar_victoria(tablero, descubiertas):
                                    juego_terminado = True
                                    gano = True
                    elif evento.button == 3:
                        if (fila, col) in marcadas:
                            marcadas.remove((fila, col))
                        else:
                            if (fila, col) not in descubiertas:
                                marcadas.add((fila, col))

        if modo_bot and not juego_terminado and tiempo_bot >= intervalo_bot:
            g = bot_jugar(tablero, descubiertas, marcadas)
            if verificar_victoria(tablero, descubiertas):
                juego_terminado = True
                gano = True
            if g is False:
                juego_terminado = True
                gano = False
            tiempo_bot = 0
        
        dibujar_barra_estado(ventana, MINAS, marcadas) 
        dibujar_tablero(ventana, tablero, descubiertas, marcadas)

        if juego_terminado:
            texto = "¡Ganaste! Presiona tecla o clic para volver." if gano else "¡Perdiste! Presiona tecla o clic para volver."
            texto_render = FUENTE.render(texto, True, ROJO if not gano else VERDE)
            ventana.blit(texto_render, (10, ALTO_VENTANA - 30))

        pygame.display.flip()


def menu():
    opciones = ["Jugar tú mismo", "Dejar que el bot juegue"]
    seleccion = 0

    reloj = pygame.time.Clock()

    while True:
        reloj.tick(30)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        juego(modo_bot=False)
                    else:
                        juego(modo_bot=True)

        dibujar_menu(ventana, opciones, seleccion)


if __name__ == "__main__":
    menu()
