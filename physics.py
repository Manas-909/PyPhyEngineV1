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
        self.dragging = True
        self.pre_pos = (x, y)

    def draw_balls(self):
        pygame.draw.circle(window, (0, 255, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(window, (0, 0, 0), (self.x, self.y), self.radius, 1)

    def update_physics(self, dt):
        if self.dragging:
            return

        self.dy += GRAVITY * dt
        self.y += self.dy * PTM * dt
        self.x += self.dx * PTM * dt

    def update_state(self, cur_pos, dt):
        cur_x, cur_y = cur_pos

        if dt > 0:
            self.dx = (cur_x - self.pre_pos[0]) / (dt * PTM)
            self.dy = (cur_y - self.pre_pos[1]) / (dt * PTM)

        self.x = cur_x
        self.y = cur_y
        self.pre_pos = cur_pos

    def check_collision(self, wall):
        if self.dragging:
            return

        ball_surface = self.y + self.radius

        if (ball_surface >= wall.rect.top and
            self.y - self.radius < wall.rect.bottom and
            self.x + self.radius >= wall.rect.left and
            self.x - self.radius <= wall.rect.right):

            if self.dy > 0:
                self.y = wall.rect.top - self.radius
                self.dy = -self.dy * 0.7


class Wall():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw_wall(self):
        pygame.draw.rect(window, (192, 192, 192), self.rect)
        pygame.draw.rect(window, (0, 0, 0), self.rect, 1)

    
def simulate_ball(balls, wall, dt):
    for ball in balls:
        ball.draw_balls()
        ball.check_collision(wall)
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

    wall = Wall(200, 500, 600, 40)

    balls = []
    active_ball = None

    while run:
        dt = clock.tick(FPS)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    ball = Balls(pos[0], pos[1], 40)
                    balls.append(ball)
                    active_ball = ball

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    active_ball.update_state(event.pos, dt)
                    active_ball.dragging = False
                    active_ball = None
                

        window.fill((255, 255, 255))
        draw_grid()

        wall.draw_wall()

        simulate_ball(balls, wall, dt)
        if active_ball:
            active_ball.update_state(pygame.mouse.get_pos(), dt)

        pygame.display.update()

        if not run:
            print("Exiting...")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main(window)