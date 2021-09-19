import pygame
import os
import random
import csv
import button
import pyautogui
import webbrowser
import time

pygame.init()

FULL_SCREEN_WIDTH = 1080
FULL_SCREEN_HEIGHT = 1920
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
programIcon = pygame.image.load('img/favicon.png')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(programIcon)
pygame.display.set_caption('Zombioo')
pygame.mouse.set_visible(1)

# FPS
clock = pygame.time.Clock()
FPS = 85

# VAR
GRAVITY = 0.50
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 22
MAX_LEVELS = 6
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False


# PLAYER VAR
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False
molotov = False
molotov_thrown = False



# IMAGES
start_img = pygame.image.load('img/btn/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/btn/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/btn/restart_btn.png').convert_alpha()
menubg = pygame.image.load('img/background/menuzombioo.png').convert_alpha()

#KEYBOARD
Wkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/W_Key_Light.png').convert_alpha()
Akey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/A_Key_Light.png').convert_alpha()
Dkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/D_Key_Light.png').convert_alpha()
Qkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/Q_Key_Light.png').convert_alpha()
ESCkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/Esc_Key_Light.png').convert_alpha()
SPkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/Spacelarge_Key_Light.png').convert_alpha()
Mkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/M_Key_Light.png').convert_alpha()
Ukey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/U_Key_Light.png').convert_alpha()
Fkey = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/F_Key_Light.png').convert_alpha()
F5key = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/F5_Key_Light.png').convert_alpha()
F4key = pygame.image.load('img/icons/keyboard/Keyboard & Mouse/Light/F4_Key_Light.png').convert_alpha()

# BACKGROUND IMAGES
pine1_img = pygame.image.load(
    'img/background/2_background_NEST/2_game_background.png').convert_alpha()
pine2_img = pygame.image.load(
    'img/background/2_background_NEST/2_game_background.png').convert_alpha()
mountain_img = pygame.image.load('img/background/2_background_NEST/2_game_background.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()
headhp = pygame.image.load('img/player/headHP.png').convert_alpha()
headdeadhp = pygame.image.load('img/player/headdeadHP.png').convert_alpha()
# TILES ETC
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

bullet_img = pygame.image.load('img/icons/ammo.png').convert_alpha()
bullet_zombie = pygame.image.load('img/icons/bulletzombie.png').convert_alpha

grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
molotov_img = pygame.image.load('img/icons/molotov.png').convert_alpha() 

health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
molotov_box_img = pygame.image.load('img/icons/molotov_box.png').convert_alpha()
item_boxes = {
    'Health'	: health_box_img,
    'Ammo'		: ammo_box_img,
    'Grenade'	: grenade_box_img,
    'Molotov'   :molotov_box_img
}

# COLORS
BG = (81, 6, 13)
RED = (176, 8, 12)
WHITE = (255, 255, 255)
GREEN = (26, 110, 15)
BLACK = (0, 0, 0)

#MUSIC
menumusic = pygame.mixer.music.load('audio/THEME.wav')
pygame.mixer.music.play(0)
SHOOT_SOUND = pygame.mixer.Sound('audio/shot.mp3')
SHOOT_SOUND.set_volume(0.6)

RELOAD = pygame.mixer.Sound('audio/Reloading.mp3')
RELOAD.set_volume(1)

GRENADESOUND = pygame.mixer.Sound('audio/grenade.mp3')
GRENADESOUND.set_volume(1)

MOLOTOVSOUND = pygame.mixer.Sound('audio/molotov.wav')
MOLOTOVSOUND.set_volume(1)

MOLOTOVBR = pygame.mixer.Sound('audio/molotovbr.wav')
MOLOTOVBR.set_volume(3)

PICK = pygame.mixer.Sound('audio/grenadepick.mp3')
PICK.set_volume(2)

PICKHEALTH = pygame.mixer.Sound('audio/pills.mp3')
PICKHEALTH.set_volume(2)

GRUNTING = pygame.mixer.Sound('audio/Grunting.mp3')
GRUNTING.set_volume(2)

ZOMBIEATTACK = pygame.mixer.Sound('audio/zombieattack.mp3')
ZOMBIEATTACK.set_volume(20)

MENUSELECT = pygame.mixer.Sound('audio/menuselect.mp3')
MENUSELECT.set_volume(9)

NEXTLEVEL = pygame.mixer.Sound('audio/nextlevel.mp3')
NEXTLEVEL.set_volume(9)

JUMP = pygame.mixer.Sound('audio/jump.mp3')
JUMP.set_volume(2)

GAMEOVER = pygame.mixer.Sound('audio/gameover.wav')
GAMEOVER.set_volume(2)

SCREENSHOT = pygame.mixer.Sound('audio/takingphoto.wav')
GAMEOVER.set_volume(5)

# FONT
font = pygame.font.Font("font/Futurot.ttf", 21)
ver = pygame.font.Font("font/Futurot.ttf", 10)
zombiootitle = pygame.font.Font("font/Futurot.ttf", 90)
BTNtext = pygame.font.Font("font/Futurot.ttf", 50)
YOUDIED = pygame.font.Font("font/Futurot.ttf", 110)
JanKupczyk = pygame.font.Font("font/Futurot.ttf", 13)

pausetimerevent = pygame.USEREVENT + 1
paused = False

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6,
                                   SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7,
                                SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8,
                                SCREEN_HEIGHT - pine2_img.get_height()))


