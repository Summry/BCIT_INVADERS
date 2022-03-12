import pygame
import time
import random

WIN_WIDTH = 1000
WIN_HEIGHT = 700
MAIN_WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load("images/space-background.png"), (WIN_WIDTH, WIN_HEIGHT))

BOSS1 = pygame.image.load("images/ben_boss.png")
BOSS2 = pygame.image.load("images/ben_spiderman.png")
ENEMY = pygame.image.load("images/sfu_enemy.png")

SHIP = pygame.image.load("images/bcit_ship.png")

pygame.display.set_caption("BCIT Invaders")

def redraw():
        MAIN_WINDOW.blit(SPACE_BACKGROUND, (0, 0))
        MAIN_WINDOW.blit(BOSS1, (50, 50))

        pygame.display.update()

def game():
    play = True
    frames = 60
    clock = pygame.time.Clock()

    while play:
        clock.tick(frames)
        redraw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

def main():
    game()

if __name__ == "__main__":
    main()