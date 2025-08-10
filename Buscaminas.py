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
   primer_click = tuple(primer_click) 
   bombas = int(numero * numero * dificultad)
   bombas_inactivas = int(numero * numero * dificultad)
   rows = len(cuadricula)
   cols = len(cuadricula[0])  
   
   while bombas > 0:
      random_row = random.randint(0, rows - 1)
      random_col = random.randint(0, cols - 1)
      
      #verificar si la posicion aleatoria se encuentra denntro de la region de 3x3 al rededor del primer intetno.
      if(
         abs(random_row - primer_click[0]) <= 1 and 
         abs(random_col - primer_click[1]) <= 1
      ):
         
         continue #busca otra posicion aleatoria
      
      #si la posicion no esta en la region del 3x3 del primer click  y esta vacia (0)
      if cuadricula[random_row][random_col] == 0:
         cuadricula[random_row][random_col] = 'b'
         bombas -= 1
         
   donde_hay_bomba()
   
def donde_hay_bomba():
   numero_filas = len(cuadricula)   
   numero_columnas = len(cuadricula[0])
   
   indice = 0
   for row in range(numero_filas):
      for col in range(numero_columnas):
         bombas_alrededor = 0
         
         #verificacion celdas alrededor dentro del 3x3
         for i in range(-1, 2):
            for j in range(-1, 2):
               if i == 0 and j == 0:
                  continue # saltar la propia celda cuando pase por ahi
               
               try:
                  if row + i >= 0 and col + j >= 0:
                     if cuadricula[row + i][col + j] == 'b':
                        bombas_alrededor += 1
               except IndexError:
                  pass       
               
               #Actualizar la celda con el numero de bombas alrededor
               if cuadricula[row][col] != 'b':
                  cuadricula[row][col] = bombas_alrededor
                  
               cantidad_celdas[indice]['valor'] = cuadricula[row][col]
               indice += 1
               
def color_numero(element,color):
   valor_casilla =  font.render(
      str(cantidad_celdas[element]['valor']),
      True,
      color
   )
   ventana.blit(
      valor_casilla, 
      (cantidad_celdas[element]['posicionXY'].x + (tamano_cuadricula / 4),
      cantidad_celdas[element]['posicionXY'].y + (tamano_cuadricula / 8)))
   pygame.display.update()
   
def click_casilla(numero,event,dificultad):
   
   
   global primera_celda_pulsada, bombas_activas, bombas_inactivas
   for element in cantidad_celdas:
      if cantidad_celdas[element]['posicionXY'].collidepoint(event.pos):
         if primera_celda_pulsada:
            print(cantidad_celdas[element]['indice'])
            colocar_bombas(numero, cantidad_celdas[element]['indice'], dificultad)
            primera_celda_pulsada = False
         if not primera_celda_pulsada:
            keys = pygame.mouse.get_pressed()
            if keys[0] and not cantidad_celdas[element]['bandera'] == True:
               match cantidad_celdas[element]['valor']:
                  case 0:
                     color_numero(element, (0,0,255))
                  case 1:
                     color_numero(element, (0,255,0))
                  case 2:
                     color_numero(element, (255,255,0))
                  case 3:
                     color_numero(element, (255,100,255))
                  case 4:
                     color_numero(element, (200,0,0))
                  case 5:
                     color_numero(element, (255,0,0))
                  case 6:
                     color_numero(element, (255,0,0))
                  case 7:
                     color_numero(element, (255,0,0))
                  case 8:
                     color_numero(element, (255,0,0))
                  case 9:
                     color_numero(element, (255,0,0))
                  case 'b':
                     return False, True
               
               cantidad_celdas[element]['pulsado'] = True
            
            if keys[2]:
               if not cantidad_celdas[element]['pulsado'] == True and not cantidad_celdas[element]['bandera'] == True and not bombas_activas == 0:
                  valor_casilla = font.render('?', True, (0,0,0))
                  ventana.blit(
                     valor_casilla, 
                     (cantidad_celdas[element]['posicionXY'].x + 10,
                     cantidad_celdas[element]['posicionXY'].y + 5))
                  pygame.display.update()
                  cantidad_celdas[element]['bandera'] = True
                  bombas_activas -= 1
               
               elif not cantidad_celdas[element]['pulsado'] == True and cantidad_celdas[element]['bandera'] == False:
                  square = pygame.Rect(
                     cantidad_celdas[element]['posicionXY'].x,
                     cantidad_celdas[element]['posicionXY'].y,
                     tamano_cuadricula - 4, 
                     tamano_cuadricula - 4
                     )
                  pygame.draw.rect(ventana, 'white', square)
                  pygame.display.update()
                  cantidad_celdas[element]['bandera'] = False
                  bombas_activas += 1
                  
            if cantidad_celdas[element]['valor']== 'b' and cantidad_celdas[element]['bandera'] == True:
               bombas_inactivas -= 1
               if bombas_inactivas == 0:
                  return True, False
            
   return True, False

