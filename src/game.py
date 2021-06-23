import random
import pygame
import numpy
from colorsys import hls_to_rgb

pygame.init()

win_size = pygame.math.Vector2(1920, 1024)
win = pygame.display.set_mode((int(win_size.x), int(win_size.y)))

pygame.display.set_caption("Swarm")

win_center = pygame.math.Vector2(win_size.x * 0.5, win_size.y * 0.5)
spawn_size = pygame.math.Vector2(win_center.x * 0.75, win_center.y * 0.75)
drone_radius = 50
widht = 40
height = 60
drone_start_velocity = 2
drone_start_distance_to = round(win_center.length())
drone_scream_range = 50
drone_count = 15
delay = 100
fps = 144

clock = pygame.time.Clock()
random.seed()

class drone(pygame.sprite.Sprite):
    def __init__(self,position, picture_path):
        super().__init__()
        self.color = (0, 0, 255)
        self.radius = drone_radius
        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        #self.image = pygame.Surface([self.radius, self.radius])
        #self.image.fill(self.color)
        self.rect = self.image.get_rect()
        #self.image = pygame.image.load(picture_path)
        self.position = pygame.math.Vector2(position)
        self.velocity = drone_start_velocity
        self.scream_range = drone_scream_range
        self.distance_to = {
            'queen': drone_start_distance_to,
            'food': {
                'a': drone_start_distance_to
            }
        }
        self.direction = pygame.math.Vector2()
        while self.direction.length() == 0:
            self.direction = pygame.math.Vector2(
                random.randint(-100, 100),
                random.randint(-100, 100)
            )
        self.direction = self.direction.normalize()
        self.collide_flag = False

    def draw(self, win):
        #self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
        pygame.draw.circle(win, self.color, (self.position.x, self.position.y), self.radius)

    def move(self):
        self.position += self.direction * self.velocity
        self.direction_old = pygame.math.Vector2(self.direction.x, self.direction.y)
        self.rect.center = self.position

    def reflect(self, norm_vec):
        self.direction = self.direction.reflect(pygame.math.Vector2(norm_vec))

    def border_check(self):
        new_position = pygame.math.Vector2(
            self.position.x + self.direction.x * self.velocity,
            self.position.y + self.direction.y * self.velocity)
        if new_position.x - self.radius <= 0:
            self.reflect((1, 0))
        if new_position.x + self.radius >= win_size.x:
            self.reflect((-1, 0))
        if new_position.y - self.radius <= 0:
            self.reflect((0, 1))
        if new_position.y + self.radius >= win_size.y:
            self.reflect((0, -1))

    def update(self):
        self.border_check()
        self.move()
        #self.draw(win)
        self.collide_flag = False

def redrawGameWindow():
    win.fill((0, 0, 0))

    drones.update()
    drones.draw(win)
    pygame.display.update()

#main loop
drones = pygame.sprite.Group()
for i in range(drone_count):
    position = pygame.math.Vector2(
        random.randint(-spawn_size.x, spawn_size.x) + win_center.x,
        random.randint(-spawn_size.y, spawn_size.y) + win_center.y
    )
    drones.add(drone(position, 'blob.png'))

run = True
while run:
    #pygame.time.delay(delay)
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for drone in drones:
        hits = pygame.sprite.spritecollide(drone, drones, False, pygame.sprite.collide_circle)
        l = len(hits)
        if l > 1 and l != drone_count:
            parent_hit = hits[0]
            #print(1, parent_hit.position)
            for i in range(1, len(hits)):
                child_hit = hits[i]

                middle_vec = pygame.math.Vector2( child_hit.position.x, child_hit.position.y)
                middle_vec -= parent_hit.position
                middle_vec = middle_vec.normalize()

                if parent_hit.collide_flag == False:
                    new_direction = pygame.math.Vector2(parent_hit.direction_old.x, parent_hit.direction_old.y)
                    new_direction += middle_vec
                    child_hit.direction = new_direction.normalize()
                    parent_hit.border_check()
                    parent_hit.collide_flag = True

                if child_hit.collide_flag == False:
                    new_direction = pygame.math.Vector2(child_hit.direction_old.x, child_hit.direction_old.y)
                    new_direction -= middle_vec
                    parent_hit.direction = new_direction.normalize()
                    child_hit.border_check()
                    child_hit.collide_flag = True

    redrawGameWindow()

pygame.quit()
