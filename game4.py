import pygame
import random
import math

pygame.init()


WIDTH, HEIGHT = 800, 600
FPS = 60

PLAYER_SIZE = 18
NPC_RADIUS = 16
BULLET_RADIUS = 4

PLAYER_SPEED = 4
ROT_SPEED = 5
BULLET_SPEED = 9

BG_COLOR = (25, 25, 25)
GRID_COLOR = (40, 40, 40)
PLAYER_COLOR = (0, 220, 120)
NPC_COLOR = (220, 60, 60)
BULLET_COLOR = (255, 220, 100)

font = pygame.font.SysFont(None, 24)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Assignment")
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0

    def update(self, keys):
        if keys[pygame.K_a]:
            self.angle -= ROT_SPEED
        if keys[pygame.K_d]:
            self.angle += ROT_SPEED
        if keys[pygame.K_w]:
            self.x += math.cos(math.radians(self.angle)) * PLAYER_SPEED
            self.y += math.sin(math.radians(self.angle)) * PLAYER_SPEED

    def draw(self):
        front = (
            self.x + math.cos(math.radians(self.angle)) * PLAYER_SIZE,
            self.y + math.sin(math.radians(self.angle)) * PLAYER_SIZE
        )
        left = (
            self.x + math.cos(math.radians(self.angle + 140)) * PLAYER_SIZE,
            self.y + math.sin(math.radians(self.angle + 140)) * PLAYER_SIZE
        )
        right = (
            self.x + math.cos(math.radians(self.angle - 140)) * PLAYER_SIZE,
            self.y + math.sin(math.radians(self.angle - 140)) * PLAYER_SIZE
        )

        pygame.draw.polygon(screen, PLAYER_COLOR, [front, left, right])

        # crosshair
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(front[0]), int(front[1])), 4, 1)


class NPC:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.choice([-2, 2])
        self.vy = random.choice([-2, 2])

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.x <= 0 or self.x >= WIDTH:
            self.vx *= -1
        if self.y <= 0 or self.y >= HEIGHT:
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(screen, NPC_COLOR, (int(self.x), int(self.y)), NPC_RADIUS)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), NPC_RADIUS, 2)


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.vx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.vy = math.sin(math.radians(angle)) * BULLET_SPEED
        self.trail = []
        self.life = 120


    def update(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)

        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def out_of_screen(self):
        return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT

    def draw(self):
        for i, pos in enumerate(self.trail):
            r = max(1, BULLET_RADIUS - i)
        if self.life > 0:
              pygame.draw.circle(screen, (255, 255, 255),
                    (int(self.x), int(self.y)), BULLET_RADIUS + 2)
        self.life -= 1

player = Player(WIDTH // 2, HEIGHT // 2)
npcs = []
bullets = []

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            npcs.append(NPC(mx, my))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.x, player.y, player.angle))

    keys = pygame.key.get_pressed()
    player.update(keys)

    for npc in npcs:
        npc.update()

    for bullet in bullets[:]:
        bullet.update()
        if bullet.out_of_screen():
            bullets.remove(bullet)

    for bullet in bullets[:]:
        for npc in npcs[:]:
            if math.hypot(bullet.x - npc.x, bullet.y - npc.y) < NPC_RADIUS:
                bullets.remove(bullet)
                npcs.remove(npc)
                break

    screen.fill(BG_COLOR)
    draw_grid()

    player.draw()
    npc_text = font.render(f"NPCs: {len(npcs)}", True, (200, 200, 200))
    screen.blit(npc_text, (10, 10))

    for npc in npcs:
        npc.draw()
    for bullet in bullets:
        bullet.draw()

    pygame.display.flip()

pygame.quit()
