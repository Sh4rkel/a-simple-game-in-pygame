import pygame
import sys
import random
import numpy as np
from moviepy.editor import ImageSequenceClip

pygame.init()

screen_width, screen_height = 1200, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blocky Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

block_size = 50
block_x, block_y = screen_width // 2, screen_height // 2
block_speed = 5

collectible_size = 30
num_collectibles = 10
collectibles = [(random.randint(0, screen_width - collectible_size), random.randint(0, screen_height - collectible_size)) for _ in range(num_collectibles)]
collectible_speeds = [(random.choice([-3, 3]), random.choice([-3, 3])) for _ in range(num_collectibles)]

enemy_size = 50
num_enemies = 5
enemies = [(random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)) for _ in range(num_enemies)]
enemy_speeds = [(random.choice([-3, 3]), random.choice([-3, 3])) for _ in range(num_enemies)]

score = 0
font = pygame.font.SysFont(None, 36)

frames = []

def display_score(screen, score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def generate_collectibles():
    global collectibles, collectible_speeds
    collectibles = [(random.randint(0, screen_width - collectible_size), random.randint(0, screen_height - collectible_size)) for _ in range(num_collectibles)]
    collectible_speeds = [(random.choice([-3, 3]), random.choice([-3, 3])) for _ in range(num_collectibles)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        block_x -= block_speed
    if keys[pygame.K_RIGHT]:
        block_x += block_speed
    if keys[pygame.K_UP]:
        block_y -= block_speed
    if keys[pygame.K_DOWN]:
        block_y += block_speed

    block_x = max(0, min(screen_width - block_size, block_x))
    block_y = max(0, min(screen_height - block_size, block_y))

    for i in range(num_collectibles):
        collectible_x, collectible_y = collectibles[i]
        speed_x, speed_y = collectible_speeds[i]
        collectible_x += speed_x
        collectible_y += speed_y
        if collectible_x <= 0 or collectible_x >= screen_width - collectible_size:
            speed_x = -speed_x
        if collectible_y <= 0 or collectible_y >= screen_height - collectible_size:
            speed_y = -speed_y
        collectibles[i] = (collectible_x, collectible_y)
        collectible_speeds[i] = (speed_x, speed_y)

    for i in range(num_enemies):
        enemy_x, enemy_y = enemies[i]
        speed_x, speed_y = enemy_speeds[i]
        enemy_x += speed_x
        enemy_y += speed_y
        if enemy_x <= 0 or enemy_x >= screen_width - enemy_size:
            speed_x = -speed_x
        if enemy_y <= 0 or enemy_y >= screen_height - enemy_size:
            speed_y = -speed_y
        enemies[i] = (enemy_x, enemy_y)
        enemy_speeds[i] = (speed_x, speed_y)

    block_rect = pygame.Rect(block_x, block_y, block_size, block_size)
    for i, (collectible_x, collectible_y) in enumerate(collectibles):
        collectible_rect = pygame.Rect(collectible_x, collectible_y, collectible_size, collectible_size)
        if block_rect.colliderect(collectible_rect):
            score += 10
            block_size += 10
            block_speed += 1
            collectibles[i] = (random.randint(0, screen_width - collectible_size), random.randint(0, screen_height - collectible_size))

    for enemy_x, enemy_y in enemies:
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)
        if block_rect.colliderect(enemy_rect):
            running = False

    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (block_x, block_y, block_size, block_size))
    for collectible_x, collectible_y in collectibles:
        pygame.draw.rect(screen, GREEN, (collectible_x, collectible_y, collectible_size, collectible_size))
    for enemy_x, enemy_y in enemies:
        pygame.draw.rect(screen, BLUE, (enemy_x, enemy_y, enemy_size, enemy_size))
    display_score(screen, score)
    pygame.display.flip()

    # Save frame
    frame = pygame.surfarray.array3d(screen)
    frame = np.rot90(frame, 3)
    frames.append(frame)

    pygame.time.Clock().tick(30)

clip = ImageSequenceClip(frames, fps=30)
clip.write_videofile("game_recording.mp4", codec="libx264")

pygame.quit()
sys.exit()