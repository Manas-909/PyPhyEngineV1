import pygame
import os
import math
import sys

pygame.init()
pygame.display.set_caption("PyPhy Engine")

WIDTH, HEIGHT = 1000, 600
PTM = 100
GRAVITY = 9.8
FPS = 120

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

    def ball_collision(self, ball):
        if self.dragging or ball.dragging or ball is self:
            return

        distance = math.sqrt((self.x - ball.x)**2 + (self.y - ball.y)**2)

        if distance <= self.radius + ball.radius:
            overlap_ball = ((self.radius + ball.radius) - distance) / 2
            
            ball_nx = (self.x - ball.x) / distance
            ball_ny = (self.y - ball.y) / distance
            
            relative_nx = (self.dx - ball.dx) / 2
            relative_ny = (self.dy - ball.dy) / 2
            
            ball_nv = relative_nx * ball_nx + relative_ny * ball_ny
            
            if ball_nv < 0:
                elasticity = 0.6
                impulse = -(1 + elasticity) * ball_nv / 2
            
                self.dx += impulse * ball_nx
                self.dy += impulse * ball_ny
            
                ball.dx -= impulse * ball_nx
                ball.dy -= impulse * ball_ny
            
            self.x += ball_nx * overlap_ball
            self.y += ball_ny * overlap_ball
            
            ball.x -= ball_nx * overlap_ball
            ball.y -= ball_ny * overlap_ball


    def check_collision(self, wall):
        if self.dragging:
            return

        closest_x = max(wall.rect.left, min(self.x, wall.rect.right))
        closest_y = max(wall.rect.top, min(self.y, wall.rect.bottom))

        dis_x = self.x - closest_x
        dis_y = self.y - closest_y

        distance = math.sqrt(dis_x**2 + dis_y**2)

        if distance <= self.radius:
            if distance > 0:
                normal_x = dis_x / distance
                normal_y = dis_y / distance

                overlap = self.radius - distance

            else:
                left = self.x - wall.rect.left
                right = wall.rect.right - self.x
                top = self.y - wall.rect.top
                bottom = wall.rect.bottom - self.y

                nearest = min(left, right, top, bottom)

                if nearest == left:
                    normal_x, normal_y = -1, 0
                elif nearest == right:
                    normal_x, normal_y = 1, 0
                elif nearest == top:
                    normal_x, normal_y = 0, -1
                elif nearest == bottom:
                    normal_x, normal_y = 0, 1

                overlap = self.radius + nearest

            self.x += normal_x * overlap
            self.y += normal_y * overlap

            normal_v = self.dx * normal_x + self.dy * normal_y

            if normal_v < 0:
                restitution = 0.7

                self.dx -= (1 + restitution) * normal_v * normal_x
                self.dy -= (1 + restitution) * normal_v * normal_y


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

    
def simulate_ball(balls, walls, dt):
    for ball in balls:
        ball.update_physics(dt)

        for wall in walls:
            ball.check_collision(wall)

    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].ball_collision(balls[j])

    for ball in balls:
        ball.draw_balls()


def draw_grid():
    grid_size = 30

    for x in range(0, WIDTH, grid_size):
        pygame.draw.line(window, (211, 211, 211), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, grid_size):
        pygame.draw.line(window, (211, 211, 211), (0, y), (WIDTH, y))


def main(window):
    clock = pygame.time.Clock()
    run = True

    wall1 = Wall(200, 500, 600, 40)
    wall2 = Wall(200, 250, 40, 250)
    wall3 = Wall(760, 250, 40, 250)

    balls = []
    walls = [wall1, wall2, wall3]
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

        for wall in walls:
            wall.draw_wall()

        simulate_ball(balls, walls, dt)
        if active_ball:
            active_ball.update_state(pygame.mouse.get_pos(), dt)

        pygame.display.update()

        if not run:
            print("Exiting...")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main(window)