import pygame
import sys
import os
import random
from pygame.locals import *

# Game set up
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
window_width = 1200
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Boss Rush')
icon = pygame.Surface((20, 20))
pygame.display.set_icon(icon)

pygame.font.init()
font = pygame.font.SysFont('arial', 20)

# lists
world = []
bullets = []

# level, used for many things
stage = 0

# platform colors
gray = (120, 120, 120)
yellow = (160, 160, 0)
# other colors are listed as regular RGB, hope you can read that


class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(50, 550, 20, 20)
        
        # player velocities, used for acceleration
        self.x_velocity = 0
        self.y_velocity = 0
        
        # counters to reset bullets and dodging
        self.bullet_counter = 0
        self.dodge_counter = 0
        
        # last direction faced, used for dashing
        self.x_dir = 0
        
        # counters to see if double jump is valid and how long the player has been off the ground for
        self.double_jump = False
        self.double_jump_counter = 0
        
        # seeing if holding jump button, used to make sure you press it instead of holding
        self.previous_w_values = [False, False, False, False, False]
        
        # if the exit doors (yellow) are opened
        self.exit_open = False

    def move(self):
        # movement
        key = pygame.key.get_pressed()
        x = y = 0
        if key[K_d]:
            x = 5
            self.x_dir = 8
        if key[K_a]:
            x = -5
            self.x_dir = -8

        # if space is hit, set velocity based on most recent direction player was looking
        # can only do once every 40 frames
        if key[K_SPACE] and self.dodge_counter >= 40:
            self.x_velocity = self.x_dir*2.5
            self.dodge_counter = 0
        if self.dodge_counter < 40:
            self.dodge_counter += 1

        # can only press jump, not hold.
        # checks previous 5 values instead of just the previous because gravity is a bit poorly coded.
        if self.previous_w_values.count(True) < 5 and key[K_w]:
            y = -12
        if key[K_w]:
            self.previous_w_values.append(True)
        else:
            self.previous_w_values.append(False)
        del self.previous_w_values[0]

        # calling for other functions of movement and shooting.
        self.move_y(y)
        self.move_x(x)
        self.shoot()

    def move_x(self, x):
        # acceleration is only used for dodging
        if self.x_velocity > 0:         # reducing velocity over time
            self.x_velocity -= 1
        if self.x_velocity < 0:
            self.x_velocity += 1
        x += self.x_velocity            # changing x by velocity
        
        self.rect.x += x                # move by x, which is the sum of dashing + regular movement

        for platform in world:                              # platform collision detection
            if self.rect.colliderect(platform[0]):
                if platform[1] == gray:                     # hits gray platforms
                    if x > 0:
                        self.rect.right = platform[0].left
                    if x < 0:
                        self.rect.left = platform[0].right
                if platform[1] == yellow:
                    if self.exit_open:                      # if exit is open, can leave through yellow
                        self.rect.x = 50
                        self.rect.y = 550
                        self.x_velocity = 0
                        self.y_velocity = 0
                        set_level()
                    else:                                   # otherwise, yellow is the same as gray
                        if x > 0:
                            self.rect.right = platform[0].left
                        if x < 0:
                            self.rect.left = platform[0].right
                        window.blit(font.render("Exit is closed.", False, (255, 0, 0)),
                                    (window_width - 120, window_height - 29))

        pygame.draw.rect(window, (0, 0, 255), self.rect)    # draws player

    def move_y(self, y):
        on_ground = False                   # assumes you are in free-fall
        self.rect.y += self.y_velocity      # moves you by velocity

        for platform in world:                              # collision checks
            if self.rect.colliderect(platform[0]) and platform[1] == gray:            # collides if gray
                if self.y_velocity > 0:
                    self.rect.bottom = platform[0].top
                    on_ground = True                        # if you are touching the ground, these 2 are set as true.
                    self.double_jump = True                 # allows you to jump and resets double jump ability.
                    self.double_jump_counter = 0            # sets counter for double jump to 0, used to prevent
                if self.y_velocity < 0:                     # both jumps from immediately occuring back-to-back.
                    self.rect.top = platform[0].bottom

        if on_ground:                                           # can only jump if on the ground
            self.y_velocity = y
        if not on_ground:                                       # if not on the ground, gravity applies
            self.y_velocity += 0.6                              # and double-jump counter starts
            self.double_jump_counter += 1
        if y == -12 and self.double_jump and self.double_jump_counter > 5:     # can only double jump if holding space
            self.y_velocity = y                                                # and a double jump is available and
            self.double_jump = False                                           # the counter has finished

        if abs(self.y_velocity) > 20:           # terminal velocity
            self.y_velocity *= 0.8

    def shoot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()       # vector for mouse
        x_diff = mouse_x - (self.rect.x + 5)
        y_diff = mouse_y - (self.rect.y + 5)

        key = pygame.key.get_pressed()              # if keys are pressed, key vectors are prioritzed instead
        if key[pygame.K_UP]:
            y_diff = -1
            x_diff = 0
        if key[pygame.K_DOWN]:
            y_diff = 1
            x_diff = 0
        if key[pygame.K_LEFT]:
            x_diff = -1
            y_diff = 0                      # apologies about how long it is, I couldn't find a smaller method
            if key[pygame.K_UP]:
                y_diff = -1
            if key[pygame.K_DOWN]:
                y_diff = 1
        if key[pygame.K_RIGHT]:
            x_diff = 1
            y_diff = 0
            if key[pygame.K_UP]:
                y_diff = -1
            if key[pygame.K_DOWN]:
                y_diff = 1

        # vector calculation decides where it goes
        if not (abs(x_diff) + abs(y_diff)) == 0:                # first making sure no divide by 0 error
            x_vector = x_diff / (abs(x_diff) + abs(y_diff))     # getting how much of x is in x + y
            y_vector = y_diff / (abs(x_diff) + abs(y_diff))     # getting how much of y is in x + y

            valid_key_pressed = key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_UP] or key[pygame.K_DOWN] or \
                pygame.mouse.get_pressed()[0]

            # only fires if a key is pressed and 30 ticks of the counter have passed
            if valid_key_pressed and self.bullet_counter >= 30:
                # bullet direction is set based on vectors
                Bullet(self.rect.x + 5, self.rect.y + 5, x_vector * 30, y_vector * 30, "player", 10, 0)
                self.bullet_counter = 0

        # ticking counter
        if self.bullet_counter < 30:
            self.bullet_counter += 1

    # returns rect, used for collision with bullets
    def location(self):
        return self.rect

    # used to input if the exit is opened, done in the main loop
    def exit(self, status):
        self.exit_open = status


