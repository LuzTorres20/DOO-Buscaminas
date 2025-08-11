import random
import time
import pygame
import sys

def click_en_casilla(cantidad_casilla, celda, boton=1):
    x = cantidad_casilla[celda]['posicionXY'].centerx
    y = cantidad_casilla[celda]['posicionXY'].centery
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (x, y), 'button': boton}))
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (x, y), 'button': boton}))
    time.sleep(0.05)

def obtener_vecinos(cantidad_casilla, celda, numero):
    vecinos = []
    r, c = cantidad_casilla[celda]['indice']
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < numero and 0 <= nc < numero:
                for idx, info in cantidad_casilla.items():
                    if info['indice'] == (nr, nc):
                        vecinos.append(idx)
    return vecinos

def expandir_ceros(r, c, cantidad_casilla, numero):
    stack = [(r, c)]
    visitados = set()

    while stack:
        rr, cc = stack.pop()
        if (rr, cc) in visitados:
            continue
        visitados.add((rr, cc))

        for idx, info in cantidad_casilla.items():
            if info['indice'] == (rr, cc) and not info['pulsada']:
                click_en_casilla(cantidad_casilla, idx, 1)
                break

        # Esperamos que el juego actualice la casilla antes de seguir
        time.sleep(0.05)

        # Si esta celda es 0, añadimos vecinos para abrir
        valor = None
        for info in cantidad_casilla.values():
            if info['indice'] == (rr, cc):
                valor = info['valor']
                break

        if valor == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < numero and 0 <= nc < numero:
                        if (nr, nc) not in visitados:
                            stack.append((nr, nc))

def bot_jugar(numero, dificultad, casillas, cantidad_casilla, click_casilla, mostrar_resultado, run):
    ganar, perder = False, False
    esperando_click_usuario = True  # Espera el click del usuario para iniciar jugada

    # Primer click seguro aleatorio para iniciar el juego
    primera_celda = random.choice(list(cantidad_casilla.keys()))
    click_en_casilla(cantidad_casilla, primera_celda, 1)

    while not ganar and not perder:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detectar click izquierdo del usuario para continuar
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                esperando_click_usuario = False

            # Procesar clicks generados por el bot y sus efectos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ganar, perder = click_casilla(numero, event, dificultad)

        if esperando_click_usuario:
            # Espera hasta que el usuario haga click izquierdo para continuar
            continue

        # Aquí va la lógica del bot para hacer una jugada
        progreso = False
        for celda, info in cantidad_casilla.items():
            if not info['pulsada']:
                continue
            valor = info['valor']
            if isinstance(valor, int) and valor > 0:
                vecinos = obtener_vecinos(cantidad_casilla, celda, numero)
                ocultos = [v for v in vecinos if not cantidad_casilla[v]['pulsada'] and not cantidad_casilla[v]['bandera']]
                banderas = [v for v in vecinos if cantidad_casilla[v]['bandera']]

                if valor == len(ocultos) + len(banderas) and ocultos:
                    for v in ocultos:
                        click_en_casilla(cantidad_casilla, v, 3)
                        progreso = True
                        break
                elif valor == len(banderas) and ocultos:
                    for v in ocultos:
                        click_en_casilla(cantidad_casilla, v, 1)
                        r, c = cantidad_casilla[v]['indice']
                        if cantidad_casilla[v]['valor'] == 0:
                            expandir_ceros(r, c, cantidad_casilla, numero)
                        progreso = True
                        break
            if progreso:
                break

        if not progreso:
            ocultas = [idx for idx, d in cantidad_casilla.items() if not d['pulsada'] and not d['bandera']]
            if ocultas:
                click_en_casilla(cantidad_casilla, random.choice(ocultas), 1)

        esperando_click_usuario = True  # Pausa el bot hasta el próximo click del usuario

    mostrar_resultado(ganar)
    # run()