def menu():
   pygame.init()
   
   menu_activo = True
   font= pygame.font.Font(None, 50)
   
   screen = pygame.display.set_mode((400,400))
   
   easy_button = pygame.Rect(100, 0, 200, 80)
   normal_button = pygame.Rect(100, 100, 200, 80)
   hard_button = pygame.Rect(100, 200, 200, 80)
   
   BLACK_COLOR = (0, 0, 0)
   WHITE_COLOR = (255, 255, 255)
   while menu_activo:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         elif event.type == pygame.MOUSEBUTTONDOWN:
            if easy_button.collidepoint(event.pos):
               numero = 7
               dificultad = .3
               casillas = 40
               return numero, dificultad, casillas
            elif normal_button.collidepoint(event.pos):
               numero = 10
               dificultad = .5
               casillas= 40
               return numero, dificultad, casillas
            elif hard_button.collidepoint(event.pos):
               numero = 15
               dificultad = .7
               casillas = 40
               return numero, dificultad, casillas
            
         pygame.draw.rect(screen, BLACK_COLOR, easy_button)
         pygame.draw.rect(screen, BLACK_COLOR, normal_button)
         pygame.draw.rect(screen, BLACK_COLOR, hard_button)
         
         start_text = font.render('Facil', True, WHITE_COLOR)
         screen.blit(start_text, (easy_button.x + 40, easy_button.y + 20))
         
         start_text = font.render('Normal', True, WHITE_COLOR)
         screen.blit(start_text, (normal_button.x + 40, normal_button.y +  20))
         
         start_text = font.render('Dificil', True, WHITE_COLOR)
         screen.blit(start_text, (hard_button.x + 40, hard_button.y + 20))
         
         pygame.display.update()
         
def mostrar_bombas(numero,casillas):
   global bombas_activas
   x = numero * casillas + 50
   y = 0
   pygame.draw.rect(ventana, (0,0,0), (x, y, 100, 100))
   font = pygame.font.Font(None, 60)
   start_text = font.render(str(bombas_activas), True, (255, 255, 255))
   ventana.blit(start_text, (x , y ))
   pygame.display.update()
   
def game(numero, dificultad, casillas):
   global primera_celda_pulsada, cantidad_celdas, bombas_activas
   primera_celda_pulsada = True
   ganar, perder  = False, False
   while not ganar and not perder:
      for event in pygame.event.get():
         mostrar_bombas(numero, casillas)
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         elif event.type == pygame.MOUSEBUTTONDOWN:
            ganar, perder = click_casilla(numero, event, dificultad)
  
   cantidad_celdas = {}
   bombas_activas = 0
   run()
   
def run():
   global bombas_activas
   numero, dificultas, casillas = menu()
   iniciar_tablero(numero, casillas)
   bombas_inactivas = int(numero * numero * dificultas)
   bombas_activas = bombas_inactivas
   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         elif event.type == pygame.MOUSEBUTTONDOWN:
            game(numero, dificultas, casillas)
            
if __name__ == "__main__":
   run()