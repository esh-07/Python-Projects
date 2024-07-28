import pygame
import random
from shapely import affinity
import math

pygame.init()

s_w = 700
s_h = 600
screen = pygame.display.set_mode([s_w , s_h])
clock = pygame.time.Clock()


center_x = s_w/2
center_y = s_h/2


earth_img = pygame.image.load("earth.jpg").convert()
w,h = earth_img.get_size()
earth_img = pygame.transform.scale(earth_img, (w*0.5,h*0.5))
logo_rect = earth_img.get_rect(center = screen.get_rect().center)


class Sat():
    def __init__(self):
        self.r = 5                                                      # radius of planet
        self.R = random.randint(190,220)                                  # radius of orbit
        self.rot = random.randint(0,359)
        self.x = self.R*math.cos(math.radians(self.rot)) + center_x
        self.y = self.R*math.sin(math.radians(self.rot)) + center_y

    def move(self):
        self.rot = self.rot+1
        self.x = self.R*math.cos(math.radians(self.rot)) + center_x
        self.y = self.R*math.sin(math.radians(self.rot)) + center_y

    def show(self):
        pygame.draw.circle(screen, (0,0,255), (self.x, self.y), self.r)


class Decaying_sat(Sat):
    def __init__(self):
        super().__init__()
        self.decay_count = 0
        self.dot_count = 0
        self.dot_list = []

    def deacy(self):
        if self.decay_count%10 == 0:                             # change this to change the decay rate
            self.R = self.R-1
        self.decay_count = self.decay_count+1

    def show(self):
        if self.R<160:
            if self.dot_count%5 == 0:                           # change this to change the dots
                self.dot_list.append((self.x,self.y))
            self.dot_count = self.dot_count+1
            pygame.draw.circle(screen, (255,0,0), (self.x, self.y), self.r)
            for i in self.dot_list:
                pygame.draw.circle(screen, (255,255,255), (i[0], i[1]), 1)      # remove this to remove dots

        else:
            pygame.draw.circle(screen, (0,0,255), (self.x, self.y), self.r)


num_sat = 5
sat_list = []
for i in range(num_sat):
    sat_list.append(Sat())

p2 = Decaying_sat()



# Run until the user asks to quit
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0, 0, 0))
    screen.blit(earth_img,logo_rect)
    pygame.draw.circle(screen, (0, 255, 0), (center_x, center_y), 160,1)

    for i in sat_list:
        i.move()
        i.show()

    p2.move()
    p2.show()
    p2.deacy()

    clock.tick(30)
    pygame.display.flip()


pygame.quit()