import pygame
import time
import random
pygame.font.init()
pygame.init()
game_font = pygame.font.SysFont("verdana", 30)
lose_font = pygame.font.SysFont("verdana", 20)

WIN_WIDTH = 1000
WIN_HEIGHT = 700
MAIN_WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load("images/space-background.png"), (WIN_WIDTH, WIN_HEIGHT))
START_MENU = pygame.image.load("images/menu_title.png")
START = pygame.image.load("images/start_button.png")

BOSS1 = pygame.image.load("images/ben_boss.png")
BOSS2 = pygame.image.load("images/ben_spiderman.png")
ENEMY = pygame.image.load("images/enemy.png")
ENEMY_BULLET = pygame.image.load("images/enemybullet.png")

BCIT_SHIP = pygame.image.load("images/bcit_ship.png")
BULLET = pygame.image.load("images/bullet.png")

pygame.display.set_caption("BCIT INVADERS")

class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def reach_end(self, height):
        return not(self.y <= height and self.y >= 0)

    def impact(self, object):
        return ship_impact(self, object)

class Enemy_bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def reach_end(self, height):
        return not(self.y <= height and self.y >= 0)

    def impact(self, object):
        return ship_impact(self, object)

class ship:
    COOLDOWN = 30
    
    def __init__(self, x, y, health=10):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.bullet_img = None
        self.bullets = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def move_bullet(self, vel, object):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.reach_end(WIN_HEIGHT):
                self.bullets.remove(bullet)
            elif bullet.impact(object):
                object.health -= 1
                self.bullets.remove(bullet)
    
    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

    def get_height(self):
        return self.ship_img.get_height()
    
    def get_width(self):
        return self.ship_img.get_width()
    
    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))

class Player(ship):
    def __init__(self, x, y, health=10):
        super().__init__(x, y, health)
        self.ship_img = BCIT_SHIP
        self.bullet_img = BULLET
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_bullet(self, vel, objects):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.reach_end(WIN_HEIGHT):
                self.bullets.remove(bullet)
            else:
                for object in objects:
                    if bullet.impact(object):
                        objects.remove(object)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(ship):
    def __init__(self, x,  y, health=10):
        super().__init__(x, y, health)
        self.ship_img = ENEMY
        self.bullet_img = ENEMY_BULLET
        self.mask = pygame.mask.from_surface(self.ship_img)

    def movement(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            enemybullet = Enemy_bullet(self.x-20, self.y, self.bullet_img)
            self.bullets.append(enemybullet)
            self.cool_down_counter = 1

def ship_impact(object1, object2):
    set_x = object2.x - object1.x
    set_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask, (set_x, set_y)) != None

def game():
    pygame.mixer.music.load("song/Game_Music.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    lives = 3
    round = 1
    frames = 60
    clock = pygame.time.Clock()
    play = True

    player_ship_velocity = 7
    bullet_speed = 7

    listenemies = []
    round_length = 2
    enemy_velocity = 1

    player_ship = Player(300, 630)

    lose = False
    lose_count = 0

    def gamescreen():
        MAIN_WINDOW.blit(SPACE_BACKGROUND, (0, 0))

        lives_num = game_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        round_num = game_font.render(f"Round: {round}", 1, (255, 255, 255))

        MAIN_WINDOW.blit(lives_num, (10, 10))
        MAIN_WINDOW.blit(round_num, (WIN_WIDTH - round_num.get_width() - 10, 10))

        player_ship.draw(MAIN_WINDOW)

        for enemy in listenemies:
            enemy.draw(MAIN_WINDOW)

        if lose:
            lose_text = lose_font.render("Read the textbook", 1, (255, 255, 255))
            MAIN_WINDOW.blit(lose_text, (WIN_WIDTH / 2 - lose_text.get_width()/2, 350))

        pygame.display.update()

    while play:
        clock.tick(frames)
        gamescreen()

        if lives == 0 or player_ship.health <= 0:
            lose = True
            lose_count += 1
        
        if lose:
            if lose_count > 5:
                play = False
            else:
                continue
        
        if len(listenemies) == 0:
            round += 1
            round_length += 2
            for count in range(round_length):
                enemy = Enemy(random.randrange(50, WIN_WIDTH-100), random.randrange(-1000, -100))
                listenemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        mkey = pygame.key.get_pressed()
        if mkey[pygame.K_LEFT] and player_ship.x - player_ship_velocity > 0:
            player_ship.x -= player_ship_velocity
        if mkey[pygame.K_UP] and player_ship.y - player_ship_velocity > 0:
            player_ship.y -= player_ship_velocity
        if mkey[pygame.K_DOWN] and player_ship.y + player_ship_velocity + player_ship.get_height() + 15 < WIN_HEIGHT:
            player_ship.y += player_ship_velocity
        if mkey[pygame.K_RIGHT] and player_ship.x + player_ship_velocity + player_ship.get_width() < WIN_WIDTH:
            player_ship.x += player_ship_velocity
        if mkey[pygame.K_SPACE]:
            player_ship.shoot()

        for enemy in listenemies[:]:
            enemy.movement(enemy_velocity)
            enemy.move_bullet(bullet_speed, player_ship)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if ship_impact(player_ship, enemy):
                player_ship.health -= 1
                listenemies.remove(enemy)
            elif enemy.y + enemy.get_height() > WIN_HEIGHT:
                lives -= 1
                listenemies.remove(enemy)

        player_ship.move_bullet(-bullet_speed, listenemies)
    
    pygame.mixer.music.stop()
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.load('song/Menu_Music.wav')
    pygame.mixer.music.play(-1)

def mainmenu():
    mainscreen = True
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.load('song/Menu_Music.wav')
    pygame.mixer.music.play(-1)
    while mainscreen:
        MAIN_WINDOW.blit(SPACE_BACKGROUND, (0, 0))
        MAIN_WINDOW.blit(START_MENU, (10, 100))
        MAIN_WINDOW.blit(START, (WIN_WIDTH / 2 - 385, 600))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainscreen = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()
                game()
    pygame.quit()

def main():
    mainmenu()

if __name__ == "__main__":
    main()