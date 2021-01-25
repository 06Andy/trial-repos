import pygame
import math
from random import randrange
from gameObject import Boid 

def rel_pos(target_object,viewed_object):
    return viewed_object.position - target_object.position

def view_angle(target_object,viewed_object):
    return target_object.direction.angle_to(viewed_object.position - target_object.position)

class Game:

    def __init__(self):

        self.width = 700
        self.height = 700
        self.white_colour = (255, 255, 255)
        self.game_window = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        self.frame_rate = 60
        self.number_of_boids = 100
        self.special_boid = Boid(self.width,self.height)
        self.special_boid.direction.x = 1
        self.special_boid.direction.y = 0
        self.boids = []
        for boid in range(self.number_of_boids):
            self.boids.append(Boid(self.width,self.height))

    def draw_boids(self):

        #self.game_window.fill(self.white_colour)

        for boid in self.boids:
            boid.move(self.width, self.height)
            pygame.draw.circle(self.game_window, boid.colour, (boid.position.x,boid.position.y), 10)

    def adjust_direction(self):
    
        for target_boid in self.boids:

            nearby_boids = []
            nearby_boid_distances = []
            ave_boid_direction = pygame.Vector2(0,0)
            ave_boid_position = pygame.Vector2(0,0)
            total_repulsive_force = pygame.Vector2(0,0)

            # Get a list of which boids are near the target boid
            for boid in self.boids:
                if boid != target_boid:
                    if rel_pos(target_boid,boid).length() < 200 and abs(view_angle(target_boid,boid))<130:
                        nearby_boids.append(boid)
                        nearby_boid_distances.append(rel_pos(target_boid,boid).length())

            if len(nearby_boids) > 0:

                for boid in nearby_boids:
                    ave_boid_direction += boid.direction
                    ave_boid_position += boid.position

                    if rel_pos(target_boid,boid).magnitude() < 100:
                        repulsive_force = (100/rel_pos(target_boid,boid).magnitude())-2
                        repulsive_vector = -repulsive_force*(boid.direction.normalize())
                        total_repulsive_force += repulsive_vector

                if total_repulsive_force.magnitude() > 0:
                    total_repulsive_force.normalize_ip()

                ave_boid_position = ave_boid_position / len(nearby_boids)
                ave_boid_position = ave_boid_position - target_boid.position

                boid_target = 10*ave_boid_direction.normalize() + 40*total_repulsive_force + 0.3*ave_boid_position

                angle_2 = (target_boid.direction).angle_to(boid_target)

                #target_boid.speed = 3 - (total_repulsive_force.magnitude()/10)
                if angle_2 > 0:
                    target_boid.direction = target_boid.direction.rotate(boid_target.magnitude()/10)
                else:
                    target_boid.direction = target_boid.direction.rotate(-boid_target.magnitude()/10)

    def run_game_loop(self):

        while True:
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # Impliment Logic

            self.adjust_direction()

            # Update the display
            self.special_boid.colour = (255,0,0)
            self.draw_boids()

            pygame.display.update()
            # Tick the clock
            self.clock.tick(self.frame_rate)