import pygame
import random
from libreria import *
import json

ANCHO=800
ALTO=600
VERDE=[0,255,0]
ROJO=[255,0,0]
AZUL=[0,0,255]
AMARILLO=[255,255,0]
AZUL_2=[0,255,255]
NEGRO=[0,0,0]
BLANCO=[255,255,255]
GRIS = [180,180,180]
BORDE_MAPA = 200

class Jugador(pygame.sprite.Sprite):
    def __init__(self, pos, ls_bloques_limite):
        '''
        El atributo direccion hace se utiliza para saber que sprite mostrar cuando se dibuja, mientras que los
        atributos direccion_x y direccion_y hacen referencia a hacia donde está mirando el jugador
        '''
        pygame.sprite.Sprite.__init__(self)
        #self.imagen = recortar_imagen('sprites/JugadorPrueba.png', 3, 4)
        self.imagen = recortar_imagen('sprites/Jugador.png', 3, 4)
        self.puntaje = 0
        self.direccion = 0
        self.contador = 0
        self.direccion_x = 0
        self.direccion_y = 0
        self.image = self.imagen[self.direccion][self.contador]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.ls_bloques_limite = ls_bloques_limite
        self.velocidad = 7
        self.velx = 0
        self.vely = 0
        self.salud = 249
        self.limite_contador_disparo = 15
        self.contador_disparo = random.randint(0, self.limite_contador_disparo)
        self.sonido_disparo = pygame.mixer.Sound('sonidos/bola_fuego.wav')
        self.sonido_disparo.set_volume(0.5)
        self.sonido_muerte = pygame.mixer.Sound('sonidos/muerte_jugador.wav')
        self.sonido_obtencion = pygame.mixer.Sound('sonidos/sonido_modificadores.wav')
        self.sonido_obtencion.set_volume(1.0)
        self.sonido_daño = pygame.mixer.Sound('sonidos/sonido_daño_jugador.wav')

    def update(self):
        self.rect.x+=self.velx
        self.rect.y+=self.vely
        self.contador_disparo += 1

        if self.velx != 0 or self.vely != 0:
            #el contador tiene que ser igual a los ticks a lo que va el juego
            if self.contador < 30:
                self.contador += 1
            else:
                self.contador = 0
            #Se divide el contador por 11 para darle una animación mas lenta a la hora de mostrar en pantalla
            self.image = self.imagen[self.direccion][self.contador // 11]

        self.verificar_colision()

    def disparar(self):
        if self.contador_disparo < self.limite_contador_disparo:
            return False
        else:
            self.contador_disparo = 0
            self.sonido_disparo.play()
            return True


    def mover(self, key):
        if key == pygame.K_DOWN:
            self.velx = 0
            self.vely = self.velocidad
            self.direccion = 0
            self.direccion_x = 0
            self.direccion_y = 1
        if key == pygame.K_LEFT:
            self.velx = -self.velocidad
            self.vely = 0
            self.direccion = 1
            self.direccion_x = -1
            self.direccion_y = 0
        if key == pygame.K_RIGHT:
            self.velx = self.velocidad
            self.vely = 0
            self.direccion = 2
            self.direccion_x = 1
            self.direccion_y = 0
        if key == pygame.K_UP:
            self.velx = 0
            self.vely = -self.velocidad
            self.direccion = 3
            self.direccion_x = 0
            self.direccion_y = -1

    def detener(self):
        self.velx = 0
        self.vely = 0

    def verificar_colision(self):

        ls_colision = pygame.sprite.spritecollide(self, self.ls_bloques_limite, False)

        for bloque in ls_colision:
            if self.rect.right > bloque.rect.left and self.velx > 0:
                self.rect.right = bloque.rect.left - 10
                self.velx = 0
            if self.rect.top < bloque.rect.bottom and self.vely < 0:
                self.rect.top = bloque.rect.bottom + 10
                self.vely = 0
            if self.rect.left < bloque.rect.right and self.velx < 0:
                self.rect.left = bloque.rect.right + 10
                self.velx = 0
            if self.rect.bottom > bloque.rect.top and self.vely > 0:
                self.rect.bottom = bloque.rect.top - 10
                self.vely = 0

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, pos, ls_bloques_limite, id_generador):
        pygame.sprite.Sprite.__init__(self)
        self.id_generador = id_generador
        self.imagen = recortar_imagen('sprites/enemigos2.png', 3, 4)
        self.direccion_sprite = 0
        self.contador_sprite = 0
        self.contador_movimiento = 60
        self.image = self.imagen[self.direccion_sprite][self.contador_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.ls_bloques_limite = ls_bloques_limite
        self.velx = 0
        self.vely = 0
        self.daño = 1
        self.salud = 250
        self.puntaje = 5
        self.sondio_muerte = pygame.mixer.Sound('sonidos/muerte_enemigos.wav')

    def update(self):
        self.mover()
        self.verificar_colision()
        self.dibujar()

    def mover(self):
        if self.contador_movimiento > 60:
            direccion_movimiento = random.randint(0,3)
            #Movimiento hacia abajo
            if direccion_movimiento == 0:
                self.velx = 0
                self.vely = 3
                self.direccion_sprite = 0
            #Movimiento hacia izquierda
            if direccion_movimiento == 1:
                self.velx = -3
                self.vely = 0
                self.direccion_sprite = 1
            #Movimiento hacia derecha
            if direccion_movimiento == 2:
                self.velx = 3
                self.vely = 0
                self.direccion_sprite = 2
            #Movimiento hacia arriba
            if direccion_movimiento == 3:
                self.velx = 0
                self.vely = -3
                self.direccion_sprite = 3

            self.contador_movimiento = 0
        else:
            self.contador_movimiento += 1

        self.rect.x+=self.velx
        self.rect.y+=self.vely

    def verificar_colision(self):

        ls_colision = pygame.sprite.spritecollide(self, self.ls_bloques_limite, False)

        for bloque in ls_colision:
            if self.rect.right > bloque.rect.left and self.velx > 0:
                self.rect.right = bloque.rect.left
                self.velx = 0
            elif self.rect.top < bloque.rect.bottom and self.vely < 0:
                self.rect.top = bloque.rect.bottom
                self.vely = 0
            elif self.rect.left < bloque.rect.right and self.velx < 0:
                self.rect.left = bloque.rect.right
                self.velx = 0
            elif self.rect.bottom > bloque.rect.top and self.vely > 0:
                self.rect.bottom = bloque.rect.top
                self.vely = 0

    def dibujar(self):
        if self.velx != 0 or self.vely != 0:
            #el contador tiene que ser igual a los ticks a lo que va el juego
            if self.contador_sprite < 30:
                self.contador_sprite += 1
            else:
                self.contador_sprite = 0
            #Se divide el contador por 11 para darle una animación mas lenta a la hora de mostrar en pantalla
            self.image = self.imagen[self.direccion_sprite][self.contador_sprite // 11]

class Proyectil(pygame.sprite.Sprite):
    daño = 20
    nombre_imagen = 'sprites/disparos2.png'

    def __init__(self, pos, direccion_x, direccion_y):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen(Proyectil.nombre_imagen, 4, 2)
        self.direccion_x = direccion_x
        self.direccion_y = direccion_y
        self.apuntado = 0
        self.image = self.imagen[1][self.apuntado]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
        self.daño = Proyectil.daño

    def update(self):
        self.mover()
        self.dibujar()

    def mover(self):
        if self.direccion_x == 1:
            self.velx = 5
            self.vely = 0
            self.apuntado = 0
        if self.direccion_x == -1:
            self.velx = -5
            self.vely = 0
            self.apuntado = 1
        if self.direccion_y == -1:
            self.velx = 0
            self.vely = -5
            self.apuntado = 2
        if self.direccion_y == 1:
            self.velx = 0
            self.vely = 5
            self.apuntado = 3

        self.rect.x+=self.velx
        self.rect.y+=self.vely

    def dibujar(self):
        self.image = self.imagen[1][self.apuntado]

class Bala(pygame.sprite.Sprite):
    def __init__(self, pos, direccion_movimiento):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('sprites/BalasMario.png', 3, 4)
        #La direccion_movimiento es 0: izquierda, 1: derecha, 2: arriba y 3: abajo
        self.direccion_movimiento = direccion_movimiento
        self.contador_sprite = 0
        self.image = self.imagen[self.direccion_movimiento][self.contador_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
        self.daño = 15

    def mover(self):
        if self.direccion_movimiento == 0:
            self.velx = -5
            self.vely = 0
        if self.direccion_movimiento == 1:
            self.velx = 5
            self.vely = 0
        if self.direccion_movimiento == 2:
            self.velx = 0
            self.vely = -5
        if self.direccion_movimiento == 3:
            self.velx = 0
            self.vely = 5

        self.rect.x += self.velx
        self.rect.y += self.vely


    def dibujar(self):
        if self.contador_sprite < 30:
            self.contador_sprite += 1
            self.image = self.imagen[self.direccion_movimiento][self.contador_sprite // 11]
        else:
            self.contador_sprite = 0


    def update(self):
        self.mover()
        self.dibujar()

class GeneradorEnemigos(pygame.sprite.Sprite):
    def __init__(self, pos, identificador):
        pygame.sprite.Sprite.__init__(self)
        self.identificador = identificador
        self.imagen = recortar_imagen('sprites/GeneradorEnemigos.png', 3, 4)
        self.contador_sprite = 0
        self.image = self.imagen[self.contador_sprite][0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.salud = 200
        self.contador_enemigos = 0
        self.limite_enemigos = 5
        self.puntaje = 10
        self.sonido_destruccion = pygame.mixer.Sound('sonidos/destruccion_generador.wav')
        self.sonido_destruccion.set_volume(1.0)


    def update(self):
        self.dibujar()

    def dibujar(self):
        if self.contador_sprite < 90:
            self.contador_sprite += 1
            self.image = self.imagen[self.contador_sprite // 30][0]
        else:
            self.contador_sprite = 0

    def revisar_enemigos(self):
        if (self.contador_enemigos < self.limite_enemigos):
            return True
        else:
            return False

class GeneradorBalas(pygame.sprite.Sprite):
    def __init__(self, pos, direccion):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('sprites/GeneradoresFlechas2.png', 4, 1)
        self.contador_sprite = 0
        self.image = self.imagen[0][self.contador_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        #La direccion es 0: izquierda, 1: derecha, 2: arriba y 3: abajo
        self.direccion = direccion
        self.limite_contador_disparo = 100
        self.contador_disparo = random.randint(0, self.limite_contador_disparo)

    def dibujar(self):
        if self.contador_sprite < 90:
            self.contador_sprite += 1
            self.image = self.imagen[0][self.contador_sprite // 30]
        else:
            self.contador_sprite = 0

    def disparar(self):
        if self.contador_disparo < self.limite_contador_disparo:
            self.contador_disparo += 1
            return False
        else:
            self.contador_disparo = 0
            return True


    def update(self):
        self.dibujar()

class BloqueLimite(pygame.sprite.Sprite):
    def __init__(self, posicion, imagen):
        pygame.sprite.Sprite.__init__(self)
        #self.imagen = recortar_imagen('sprites/Bloques.png', 6, 3)
        #self.image = self.imagen[1][0]
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]

    def update(self):
        pass

class ModificadorBala(pygame.sprite.Sprite):
    aumento_daño = 20
    nombre_cambio_imagen = 'sprites/disparos3.png'
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('sprites/Modificadores.png', 10, 4)
        self.image = self.imagen[2][5]
        self.rect = self.image.get_rect()
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]

    def update(self):
        pass

class ModificadorVida(pygame.sprite.Sprite):
    aumento_vida = 50
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('sprites/Modificadores.png', 10, 4)
        self.image = self.imagen[0][0]
        self.rect = self.image.get_rect()
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]

    def update(self):
        pass

class ModificadorPuntaje(pygame.sprite.Sprite):
    aumento_puntaje = 100
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('sprites/Modificadores.png', 10, 4)
        self.image = self.imagen[3][2]
        self.rect = self.image.get_rect()
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]

    def update(self):
        pass

class Fondo(pygame.sprite.Sprite):
    def __init__(self, pos, nombre_imagen):
        pygame.sprite.Sprite.__init__(self)
        self.posx = pos[0]
        self.posy = pos[1]
        self.velx = 0
        self.vely = 0
        self.imagen = pygame.image.load(nombre_imagen)
        self.rect = self.imagen.get_rect()
        self.ancho = self.rect[2]
        self.alto = self.rect[3]
        self.limite_derecho = ANCHO - BORDE_MAPA
        self.limite_izquierdo = BORDE_MAPA
        self.limite_superior = BORDE_MAPA
        self.limite_inferior = ALTO - BORDE_MAPA

    def mover(self):
        self.posx += self.velx
        self.posy += self.vely

    def update(self):
        self.mover()

def cargar_mapa(pantalla, nombre_json, nombre_sprites):
    bloques_limite = pygame.sprite.Group()

    #leer archivo xml
    img_textura=pygame.image.load(nombre_sprites)
    fila=[]
    for j in range(3):
        for i in range(6):
            cuadro=img_textura.subsurface(i*32,j*32,32,32)
            fila.append(cuadro)

    nom_archivo = nombre_json
    mapa_info=None
    with open(nom_archivo) as info:
        #mapa_info contiene la información del json
        mapa_info=json.load(info)
    info.close()

    dic_mapa=mapa_info['layers'][1]
    mapa=dic_mapa['data']
    con=0
    #extrer informacion de los limites
    limfilas=int(dic_mapa['height'])
    limcolumnas=int(dic_mapa['width'])
    for i in range(limfilas):
        for j in range(limcolumnas):
            if mapa[con] > 0:
                pos=mapa[con]-1
                bloque = BloqueLimite([j*32, i*32], fila[pos])
                bloques_limite.add(bloque)
            con+=1

    return bloques_limite

def mostrar_info(pantalla, fuente, texto, color, dimensiones, pos):
    letra = pygame.font.Font(fuente, dimensiones)
    superficie = letra.render(texto, True, color)
    rect = superficie.get_rect()
    pantalla.blit(superficie, pos)

def mostrar_info_salud(pantalla, matriz_sprites, salud_jugador, pos):
    cantidad_corazones = (salud_jugador + 50) // 50
    posx = pos[0]
    posy = pos[1]

    for i in range(cantidad_corazones):
        pantalla.blit(matriz_sprites[0][0], [posx, posy])
        posx += 32


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('JCUBO')
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    reloj = pygame.time.Clock()

    '''Banderas'''
    inicio_juego = False
    fin = False
    fin_juego = False
    ganar_juego = False
    game_over = False
    '''--------'''

    '''Musica Fondo'''
    pygame.mixer.music.load('sonidos/sonido_fondo.wav')
    pygame.mixer.music.play(-1)
    '''------------'''

    '''Pantalla inicio'''
    fondo_inicio = pygame.image.load('fondo_inicio.png')
    

    while (not fin) and (not inicio_juego):
        #Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    inicio_juego = True
        pantalla.fill(NEGRO)
        pantalla.blit(fondo_inicio, [0,0])
        info_inicio = '(Presiona la tecla espacio...)'
        mostrar_info(pantalla, None, info_inicio, BLANCO, 30, [250, 550])

        pygame.display.flip()

    '''---------------'''

    '''Pantalla juego'''

    '''Fondo'''
    fondo = Fondo([-320,-320], 'FondoGrande.png')
    imagen_corazones = recortar_imagen('corazones.png', 3, 1)
    '''-----'''

    ''' Grupos de objetos'''
    jugadores = pygame.sprite.Group()
    proyectiles = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    generadores_enemigos = pygame.sprite.Group()
    bloques_limite = pygame.sprite.Group()
    generadores_balas = pygame.sprite.Group()
    balas = pygame.sprite.Group()
    modificadores_bala = pygame.sprite.Group()
    modificadores_vida = pygame.sprite.Group()
    modificadores_puntaje = pygame.sprite.Group()

    '''------------------'''

    '''Instacias de clases y agregado a grupos'''
    #Creacion de los bloques
    bloques_limite = cargar_mapa(pantalla, 'fondo.json', 'Textura.png')

    #Creacion del jugador
    jugador = Jugador([50,50], bloques_limite)
    jugadores.add(jugador)

    #Creacion de generadores de enemigos
    generador = GeneradorEnemigos([320, 320], 1)
    generadores_enemigos.add(generador)

    generador2 = GeneradorEnemigos([2944, 480], 2)
    generadores_enemigos.add(generador2)

    generador3 = GeneradorEnemigos([1696, 832], 3)
    generadores_enemigos.add(generador3)

    generador4 = GeneradorEnemigos([352, 1504], 4)
    generadores_enemigos.add(generador4)

    generador5 = GeneradorEnemigos([2912,1472], 5)
    generadores_enemigos.add(generador5)

    #Creacion generadores de balas borde superior
    cantidad_generadores_balas = 4
    posx_inicial_superior = 352
    for i in range(cantidad_generadores_balas):
        posicion = [posx_inicial_superior + (800*i), 0]
        direccion = 3
        generador_balas = GeneradorBalas(posicion, direccion)
        generadores_balas.add(generador_balas)

    #Creacion generadores de balas borde inferior
    cantidad_generadores_balas = 4
    posx_inicial_inferior = 384
    for i in range(cantidad_generadores_balas):
        posicion = [posx_inicial_inferior + (800*i), 1792]
        direccion = 2
        generador_balas = GeneradorBalas(posicion, direccion)
        generadores_balas.add(generador_balas)

    #Creacion generadores de balas borde izquierdo
    cantidad_generadores_balas = 3
    posy_inicial_izquierdo = 320
    for i in range(cantidad_generadores_balas):
        posicion = [0 ,posy_inicial_izquierdo + (576*i)]
        direccion = 1
        generador_balas = GeneradorBalas(posicion, direccion)
        generadores_balas.add(generador_balas)

    #Creacion generadores de balas borde derecho
    cantidad_generadores_balas = 3
    posy_inicial_derecha = 288
    for i in range(cantidad_generadores_balas):
        posicion = [3168 ,posy_inicial_derecha + (576*i)]
        direccion = 0
        generador_balas = GeneradorBalas(posicion, direccion)
        generadores_balas.add(generador_balas)

    '''-------------------'''

    '''Pantalla juego'''

    while (not fin) and (not fin_juego):
        #Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                jugador.mover(event.key)
                if event.key == pygame.K_SPACE and jugador.disparar() and jugador.salud > 0:
                    posicion = [jugador.rect.x, jugador.rect.y]
                    direccion_x = jugador.direccion_x
                    direccion_y = jugador.direccion_y
                    proyectil = Proyectil(posicion, direccion_x, direccion_y)
                    proyectiles.add(proyectil)
                    print(f'Projectiles en pantalla: {len(proyectiles)}')
            if event.type == pygame.KEYUP:
                jugador.detener()

        '''Control'''
        '''Proyectiles'''
        for proyectil in proyectiles:
            #Revision borde superior
            if proyectil.rect.bottom < 0:
                proyectiles.remove(proyectil)
            #Revision borde inferior
            if proyectil.rect.top > ALTO:
                proyectiles.remove(proyectil)
            #Revision borde derecho
            if proyectil.rect.left > ANCHO:
                proyectiles.remove(proyectil)
            #Revision borde izquierdo
            if proyectil.rect.right < 0:
                proyectiles.remove(proyectil)

            #Revision de colision con un bloque
            ls_colision = pygame.sprite.spritecollide(proyectil, bloques_limite, False)
            if(len(ls_colision) > 0):
                proyectiles.remove(proyectil)

        '''Generadores de enemigos'''
        if (len(generadores_enemigos) == 0):
            fin_juego = True
            ganar_juego = True
        for generador in generadores_enemigos:
            #Creacion de enemigos
            if generador.revisar_enemigos():
                posicion = [generador.rect.centerx, generador.rect.centery]
                enemigo = Enemigo(posicion, bloques_limite, generador.identificador)
                generador.contador_enemigos += 1
                enemigos.add(enemigo)

            #Revision de colision con proyectiles
            ls_colision = pygame.sprite.spritecollide(generador, proyectiles, True)
            if(len(ls_colision) > 0):
                generador.salud -= proyectil.daño

            #Revision de vida de generador
            if (generador.salud < 0):
                jugador.puntaje += generador.puntaje
                posicion = [generador.rect.x, generador.rect.y]
                probabilidad = random.randint(0,2)

                #Seleccion del modificador que debe aparecer al momento de derrotar un generador
                if probabilidad == 0:
                    modificador = ModificadorVida(posicion)
                    modificadores_vida.add(modificador)
                if probabilidad == 1:
                    modificador = ModificadorPuntaje(posicion)
                    modificadores_puntaje.add(modificador)
                if probabilidad == 2:
                    modificador = ModificadorBala(posicion)
                    modificadores_bala.add(modificador)

                print(f'El puntaje del jugador es: {jugador.puntaje}')
                generador.sonido_destruccion.play()
                generadores_enemigos.remove(generador)


        '''Balas'''
        for bala in balas:
            #Revision borde superior
            if bala.rect.bottom < 0:
                balas.remove(bala)
            #Revision borde inferior
            if bala.rect.top > ALTO:
                balas.remove(bala)
            #Revision borde derecho
            if bala.rect.left > ANCHO:
                balas.remove(bala)
            #Revision borde izquierdo
            if bala.rect.right < 0:
                balas.remove(bala)


        '''Generadores de balas'''
        for generador_balas in generadores_balas:
            #Revision para disparo
            if generador_balas.disparar():
                posicion = [generador_balas.rect.x, generador_balas.rect.y]
                direccion = generador_balas.direccion
                bala = Bala(posicion, direccion)
                balas.add(bala)
                print(len(balas))

            #Revision de colision contra proyectil de jugador
            ls_colision = pygame.sprite.spritecollide(generador_balas, proyectiles, True)


        '''Enemigos'''
        for enemigo in enemigos:

            #Revisar si el enemigo colisiona con el jugador
            ls_colision = pygame.sprite.spritecollide(enemigo, jugadores, False)
            if(len(ls_colision) > 0):
                jugador.salud -= enemigo.daño
                jugador.sonido_daño.play()
                print(f'Salud jugador: {jugador.salud}')

            #Revision de impacto de un proyectil
            ls_colision = pygame.sprite.spritecollide(enemigo, proyectiles, True)
            if(len(ls_colision) > 0):
                jugador.puntaje += enemigo.puntaje
                print(f'El puntaje del jugador es: {jugador.puntaje}')
                id_generador = enemigo.id_generador
                if id_generador == 1:
                    generador.contador_enemigos -=1
                    enemigo.sondio_muerte.play()
                    enemigos.remove(enemigo)
                if id_generador == 2:
                     generador2.contador_enemigos -=1
                     enemigo.sondio_muerte.play()
                     enemigos.remove(enemigo)
                if id_generador == 3:
                     generador3.contador_enemigos -=1
                     enemigo.sondio_muerte.play()
                     enemigos.remove(enemigo)
                if id_generador == 4:
                     generador4.contador_enemigos -=1
                     enemigo.sondio_muerte.play()
                     enemigos.remove(enemigo)
                if id_generador == 5:
                     generador5.contador_enemigos -=1
                     enemigo.sondio_muerte.play()
                     enemigos.remove(enemigo)


        '''Jugador'''
        #Este ciclo solo realiza una iteracion porque solo exite un jugador
        for jugador in jugadores:
            #CHEQUEO si el jugador tiene vida
            if jugador.salud < 0:
                jugador.sonido_daño.stop()
                jugador.sonido_disparo.stop()
                jugador.sonido_muerte.play()
                pygame.mixer.music.pause()
                fin_juego = True
                game_over = True
                jugadores.remove(jugador)                
            
            #Revision colision balas
            ls_colision = pygame.sprite.spritecollide(jugador, balas, True)
            if(len(ls_colision) > 0):
                jugador.salud -= bala.daño
                jugador.sonido_daño.play()
                print(f'Salud del jugador: {jugador.salud}')

            #Revision de colision con el modificador de bala
            ls_colision = pygame.sprite.spritecollide(jugador, modificadores_bala, True)
            if(len(ls_colision) > 0):
                jugador.sonido_obtencion.play()
                Proyectil.daño += ModificadorBala.aumento_daño
                Proyectil.nombre_imagen = ModificadorBala.nombre_cambio_imagen

            #Revision de colision con el modificador de vida
            ls_colision = pygame.sprite.spritecollide(jugador, modificadores_vida, True)
            if(len(ls_colision) > 0):
                jugador.sonido_obtencion.play()
                jugador.salud += ModificadorVida.aumento_vida

            #Revision de colision con el modificador de puntaje
            ls_colision = pygame.sprite.spritecollide(jugador, modificadores_puntaje, True)
            if(len(ls_colision) > 0):
                jugador.sonido_obtencion.play()
                jugador.puntaje += ModificadorPuntaje.aumento_puntaje
                print(f'El puntaje del jugador es: {jugador.puntaje}')

        '''-------'''


        '''Gestion fondo'''
        #Gestion borde derecho
        if jugador.rect.right > fondo.limite_derecho:
            jugador.rect.right = fondo.limite_derecho
            fondo.posx -= jugador.velocidad
            #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.x -= jugador.velocidad
            #Reubicacion generadores
            for generador in generadores_enemigos:
                generador.rect.x -= jugador.velocidad
            #Reubicacion enemigos
            for enemigo in enemigos:
                enemigo.rect.x -= jugador.velocidad
            #Reubicacion generadores de balas
            for generador_bala in generadores_balas:
                generador_bala.rect.x -= jugador.velocidad
            #Reubicacion balas
            for bala in balas:
                bala.rect.x -= jugador.velocidad
            #Reubicacion proyectiles
            for proyectil in proyectiles:
                proyectil.rect.x -= jugador.velocidad
            #Reubicacion modificadores
            for modificador_vida in modificadores_vida:
                modificador_vida.rect.x -= jugador.velocidad 
            for modificador_bala in modificadores_bala:
                modificador_bala.rect.x -= jugador.velocidad
            for modificador_puntaje in modificadores_puntaje:
                modificador_puntaje.rect.x -= jugador.velocidad
            
        #Gestion borde izquierdo
        if jugador.rect.left < fondo.limite_izquierdo:
            jugador.rect.left = fondo.limite_izquierdo
            fondo.posx += jugador.velocidad
            #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.x += jugador.velocidad
            #Reubicacion generadores
            for generador in generadores_enemigos:
                generador.rect.x += jugador.velocidad
            #Reubicacion enemigos
            for enemigo in enemigos:
                enemigo.rect.x += jugador.velocidad
            #Reubicacion generadores de balas
            for generador_bala in generadores_balas:
                generador_bala.rect.x += jugador.velocidad
            #Reubicacion balas
            for bala in balas:
                bala.rect.x += jugador.velocidad
            #Reubicacion proyectiles
            for proyectil in proyectiles:
                proyectil.rect.x += jugador.velocidad
            #Reubicacion modificadores
            for modificador_vida in modificadores_vida:
                modificador_vida.rect.x += jugador.velocidad 
            for modificador_bala in modificadores_bala:
                modificador_bala.rect.x += jugador.velocidad
            for modificador_puntaje in modificadores_puntaje:
                modificador_puntaje.rect.x +=jugador.velocidad    

        #Gestion border superior
        if jugador.rect.top < fondo.limite_superior:
            jugador.rect.top = fondo.limite_superior
            fondo.posy += jugador.velocidad
            #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.y += jugador.velocidad
            #Reubicacion generadores
            for generador in generadores_enemigos:
                generador.rect.y += jugador.velocidad
            #Reubicacion enemigos
            for enemigo in enemigos:
                enemigo.rect.y += jugador.velocidad
            #Reubicacion generadores de balas
            for generador_bala in generadores_balas:
                generador_bala.rect.y += jugador.velocidad
            #Reubicacion balas
            for bala in balas:
                bala.rect.y += jugador.velocidad
            #Reubicacion proyectiles
            for proyectil in proyectiles:
                proyectil.rect.y += jugador.velocidad
            #Reubicacion modificadores
            for modificador_vida in modificadores_vida:
                modificador_vida.rect.y += jugador.velocidad 
            for modificador_bala in modificadores_bala:
                modificador_bala.rect.y += jugador.velocidad
            for modificador_puntaje in modificadores_puntaje:
                modificador_puntaje.rect.y += jugador.velocidad

        #Gestrion borde inferior
        if jugador.rect.bottom > fondo.limite_inferior:
            jugador.rect.bottom = fondo.limite_inferior
            fondo.posy -= jugador.velocidad
            #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.y -= jugador.velocidad
            #Reubicacion generadores
            for generador in generadores_enemigos:
                generador.rect.y -= jugador.velocidad
            #Reubicacion enemigos
            for enemigo in enemigos:
                enemigo.rect.y -= jugador.velocidad
            #Reubicacion generadores de balas
            for generador_bala in generadores_balas:
                generador_bala.rect.y -= jugador.velocidad
            #Reubicacion balas
            for bala in balas:
                bala.rect.y -= jugador.velocidad
            #Reubicacion proyectiles
            for proyectil in proyectiles:
                proyectil.rect.y -= jugador.velocidad
            #Reubicacion modificadores
            for modificador_vida in modificadores_vida:
                modificador_vida.rect.y -= jugador.velocidad
            for modificador_bala in modificadores_bala:
                modificador_bala.rect.y -= jugador.velocidad
            for modificador_puntaje in modificadores_puntaje:
                modificador_puntaje.rect.y -= jugador.velocidad

        '''-------------'''

        pantalla.fill(NEGRO)

        '''Actualizacion de grupos'''
        bloques_limite.update()
        jugadores.update()
        proyectiles.update()
        enemigos.update()
        generadores_enemigos.update()
        generadores_balas.update()
        balas.update()
        modificadores_bala.update()
        modificadores_vida.update()
        modificadores_puntaje.update()
        '''-----------------------'''

        '''Dibujar objetos'''
        #pantalla = movimiento_mapa(pantalla, fondo, jugador)
        pantalla.blit(fondo.imagen, [fondo.posx, fondo.posy])
        bloques_limite.draw(pantalla)
        jugadores.draw(pantalla)
        proyectiles.draw(pantalla)
        generadores_enemigos.draw(pantalla)
        enemigos.draw(pantalla)
        generadores_balas.draw(pantalla)
        balas.draw(pantalla)
        modificadores_bala.draw(pantalla)
        modificadores_vida.draw(pantalla)
        modificadores_puntaje.draw(pantalla)
        '''---------------'''

        '''Refresco pantalla'''
        info_puntaje_jugador = 'Puntaje: ' +  str(jugador.puntaje)
        mostrar_info(pantalla, None, info_puntaje_jugador, AZUL, 44, [600,20])
        mostrar_info_salud(pantalla, imagen_corazones, jugador.salud, [50,20])
        info_salud_jugador = 'Salud: ' +  str(jugador.salud + 1)
        mostrar_info(pantalla, None, info_salud_jugador, AZUL, 30, [55,70])
        info_generadores_restantes = 'Generadores: ' + str(len(generadores_enemigos))
        mostrar_info(pantalla, None, info_generadores_restantes, NEGRO, 30, [600,70])
        pygame.display.flip()
        reloj.tick(30)
        fondo.update()
        '''-----------------'''

    '''--------------'''

    '''Pantalla game over'''
    fondo_game_over = pygame.image.load('fondo_game_over.jpg')
    

    while (not fin) and (game_over):
        #Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
        pantalla.fill(NEGRO)
        pantalla.blit(fondo_game_over, [0,0])
        info_puntaje_jugador = 'PUNTAJE FINAL: ' + str(jugador.puntaje)
        mostrar_info(pantalla, None, info_puntaje_jugador, BLANCO, 44, [250, 50])

        pygame.display.flip()

    '''---------------'''

    '''Pantalla win'''
    fondo_win = pygame.image.load('fondo_win.png')
    
    while (not fin) and (ganar_juego):
        #Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
        pantalla.fill(NEGRO)
        pantalla.blit(fondo_win, [0,0])
        info_puntaje_jugador = 'PUNTAJE FINAL: ' + str(jugador.puntaje)
        mostrar_info(pantalla, None, info_puntaje_jugador, BLANCO, 44, [250, 400])

        pygame.display.flip()

    '''---------------'''