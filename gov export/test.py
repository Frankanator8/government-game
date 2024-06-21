import pygame

import loader

pygame.init()
pygame.display.set_mode((800, 600))
def read_map(file):
    im = pygame.PixelArray(loader.load_image(file))
    for i in range(im.shape[1]):
        for j in range(im.shape[0]):
            color = im[i, j]
            r = color & 255
            g = (color >> 8) & 255
            b = (color >> 16) & 255
            print(r, g, b)

read_map("ec2map")