player = Player()  # defining player. used for enemies, so it needs to be done here instead of in main.


class Platform(object):
    # used to add a platform to the list of platforms (world).
    def __init__(self, pos, color):
        self.rect = pygame.Rect(pos[0], pos[1], 30, 30)
        world.append((self.rect, color))


class Bullet(object):
    # used to add a bullet to the list of bullets
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity, owner, size, gravity):
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        bullets.append([self.rect, x_velocity, y_velocity, owner, gravity])


class Enemy(object):
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        # y velocity used for acceleration (mainly due to gravity)
        self.y_velocity = 0
        self.x_velocity = 0

        # pattern counter
        self.counter = 0

        # healths
        self.enemy_health = 10
        self.total_health = 10
        self.enemy_name = ""
        self.color = (0, 0, 0)

        self.is_bird = False

        # random number is used solely for the guardian fight, needed to define it here.
        self.random_number = 0

        # used to see if the level has changed.
        self.previous_level_value = 0

    def move(self):
        # sets initial values based on stage

        # only sets the initial values if the stage has changed, which it checks by seeing
        # if the stage is the same as what it was last frame.
        if self.previous_level_value != stage:
            if stage == 1:
                self.rect = pygame.Rect(1050, 400, 30, 30)
                self.enemy_health = self.total_health = 1
                self.enemy_name = "Target, The Overcoming"
                self.color = (200, 0, 0)

            if stage == 2:
                self.enemy_health = self.total_health = 20
                self.rect = pygame.Rect(1050, 400, 50, 50)
                self.enemy_name = "Archer, Sniper of Many"
                self.color = (0, 80, 0)

            if stage == 3:
                self.enemy_health = self.total_health = 10
                self.rect = pygame.Rect(1050, 400, 50, 50)
                self.enemy_name = "Bouncer, Crusher of Plains"
                self.color = (100, 80, 0)

            if stage == 4:
                self.enemy_health = self.total_health = 15
                self.rect = pygame.Rect(1050, 100, 80, 80)
                self.enemy_name = "Birdie, Goliath of the Skies"
                self.color = (50, 50, 50)
                self.is_bird = True

            if stage == 5:
                self.enemy_health = self.total_health = 15
                self.rect = pygame.Rect(1050, 100, 40, 40)
                self.enemy_name = "Waver, Force of the Ocean"
                self.color = (5, 5, 50)

            if stage == 6:
                self.enemy_health = self.total_health = 15
                self.rect = pygame.Rect(581, 100, 40, 60)
                self.enemy_name = "Trapped Worm, Despair of the Desert"
                self.color = (80, 80, 0)

            if stage == 7:
                self.enemy_health = self.total_health = 5
                self.rect = pygame.Rect(1100, 50, 40, 40)
                self.enemy_name = "Assassin, Soul Reaper of Cities"
                self.color = (40, 40, 40)

            if stage == 8:
                self.enemy_health = self.total_health = 10
                self.rect = pygame.Rect(600, 100, 40, 40)
                self.enemy_name = "Sorceress, Plague of Humanity"
                self.color = (80, 40, 120)

            if stage == 9:
                self.enemy_health = self.total_health = 30
                self.rect = pygame.Rect(1050, 100, 40, 40)
                self.enemy_name = "Guardian, Mountain Defender"
                self.color = (200, 200, 200)

            if stage == 10:
                self.enemy_health = self.total_health = 15
                self.rect = pygame.Rect(1050, 100, 40, 40)
                self.enemy_name = "Sprayer, Lord of the Land"
                self.color = (20, 120, 20)

            if stage == 11:
                self.enemy_health = self.total_health = 30
                self.rect = pygame.Rect(581, 100, 40, 40)
                self.enemy_name = "Firework, Hope of Harm"
                self.color = (120, 120, 60)

            if stage == 12:
                self.enemy_health = self.total_health = 40
                self.rect = pygame.Rect(1050, 100, 40, 40)
                self.enemy_name = "Demon, Finale of the Ensemble"
                self.color = (180, 20, 180)
            self.counter = 0                    # resets counter
        self.previous_level_value = stage       # sets the stage value here to be used next frame

        # if it is alive, all patterns and the like start
        if self.enemy_health > 0:
            self.is_bird = False    # assumes is not a bird, meaning the enemy follows normal y movements.
            x = y = 0               # assumes that no movement is happening.

            if stage == 1:    # target
                # shows instructions, doesn't move or shoot.
                window.blit(font.render("WASD to move. You can double jump. Space to dash. ESC to pause. "
                                        "Click or arrow keys to shoot.", False, (255, 255, 255)), (5, 5))

            if stage == 2:    # archer
                if self.counter < 50:
                    pass
                if 50 <= self.counter < 150:            # oscillates between moving left and right
                    x -= 3
                if 150 <= self.counter < 250:
                    x += 3
                if self.counter % 50 == 0:              # shoots every 50 frames
                    self.shoot_at_player(30, 10, 10)
                if self.counter > 250:
                    self.counter = 50

            if stage == 3:    # bouncer
                if self.counter <= 50:
                    pass
                if 50 < self.counter <= 250:            # jumping left
                    x = -3.1
                    y = -10
                if 250 < self.counter <= 450:           # jumping right
                    x = 3.1
                    y = -10
                if self.rect.bottom == 541:            # shoots if near ground, bullets come from the bottom
                    Bullet(self.rect.x + 15, self.rect.bottom, 1, -1, "enemy", 20, 0)
                    Bullet(self.rect.x + 15, self.rect.bottom, 0, -1, "enemy", 20, 0)
                    Bullet(self.rect.x + 15, self.rect.bottom, -1, -1, "enemy", 20, 0)
                if self.counter > 450:
                    self.counter = 50

            if stage == 4:    # birdie
                self.is_bird = True                 # ignores regular y-movement due to being bird
                self.y_velocity += 0.2
                self.rect.y += self.y_velocity      # constantly moves downwards,
                if self.rect.y > 150:               # but gets pushed back up if it gets too low
                    self.rect.y = 150
                    self.y_velocity = -5
                if self.rect.centerx > player.location().x + 10:   # moves x towards player based on center locations
                    self.rect.x -= 5
                if self.rect.centerx < player.location().x + 10 and self.rect.x < 1090:
                    self.rect.x += 5
                if self.counter == 20:                  # shoots big bullets downwards
                    Bullet(self.rect.x + 20, self.rect.bottom, 0, 5, "enemy", 40, 0)
                if self.counter > 20:                   # short restart as only used for bullets
                    self.counter = 0

            if stage == 5:    # waver
                if 2 <= self.counter <= 50:
                    x = 1
                if 50 < self.counter <= 155:            # moves left
                    x = -3
                if 250 < self.counter <= 350:           # pauses for 95 frames before moving left again
                    x = -3
                if 445 < self.counter <= 545:           # pauses for 95 frames then moves right
                    x = 3
                if 640 < self.counter <= 745:           # pauses for 95 frames then moves right
                    x = 3
                if self.counter == 747:                 # fine-tuning position
                    self.rect.x = 1095
                if 85 <= self.counter < 90 or 480 <= self.counter < 485:    # jumps to get on to platform
                    y = -15
                if 165 <= self.counter < 170 or 560 <= self.counter < 565:    # jumps for shooting at center
                    y = -15
                if 370 <= self.counter < 375 or 765 <= self.counter < 770:    # jumps for shooting at edges
                    y = -15
                if 175 <= self.counter < 205 or 570 <= self.counter < 590 \
                        or 380 <= self.counter < 400 or 775 <= self.counter < 795:  # bullets near peek of jumps
                    if self.counter % 2 == 0:                                       # fires every other tick
                        Bullet(self.rect.x + 15, self.rect.bottom, 0, 2, "enemy", 10, 0)
                        Bullet(self.rect.x + 25, self.rect.bottom, 2, 2, "enemy", 10, 0)
                        Bullet(self.rect.x + 5, self.rect.bottom, -2, 2, "enemy", 10, 0)
                        Bullet(self.rect.x + 20, self.rect.bottom, 1, 2, "enemy", 10, 0)
                        Bullet(self.rect.x + 10, self.rect.bottom, -1, 2, "enemy", 10, 0)
                if self.counter > 840:
                    self.counter = 50

            if stage == 6:    # worm
                if self.counter <= 50:
                    pass
                # every other frame, shoots one of 3 patterns as seen below.
                if self.counter % 2 == 0:
                    if 50 < self.counter < 58:
                        Bullet(self.rect.x + 15, self.rect.top, -4, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, -3, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, -2, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, -1, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, 1, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, 2, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, 3, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, 4, -15, "enemy", 10, 0.3)
                    if 200 < self.counter < 216:
                        Bullet(self.rect.x + 15, self.rect.top, 1, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, 2, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, 3, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, 4, -15, "enemy", 10, 0.3)
                    if 400 < self.counter < 416:
                        Bullet(self.rect.x + 15, self.rect.top, -1, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, -2, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, -3, -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, -4, -15, "enemy", 10, 0.3)
                    if 600 < self.counter < 632:
                        Bullet(self.rect.x + 15, self.rect.top, random.randint(-5, 5), -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, random.randint(-5, 5), -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, random.randint(-5, 5), -15, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 15, self.rect.top, random.randint(-5, 5), -15, "enemy", 10, 0.3)
                if self.counter > 800:
                    self.counter = 50

            if stage == 7:    # assassin
                if self.counter <= 50:
                    pass
                if 50 < self.counter <= 155:            # moves left
                    x = -3
                if 250 < self.counter <= 350:           # pauses for 95 frames before moving left again
                    x = -3
                if 445 < self.counter <= 545:           # pauses for 95 frames then moves right
                    x = 3
                if 640 < self.counter <= 745:           # pauses for 95 frames then moves right
                    x = 3
                if self.counter == 747:                 # fine-tuning position
                    self.rect.x = 1100
                if 55 <= self.counter < 120 or 255 <= self.counter < 320:    # jumps to get on to platform
                    y = -15
                if 450 <= self.counter < 525 or 645 <= self.counter < 710:    # jumps to get on to platform
                    y = -15
                if 165 <= self.counter < 170 or 560 <= self.counter < 565:    # jumps for shooting at center
                    y = -15
                if 370 <= self.counter < 375 or 765 <= self.counter < 770:    # jumps for shooting at edges
                    y = -15
                if self.counter % 2 == 0:  # fires every other tick
                    if 175 <= self.counter < 205 or 570 <= self.counter < 590:  # bullets near peak of jumps
                        Bullet(self.rect.x + 25, self.rect.bottom, 4, 0, "enemy", 15, 0.5)
                        Bullet(self.rect.x + 5, self.rect.bottom, -4, 0, "enemy", 15, 0.5)
                        Bullet(self.rect.x + 25, self.rect.bottom, 6, 0, "enemy", 15, 0.5)
                        Bullet(self.rect.x + 5, self.rect.bottom, -6, 0, "enemy", 15, 0.5)
                        Bullet(self.rect.x + 25, self.rect.bottom, 8, 0, "enemy", 15, 0.5)
                        Bullet(self.rect.x + 5, self.rect.bottom, -8, 0, "enemy", 15, 0.5)
                    if 380 <= self.counter < 400:
                        Bullet(self.rect.x + 25, self.rect.bottom, 2, 0, "enemy", 15, 0.5)
                        Bullet(self.rect.x + 25, self.rect.bottom, 4, 0, "enemy", 15, 0.5)
                        Bullet(self.rect.x + 25, self.rect.bottom, 6, 0, "enemy", 15, 0.5)
                        Bullet(self.rect.x + 25, self.rect.bottom, 8, 0, "enemy", 15, 0.5)
                    if 775 <= self.counter < 795:
                        Bullet(self.rect.x + 5, self.rect.bottom, -2, 0, "enemy", 15, 0.5)
                        Bullet(self.rect.x + 5, self.rect.bottom, -4, 0, "enemy", 15, 0.5)
                        Bullet(self.rect.x + 5, self.rect.bottom, -6, 0, "enemy", 15, 0.5)
                        Bullet(self.rect.x + 5, self.rect.bottom, -8, 0, "enemy", 15, 0.5)
                if self.counter > 840:
                    self.counter = 50

            if stage == 8:    # sorceress
                self.is_bird = True                 # ignores regular y-movement
                self.rect.y += self.y_velocity
                if self.counter == 1:
                    self.rect.y = 100               # x and y move based on position to create
                    self.rect.x = 600               # an elliptical movement pattern
                    self.y_velocity = 0
                if 300 <= self.rect.y < 600:
                    self.y_velocity -= 0.1
                    x += 5
                if 0 <= self.rect.y < 300:
                    self.y_velocity += 0.1
                    x -= 5
                if self.counter == 60:                  # shoots tracking bullets of various speed and size
                    self.shoot_at_player(40, 5, 8)
                    self.shoot_at_player(40, 10, 5)
                if self.counter > 60:
                    self.counter = 10
                if self.rect.y < 0 or self.rect.y > 600 or self.rect.x > window_width or self.rect.x < 0:
                    self.counter = 0

            if stage == 9:  # lord
                if self.counter == 60:                              # picks movement pattern from random int
                    self.random_number = random.randint(-6, -3)
                if self.counter > 50:
                    pass
                if 80 <= self.counter < 160:                    # walks towards destination based on random int
                    x = self.random_number
                if 280 <= self.counter < 400:                   # jumps back based on random int, goes a bit extra
                    if self.rect.x < 1050:                      # can't go too extra as only moves if x < 1050
                        y = -12
                        x = -self.random_number
                if 200 <= self.counter < 220 and self.counter % 2 == 0:         # shoots upon reaching destination
                    Bullet(self.rect.x + 25, self.rect.top, 2, -10, "enemy", 8, 0.3)
                    Bullet(self.rect.x + 5, self.rect.top, -2, -10, "enemy", 8, 0.3)
                    Bullet(self.rect.x + 25, self.rect.top, 4, -10, "enemy", 8, 0.3)
                    Bullet(self.rect.x + 5, self.rect.top, -4, -10, "enemy", 8, 0.3)
                    Bullet(self.rect.x + 25, self.rect.top, 6, -10, "enemy", 8, 0.3)
                    Bullet(self.rect.x + 5, self.rect.top, -6, -10, "enemy", 8, 0.3)
                    Bullet(self.rect.x + 25, self.rect.top, 8, -10, "enemy", 8, 0.3)
                    Bullet(self.rect.x + 5, self.rect.top, -8, -10, "enemy", 8, 0.3)
                if self.counter > 500:
                    self.counter = 50

            if stage == 10:  # sprayer
                if self.counter <= 50:
                    pass
                player_x = player.location()[0]
                distance = player_x - 1050
                if self.counter % 2 == 0:               # shoots based on player distance and a random int
                    if 50 < self.counter < 80:
                        Bullet(self.rect.x + 15, self.rect.top, distance/random.randint(50, 100), -10, "enemy", 10, 0.3)
                if self.counter > 120:
                    self.counter = 50

            if stage == 11:  # firework
                if self.counter <= 50:
                    pass
                if 100 <= self.counter < 105 or 200 <= self.counter < 205:  # jumps
                    y = -15
                if 300 <= self.counter < 305 or 400 <= self.counter < 405:  # jumps
                    y = -15
                if 115 <= self.counter < 145:
                    pass
                if 215 <= self.counter < 245:                           # fires upwards with gravity
                    Bullet(self.rect.x + 15, self.rect.top, random.randint(-6, 6), -10, "enemy", 10, 0.3)
                    Bullet(self.rect.x + 15, self.rect.top, random.randint(-6, 6), -10, "enemy", 10, 0.3)
                if 310 <= self.counter < 345:                           # fires at player
                    self.shoot_at_player(40, 5, 10)
                    self.shoot_at_player(40, 5, 5)
                if 410 <= self.counter < 445:                           # fires downwards, no gravity
                    Bullet(self.rect.x + 15, self.rect.bottom, random.randint(-6, 6), 2, "enemy", 10, 0)
                    Bullet(self.rect.x + 15, self.rect.bottom, random.randint(-6, 6), 2, "enemy", 10, 0)
                if self.counter > 600:
                    self.counter = 50

            if stage == 12:    # demon
                if self.counter <= 50:
                    pass
                if 50 < self.counter <= 120:        # moves left
                    x = -7
                    if self.counter % 8 == 0:                                   # firing when jumping left
                        Bullet(self.rect.x + 15, self.rect.bottom, 0, 2, "enemy", 10, 0)
                        Bullet(self.rect.x + 25, self.rect.bottom, 3, 2, "enemy", 10, 0)
                        Bullet(self.rect.x + 5, self.rect.bottom, -3, 2, "enemy", 10, 0)
                if 350 < self.counter <= 420:       # moves right
                    x = 7
                    if self.counter % 8 == 0:                                   # firing when jumping right
                        Bullet(self.rect.x + 15, self.rect.bottom, 0, -5, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 25, self.rect.bottom, 3, -5, "enemy", 10, 0.3)
                        Bullet(self.rect.x + 5, self.rect.bottom, -3, -5, "enemy", 10, 0.3)
                if 48 <= self.counter < 55 or 348 <= self.counter < 355:     # jumps to move left or right
                    y = -55
                if 225 <= self.counter < 230 or 570 <= self.counter < 575:    # jumps for shooting at edges
                    y = -15
                if 245 <= self.counter < 265 or 590 <= self.counter < 610:  # firing at edges
                    self.shoot_at_player(40, 5, 20)
                    self.shoot_at_player(40, 5, 10)
                if self.counter > 700:                  # counter and position reset
                    self.counter = 50
                    self.rect.x = 1050

            # ticking counter, moving as per provided x and y from pattern
            self.counter += 1
            self.move_y(y)
            self.move_x(x)

        else:
            # if dead, puts the rect somewhere off-screen.
            # can't just delete it or anything since the collision detection would still try to happen and crash.
            self.rect.x = -100
            self.rect.y = -100
            self.counter = 0

    def move_x(self, x):
        self.x_velocity = x
        if self.x_velocity > 0:
            self.x_velocity -= 1
        if self.x_velocity < 0:
            self.x_velocity += 1
        x += self.x_velocity
        self.rect.x += x
        for platform in world:                                      # collision
            if self.rect.colliderect(platform[0]):
                if x > 0:
                    self.rect.right = platform[0].left
                if x < 0:
                    self.rect.left = platform[0].right
        pygame.draw.rect(window, self.color, self.rect)             # drawing

    def move_y(self, y):
        if not self.is_bird:                                        # only moves by y if not a bird.
            on_ground = False                                       # rest is the same as the player, except
            self.rect.y += self.y_velocity                          # enemies don't have double jumps.
            for platform in world:
                if self.rect.colliderect(platform[0]):
                    if self.y_velocity > 0:
                        self.rect.bottom = platform[0].top
                        on_ground = True
                    if self.y_velocity < 0:
                        self.rect.top = platform[0].bottom
            if on_ground:
                self.y_velocity = y
            if not on_ground:
                self.y_velocity += 0.6
            if abs(self.y_velocity) > 20:
                self.y_velocity *= 0.8

    # used for convenience to get bullets to shoot towards players so that I don't have to do all the vector work
    # every time i want a bullet to fire at the player
    def shoot_at_player(self, enemy_size, bullet_size, bullet_speed):
        # basically the same as it was for players
        player_x = player.location().x
        player_y = player.location().y
        x_diff = player_x - self.rect.x
        y_diff = player_y - self.rect.y
        if not (abs(x_diff) + abs(y_diff)) == 0:
            x_vector = x_diff / (abs(x_diff) + abs(y_diff))
            y_vector = y_diff / (abs(x_diff) + abs(y_diff))
            Bullet(self.rect.x + enemy_size/2 + bullet_size/2, self.rect.y + bullet_size/2 + enemy_size/2, x_vector *
                   bullet_speed, y_vector * bullet_speed, "enemy", bullet_size, 0)

    def took_damage(self):
        # used when doing bullet collisions to input a decrease in enemy health
        self.enemy_health -= 1

    def location(self):
        # used for bullet collisions
        return self.rect

    def name(self):
        # used for boss health bar later
        return self.enemy_name

    def current_enemy_health(self):
        # used for boss health bar later and for seeing if the exit should be open
        return self.enemy_health

    def total_enemy_health(self):
        # used for boss health bar later
        return self.total_health


