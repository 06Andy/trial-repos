import pygame
import math
from random import randrange

class Boid:

    def __init__(self,max_width,max_height):

        self.scale = 1
        self.speed = 3
        self.position = pygame.math.Vector2(randrange(0,max_width),randrange(0,max_height))
        self.initial_direction = randrange(0,360)
        self.direction = pygame.math.Vector2(math.sin(self.initial_direction/360*2*math.pi),math.cos(self.initial_direction/360*2*math.pi))
        self.colour = (randrange(0,256),randrange(0,256),randrange(0,256))

    def move(self,max_width,max_height):
        
        self.position += self.direction*self.speed

        if self.position.x > max_width:
            self.position.x -= max_width
        elif self.position.x < 0:
            self.position.x += max_width
        if self.position.y >= max_height:
            self.position.y -= max_height
        elif self.position.y < 0:
            self.position.y += max_height

