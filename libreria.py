import pygame
import random
import json

def recortar_imagen(nombre_img, cantidad_columnas, cantidad_filas):
    imagen = pygame.image.load(nombre_img)
    info_imagen = imagen.get_rect()
    ancho_imagen = info_imagen[2]
    alto_imagen = info_imagen[3]
    
    ancho_cuadro = ancho_imagen / cantidad_columnas
    alto_cuadro = alto_imagen / cantidad_filas

    ls_fila = []
    ls_imagen = []

    for fila in range(cantidad_filas):
        for columna in range(cantidad_columnas):
             cuadro = imagen.subsurface(columna*ancho_cuadro, fila*alto_cuadro, ancho_cuadro, alto_cuadro)
             ls_fila.append(cuadro)
        ls_imagen.append(ls_fila)
        ls_fila = []

    return ls_imagen