def level_create(level):
    # function used whenever a new level is set
    global world
    world = []      # first resets world, then rebuilds it
    x = y = 0
    for row in level:
        for value in row:
            if value == "W":
                Platform((x, y), gray)
            if value == "E":
                Platform((x, y), yellow)
            x += 30
        y += 30
        x = 0


def set_level():
    # makes world
    global stage, bullets
    bullets = []
    stage += 1
    if stage == 1:
        platforms = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      E",
            "W                                      E",
            "W                         WWWWWWWWWWWWWW",
            "W                                      W",
            "W                                      W",
            "W          W                           W",
            "W          W                           W",
            "W          W                           W",
            "W          W                           W",
            "W          W                           W",
            "W          W                           W",
            "W          W                           W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
        level_create(platforms)
    if stage == 2 or stage == 3 or stage == 4 or stage == 8 or stage == 10 or stage == 11 or stage == 12:
        platforms = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      E",
            "W                                      E",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
        level_create(platforms)
    if stage == 5:
        platforms = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W              WWWWWWWWWW              W",
            "W              WWWWWWWWWW              W",
            "W              WWWWWWWWWW              W",
            "W              WWWWWWWWWW              W",
            "W              WWWWWWWWWW              E",
            "W              WWWWWWWWWW              E",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
        level_create(platforms)
    if stage == 6:
        platforms = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W               WW    WW               W",
            "W              WWW    WWW              W",
            "W             WWWWW  WWWWW             W",
            "W           WWWWWWW  WWWWWWW           W",
            "W        WWWWWWWWWW  WWWWWWWWWW        E",
            "W     WWWWWWWWWWWWW  WWWWWWWWWWWWW     E",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
        level_create(platforms)
    if stage == 7:
        platforms = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W         WW                WW         W",
            "W                                      W",
            "WWWW              WWW               WWWW",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      E",
            "W                                      E",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
        level_create(platforms)
    if stage == 9:
        platforms = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      E",
            "W                                      E",
            "W                        WWWWWWWWWWWWWWW",
            "W                        WWWWWWWWWWWWWWW",
            "W                   WWWWWWWWWWWWWWWWWWWW",
            "W                   WWWWWWWWWWWWWWWWWWWW",
            "W              WWWWWWWWWWWWWWWWWWWWWWWWW",
            "W              WWWWWWWWWWWWWWWWWWWWWWWWW",
            "W         WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W         WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W    WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W    WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
        level_create(platforms)
    if stage == 13:  # blank level in case the player somehow manages to get to level 13
        platforms = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "W                                      W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
        level_create(platforms)