# LEVEL RESET
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    zombiebullet_group.empty()
    grenade_group.empty()
    molotov_group.empty()
    explosion_group.empty()
    moloexplosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # TILE2
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades, molotovs):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.molotovs = molotovs
        self.health = 140
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # AI VAR
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        # IDLE RUN JUMP DEATH FLIP
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # LIST
            temp_list = []
            # SUBFOLDER
            num_of_frames = len(os.listdir(
                f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0

        # Movment variables
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # JUMP
        if self.jump == True and self.in_air == False:
            JUMP.play()
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # GRAV
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # COLLISION
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True
            NEXTLEVEL.play()

        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.60 *
                                                 self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            SHOOT_SOUND.play()
            # AMMO
            self.ammo -= 1

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 400) == 1:
                self.update_action(0)  # IDLE
                self.idling = True
                self.idling_counter = 45
            if self.vision.colliderect(player.rect):
                self.update_action(0)  # IDLE
                #SHOOTING
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  # RUN
                    self.move_counter += 1
                    self.vision.center = (
                        self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        #SCROLLBG
        self.rect.x += screen_scroll

    def update_animation(self):
        ANIMATION_COOLDOWN = 90
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)
            

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(
                            img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  # create player
                        player = Soldier('player', x * TILE_SIZE,
                                         y * TILE_SIZE, 1.65, 5, 20, 5, 5)
                        health_bar = HealthBar(
                            10, 10, player.health, player.health)
                    elif tile == 16:  # create enemies
                        enemy = Soldier('enemy', x * TILE_SIZE,
                                        y * TILE_SIZE, 1.65, 2, 20, 0, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:  # create ammo box
                        item_box = ItemBox(
                            'Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:  # create grenade box
                        item_box = ItemBox(
                            'Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:  # create health box
                        item_box = ItemBox(
                            'Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:  # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                player.health += 20
                PICKHEALTH.play()
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 3
                RELOAD.play()
            elif self.item_type == 'Grenade':
                player.grenades += 1
                PICK.play()
            elif self.item_type == 'Molotov':
                player.molotovs += 1
                PICK.play()
            self.kill()


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))
        screen.blit(headhp, (-4, 2))
        screen.blit(update_fps(), (1050,5))
        draw_text('FPS', font, WHITE, 1000, 5)
        screen.blit(update_ms(), (70, 830))
        draw_text('TIME', font, WHITE, 5, 825)
        draw_text('Current build version V1.31 (release.19.09.2021)', ver, WHITE, 5, 853)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 12
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed) + screen_scroll
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= random.randint(60,140)
                    ZOMBIEATTACK.play()
                    self.kill()
                    
def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("white"))
	return fps_text

def update_ms():
    mss = str(pygame.time.get_ticks()/1000)
    mss_text = font.render(mss, 1, pygame.Color("white"))
    return mss_text

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 6
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # Check height
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        # GRENADE POS
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        # CD GRENADE TIMER
        self.timer -= 0.95
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 1.5)
            explosion_group.add(explosion)
            #DAMAGE
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 3 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 3:
                    enemy.health -= 1000
                    GRUNTING.play()

class Molotov(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 99
        self.vel_y = -10
        self.speed = 11
        self.image = molotov_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # Check height
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        # MOLOTOV POS
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        # CD MOLOTOV TIMER
        self.timer -= 2
        if self.timer <= 0:
            self.kill()
            moloexplosion = MoloExplosion(self.rect.x, self.rect.y, 1.5)
            moloexplosion_group.add(moloexplosion)
            #DAMAGE
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 25
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 4 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 4:
                    enemy.health -= 55
                    GRUNTING.play()
                    GRUNTING.play()
                    GRUNTING.play()

class MoloExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        MOLOTOVBR.play()
        for num in range(0, 4):
            img = pygame.image.load(
                f'img/moloexplosion/Molo_{num}.png').convert_alpha()
            img = pygame.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img), MOLOTOVSOUND.play()
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll

        MOLOEXPLOSION_SPEED = 23
        self.counter += 1

        if self.counter >= MOLOEXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index] 

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 7):
            img = pygame.image.load(
                f'img/explosion/Explosion_{num}.png').convert_alpha()
            img = pygame.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img), GRENADESOUND.play()
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll

        EXPLOSION_SPEED = 7
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

#TAKING SCREENSHOT
def takescreenshot(screen):
    time_ss = time.asctime(time.localtime(time.time()))
    time_ss = time_ss.replace(" ", "_")
    time_ss = time_ss.replace(":", ".")
    save_file_f = "screenshots/" + time_ss + ".png"
    pygame.image.save(screen, save_file_f)
    print("Taken screenshot: " + save_file_f) 

