import sys
import random
import pygame

primera_celda = True


#numero de celsas = ind(x,y) -> posiciones tablero, posicion pantalla
#valores pulsado true o false
cantidad_celdas = {} 

bombas_activas = 0
bombas_inactivas = 0

def iniciar_tablero(numero, tamaño_cuadricula):
   
   global ventana, font, cuadricula, tamano_cuadricula
   cuadricula = []

   for x in range(numero):
      linea = [0] * numero
      cuadricula.append(linea)

   tamano_cuadricula = tamaño_cuadricula
   medidas = tamano_cuadricula * numero
   ventana = pygame.display.set_mode((medidas + 100, medidas))   
   
   font = pygame.font.Font(None, tamano_cuadricula)
   
   i = 0 
   
   for row in range(len(cuadricula)):
      for col in range(len(cuadricula[row])):
         square = pygame.Rect(
            2 + ( 1 * row * tamano_cuadricula), 
            2 + (1 * col * tamano_cuadricula), 
            tamano_cuadricula, 
            tamano_cuadricula)       
         pygame.draw.rect(ventana, 'black', square.inflate(2, 2))
         pygame.draw.rect(ventana, 'white', square)
         pygame.display.update()
         cantidad_celdas[i] = {
            'numero': 0, 
            'indice': {row,col}, 
            'posicionXY': square, 
            'valor': ' ', 
            'pulsado': False, 
            'bandera': False   
         }
         i += 1
         
   return cuadricula

def colocar_bombas(numero, primer_click, dificultad):
   global cuadricula, bombas_inactivas
   bombas = int(numero * numero * dificultad)