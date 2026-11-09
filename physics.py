import pygame
import os
import math
import sys

pygame.init()
pygame.display.set_caption("PyPhy Engine")

WIDTH, HEIGHT = 1000, 600
PTM = 100
GRAVITY = 9.8
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))

class Balls():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.dy = 0
        self.dx = 0

    def draw_balls(self):
        pygame.draw.circle(window, (0, 255, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(window, (0, 0, 0), (self.x, self.y), self.radius, 1)

    def update_physics(self, dt):
        self.dy += GRAVITY * dt
        self.y += self.dy * PTM * dt

    
def simulate_ball(balls, dt):
    for ball in balls:
        ball.draw_balls()
        ball.update_physics(dt)


def draw_grid():
    grid_size = 30

    for x in range(0, WIDTH, grid_size):
        pygame.draw.line(window, (211, 211, 211), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, grid_size):
        pygame.draw.line(window, (211, 211, 211), (0, y), (WIDTH, y))


def main(window):
    clock = pygame.time.Clock()
    run = True

    balls = []

    while run:
        dt = clock.tick(FPS)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                ball = Balls(pos[0], pos[1], 20)
                balls.append(ball)
                

        window.fill((255, 255, 255))
        draw_grid()

        simulate_ball(balls, dt)

        pygame.display.update()

        if not run:
            print("Exiting...")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main(window)