#BTNs
start_button = button.Button(
    SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110,
                            SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(
    SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

# SPRITES
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
zombiebullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
molotov_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
moloexplosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)


run = True
while run:

    clock.tick(FPS)

    if start_game == False:
        # MENU
        screen.blit(menubg, (0, 0))
        draw_text('ZOMBIOO', zombiootitle, WHITE, 308, 150)
        draw_text('CONTROL:', font, WHITE, 115, 380)
        draw_text('JUMP', font, WHITE, 190, 410)
        screen.blit(Wkey, (140, 395))
        draw_text('LEFT', font, WHITE, 55, 450)
        screen.blit(Dkey, (180, 435))
        draw_text('RIGHT', font, WHITE, 230, 450)
        screen.blit(Akey, (100, 435))
        draw_text('SHOOT', font, WHITE, 210, 490)
        screen.blit(SPkey, (125, 460))
        draw_text('NADE', font, WHITE, 55, 546)
        screen.blit(Qkey, (5, 530))
        draw_text('MUTE MUSIC', font, WHITE, 55, 586)
        screen.blit(Mkey, (5, 570))
        draw_text('UNMUTE MUSIC', font, WHITE, 55, 626)
        screen.blit(Ukey, (5, 610))
        draw_text('FULLSCREEN', font, WHITE, 55, 666)
        screen.blit(Fkey, (5, 650))
        draw_text('VISIT WEBSITE', font, WHITE, 55, 706)
        screen.blit(F4key, (5, 690))
        draw_text('TAKE SCREENSHOT', font, WHITE, 55, 746)
        screen.blit(F5key, (5, 730))
        draw_text('EXIT', font, WHITE, 55, 810)
        screen.blit(ESCkey, (5, 795))
        draw_text('©2021 Jan Kupczyk', JanKupczyk, WHITE, 905, 845)
        draw_text('Current build version V1.31 (release.19.09.2021)', ver, WHITE, 5, 853)
        # BTNS MENU
        if start_button.draw(screen):
            start_game = True
            MENUSELECT.play()
            pygame.mixer.music.stop()
        if exit_button.draw(screen):
            MENUSELECT.play()
            run = False
    else:
        draw_bg()
        world.draw()
        health_bar.draw(player.health)
        draw_text('HEALTH', font, WHITE, 46, 12)
        draw_text('AMMO: ', font, WHITE, 10, 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + (x * 10), 40))
        draw_text('GRENADES: ', font, WHITE, 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 61))
        draw_text('MOLOTOVS: ', font, WHITE, 10, 85)
        for x in range(player.molotovs):
            screen.blit(molotov_img, (140 + (x * 15), 75))

        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        zombiebullet_group.update()
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        moloexplosion_group.update()
        molotov_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        zombiebullet_group.draw(screen)
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        moloexplosion_group.draw(screen)
        molotov_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        if player.alive:
            if shoot:
                player.shoot()
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                                  player.rect.top, player.direction)
                grenade_group.add(grenade)
                player.grenades -= 1
                grenade_thrown = True
            elif molotov and molotov_thrown == False and player.molotovs > 0:
                molotov = Molotov(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                                  player.rect.top, player.direction)
                molotov_group.add(molotov)
                player.molotovs -= 1
                molotov_thrown = True
            if player.in_air:
                player.update_action(2)  # 2: jump
            elif moving_left or moving_right:
                player.update_action(1)  # 1: run
            else:
                player.update_action(0)  # 0: idle
            screen_scroll, level_complete = player.move(
                moving_left, moving_right)
            bg_scroll -= screen_scroll
            # LEVEL COMPLETE
            if level_complete:
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    # CREATING WORLD
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
        else:
            screen_scroll = 0
            draw_text('YOU DIED!', YOUDIED, WHITE, 260, 150), GAMEOVER.stop()
            screen.blit(headdeadhp, (-4, 2))
            if restart_button.draw(screen):
                MENUSELECT.play()
                bg_scroll = 0
                world_data = reset_level()
                #CREATE WORLD DATA
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, health_bar = world.process_data(world_data)

    for event in pygame.event.get():
        # QUIT GAME
        if event.type == pygame.QUIT:
            MENUSELECT.play()
            run = False
        # KEYBOARD SETT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_e:
                molotov = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
                MENUSELECT.play()
            if event.key == pygame.K_m:
                pygame.mixer.music.pause()
                MENUSELECT.play()
            if event.key == pygame.K_u:
                pygame.mixer.music.unpause()
                MENUSELECT.play()
            if event.key == pygame.K_f:
                SCREEN_WIDTH = 1080
                SCREEN_HEIGHT = 1920
                pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                MENUSELECT.play()
            if event.key == pygame.K_F4:
                webbrowser.open('https://github.com/jankupczyk/Zombioo#readme')
                MENUSELECT.play()
            if event.key == pygame.K_F5:
                takescreenshot(screen)
                MENUSELECT.play() 
                SCREENSHOT.play()

        # KEYBOARDS SETT2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
            if event.key == pygame.K_e:
                molotov = False
                molotov_thrown = False


    pygame.display.update()

pygame.quit()

# AUTHOR: Jan Kupczyk