def main():
    # basic definitions
    enemy = Enemy(-100, -100, 20)   # defining enemy, starts off-screen
    player_health = 16              # starting health
    i_frames = 0                    # used for player invincibility frames in collisions
    timer = 0                       # used to time how long the player took
    time_passed = ""                # used for displaying time
    set_level()                     # creates a level and changes the stage

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        window.fill((0, 0, 0))

        # drawing world
        for platform in world:
            pygame.draw.rect(window, (platform[1]), platform[0])

        # player and enemey movement
        player.move()
        enemy.move()

        # all bullet stuff happens here
        for bullet in bullets:

            dead = False                        # bullet set to be alive

            bullet[0].x += bullet[1]            # change bullet x pos by x velocity
            bullet[0].y += bullet[2]            # change bullet y pos by y velocity
            bullet[2] = bullet[2] + bullet[4]   # change y velocity by y acceleration

            # throughout, it is always checked if a bullet is alive before removing it from the list
            # to avoid double-removing something, which would result in a crash

            for platform in world:
                if bullet[0].colliderect(platform[0]) and not dead:     # if bullet is hitting a wall,
                    bullets.remove(bullet)                              # delete the bullet
                    dead = True
            if not dead:
                if not 0 < bullet[0].y < window_height + 10:        # if bullet is off-screen,
                    bullets.remove(bullet)                          # delete the bullet
                elif not 0 < bullet[0].x < window_width + 10:
                    bullets.remove(bullet)

            # if it was shot by the player, collision is done to check to see if it hit the enemy
            if not dead and bullet[3] == "player":
                if bullet[0].colliderect(enemy.location()):
                    enemy.took_damage()
                    bullets.remove(bullet)
                else:
                    pygame.draw.rect(window, (200, 200, 255), bullet[0])

            # if it was shot by the enemy, collision sees if it hit the player
            if not dead and bullet[3] == "enemy":
                if bullet[0].colliderect(player.location()) and not i_frames > 0:
                    player_health -= 1
                    bullets.remove(bullet)
                    i_frames = 120      # if hit, get invincibility frames
                else:
                    pygame.draw.rect(window, (255, 255, 255), bullet[0])

        # if the player is colliding with the enemy, the player loses health
        if player.location().colliderect(enemy.location()) and not i_frames > 0:
            player_health -= 1
            i_frames = 120              # if hit, get invincibility frames

        # reduction of invincibility frames
        if i_frames > 0:
            i_frames -= 1

        # showing player health bar
        window.blit(font.render(("Health: " + str(player_health)), False, (255, 255, 255)), (50, window_height - 28))
        player_bar = pygame.Rect(50, window_height-25, 100, 20)
        player_current_bar = pygame.Rect(50, window_height-25, 100*(player_health/16), 20)
        pygame.draw.rect(window, (200, 200, 255), player_bar)
        pygame.draw.rect(window, (150, 0, 0), player_current_bar)

        # boss health bar
        percent_health = enemy.current_enemy_health()/enemy.total_enemy_health()
        boss_bar = pygame.Rect(250, window_height-25, 650, 20)
        boss_current_bar = pygame.Rect(250, window_height-25, 650*percent_health, 20)
        pygame.draw.rect(window, (200, 200, 255), boss_bar)
        pygame.draw.rect(window, (150, 0, 0), boss_current_bar)
        if enemy.current_enemy_health() > 0:
            text = font.render(enemy.name(), False, (150, 100, 100))
            text_rect = text.get_rect(center=(575, 582))
            window.blit(text, text_rect)

        # if the enemy is dead, tell the player exits are open. otherwise assume they are closed.
        exit_status = False
        if enemy.current_enemy_health() <= 0:
            exit_status = True
        player.exit(exit_status)

        # pausing
        key = pygame.key.get_pressed()
        if key[K_ESCAPE]:
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                key = pygame.key.get_pressed()      # not sure why but it doesn't work if I don't define it again
                if key[K_p]:
                    break
                window.blit(font.render("Paused. Press P to unpause.", False, (255, 255, 255)), (50, 200))

                pygame.display.update()
        if stage >= 13:             # victory
            break
        if player_health <= 0:      # game over
            break

        timer += 1

        # showing time passed on the top-right,
        # doing this instead of importing time since it isn't much work to do so.
        time_passed = int(timer/60)
        minutes_passed = time_passed // 60      # getting minutes and seconds
        seconds_passed = time_passed % 60

        minutes_passed = str(minutes_passed)       # adding a zero to the start if needed
        if int(minutes_passed) < 10:
            minutes_passed = "0" + minutes_passed
        seconds_passed = str(seconds_passed)
        if int(seconds_passed) < 10:
            seconds_passed = "0" + seconds_passed

        time_passed = minutes_passed + ":" + seconds_passed     # displaying the time
        window.blit(font.render(str(time_passed), False, (255, 255, 255)), (1140, 4))

        # ticks at FPS, updates screen to show new drawings
        fpsClock.tick(FPS)
        pygame.display.update()

    # score calculations for time, health, boss, and total

    # colors for ranks
    f_color = (200, 0, 0)
    d_color = (200, 50, 50)
    c_color = (200, 100, 0)
    b_color = (100, 150, 0)
    a_color = (0, 240, 0)
    s_color = (240, 180, 0)
    ss_color = (240, 220, 0)
    sss_color = (255, 255, 0)

    # scoring. long because of needing to define boundaries, otherwise about as compressed as I could get it.
    score = 0
    time_text = "Time: F", f_color
    health_text = "Health: F", f_color
    boss_text = "Boss Completion: F", f_color
    rank_text = "Overall : F", f_color

    if timer < 14400:     # SSS - under 4 minutes
        score += 50000
        time_text = "Time: SSS", sss_color
    elif timer < 16200:   # SS - under 4.5 minutes
        score += 45000
        time_text = "Time: SS", ss_color
    elif timer < 18000:   # S - under 5 minutes
        score += 40000
        time_text = "Time: S", s_color
    elif timer < 21600:   # A - under 6 minutes
        score += 30000
        time_text = "Time: A", a_color
    elif timer < 28800:   # B - under 8 minutes
        score += 20000
        time_text = "Time: B", b_color
    elif timer < 36000:   # C - under 10 minutes
        score += 10000
        time_text = "Time: C", c_color
    elif timer < 54000:   # D - under 15 minutes
        score += 5000
        time_text = "Time: D", d_color

    if player_health == 16:        # SSS - full health
        score += 50000
        health_text = "Health: SSS", sss_color
    elif player_health == 15:      # SS - near-full health
        score += 45000
        health_text = "Health: SS", ss_color
    elif player_health >= 13:      # S - high health
        score += 40000
        health_text = "Health: S", s_color
    elif player_health >= 11:      # A - decently high health
        score += 30000
        health_text = "Health: A", a_color
    elif player_health >= 7:       # B - medium health
        score += 20000
        health_text = "Health: B", b_color
    elif player_health >= 4:       # C - medium-low health
        score += 10000
        health_text = "Health: C", c_color
    elif player_health >= 1:       # D - low health
        score += 5000
        health_text = "Health: D", d_color

    if stage >= 13:       # SSS - beat all bosses
        score += 50000
        boss_text = "Boss Completion: SSS", sss_color
    elif stage >= 12:     # SS - died to 12th (demon)
        score += 45000
        boss_text = "Boss Completion: SS", ss_color
    elif stage >= 11:     # S - died to 11th (firework)
        score += 40000
        boss_text = "Boss Completion: S", s_color
    elif stage >= 9:      # A - died to 9th or 10th boss (guardian/sprayer)
        score += 30000
        boss_text = "Boss Completion: A", a_color
    elif stage >= 8:      # B - died to 8th boss (sorceress)
        score += 20000
        boss_text = "Boss Completion: B", b_color
    elif stage >= 6:      # C - died to 6th or 7th boss (worm/assassin)
        score += 10000
        boss_text = "Boss Completion: C", c_color
    elif stage >= 4:      # D - died to 4th or 5th boss (birdie/waver)
        score += 5000
        boss_text = "Boss Completion: D", d_color

    if score == 150000:
        rank_text = "Overall : SSS", sss_color
    elif score >= 135000:
        rank_text = "Overall : SS", ss_color
    elif score >= 120000:
        rank_text = "Overall : S", s_color
    elif score >= 90000:
        rank_text = "Overall : A", a_color
    elif score >= 60000:
        rank_text = "Overall : B", b_color
    elif score >= 30000:
        rank_text = "Overall : C", c_color
    elif score >= 15000:
        rank_text = "Overall : D", d_color

    i = 0
    while i < 1:  # loop for drawing the end screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        window.fill((0, 0, 0))
        end_game_font = pygame.font.SysFont('arial', 40)
        if player_health <= 0:      # if you died before reaching the end, does the game-over.
            window.blit(end_game_font.render("You died.", False, (255, 255, 255)), (window_width / 2 - 100, 80))
        else:                       # if you didn't die, shows the victory screen.
            window.blit(end_game_font.render("You won!", False, (255, 255, 255)), (window_width / 2 - 100, 80))

        # showing score
        window.blit(end_game_font.render(("Score: "+str(score)), False, (255, 255, 255)), (window_width / 2 - 120, 150))

        # showing boss, time, and health ranks
        end_game_font = pygame.font.SysFont('arial', 30)
        window.blit(end_game_font.render(boss_text[0], False, boss_text[1]), (window_width / 2 - 130, 230))
        window.blit(end_game_font.render(time_text[0], False, time_text[1]), ((window_width / 2 - 130), 310))
        window.blit(end_game_font.render(health_text[0], False, health_text[1]), (window_width / 2 - 130, 270))

        # showing overall rank
        end_game_font = pygame.font.SysFont('arial', 40)
        window.blit(end_game_font.render(rank_text[0], False, rank_text[1]), (window_width / 2 - 90, 360))

        # showing time
        window.blit(font.render(str(time_passed), False, (255, 255, 255)), (1140, 4))

        # as it is a new loop, need to tick at FPS and update screen again.
        fpsClock.tick(FPS)
        pygame.display.update()


main()
