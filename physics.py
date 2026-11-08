import pygame
import os
import math
import sys

pygame.init()
pygame.display.set_caption("PyPhy Engine")

WIDTH, HEIGHT = 1000, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_ball(window, balls, radius):
    for pos in balls:
        pygame.draw.circle(window, (0, 255, 0), pos, radius)
        pygame.draw.circle(window, (0, 0, 0), pos, radius, 1)


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
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                balls.append(event.pos)

        window.fill((255, 255, 255))
        draw_grid()

        draw_ball(window, balls, 20)

        pygame.display.update()

        if not run:
            print("Exiting...")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main(window)