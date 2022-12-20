import pygame
import sys
from pygame.locals import *     # used for keys and events
from levels import world
from art import draw_tile

# Game set up
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
window_width = 1200
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Object Platformer')
icon = pygame.Surface((20, 20))
pygame.display.set_icon(icon)

# initializing font for later use
pygame.font.init()
font = pygame.font.SysFont('arial', 40)

# used for get FPS
tick = pygame.time.Clock()

# list of entities to track them all
entities = []

# takes input of (value, [minimum, maximum]) to clamp.
def clamp(value, val_range):
    if value < val_range[0]:    return val_range[0]
    if value > val_range[1]:    return val_range[1]
    return value

class Entity(object):
    def __init__(self, x, y, width, height, color, type):
        self.rect = pygame.Rect(x, y, width, height)
        entities.append(self)
        self.color = color
        self.type = type
    def delete_self(self):
        entities.remove(self)
        del self 
    def draw(self, x_displacement, y_displacement):
        new_rect = pygame.Rect(self.rect.x - x_displacement, self.rect.y - y_displacement, 
            self.rect.width, self.rect.height)
        if new_rect.colliderect(pygame.Rect(0, 0, 1200, 600)):          # if on screen, draws
            if self.type == "Platform":
                draw_tile(window, new_rect.x, new_rect.y, self.color)
            else:
                pygame.draw.rect(window, self.color, new_rect)

class Platform(Entity):
    def __init__(self, x, y, color):
        super().__init__(x, y, 30, 30, color, "Platform")

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, (0, 0, 255), "Player")
        self.y_vel = 0
        self.x_vel = 0

        self.x_dir = 0
        self.dash_counter = 0

        self.on_ground = False
        self.previously_jumping = False
        self.double_jump = False
        self.double_jump_counter = 0
        
        self.pos_upon_reset = (x, y)
        self.ask_to_advance_level = False

        # used for tracer
        self.previous_positions = [(x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), 
        (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), 
        (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), 
        (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y), (x, y)]

    def move(self):
        key = pygame.key.get_pressed()
        if key[K_LEFT] or key[K_a]:
            self.x_vel -= 1
            self.x_dir = -15
        if key[K_RIGHT] or key[K_d]:
            self.x_vel += 1
            self.x_dir = 15
        if key[K_r]:
            self.reset_pos()

        if self.x_vel > 0:                          # friction
            self.x_vel -= 0.5
        elif self.x_vel < 0:
            self.x_vel += 0.5
        if self.x_vel > 8:                          # extra friction
            self.x_vel -= 0.5
        elif self.x_vel < -8:
            self.x_vel += 0.5
        if self.x_vel > 12:                         # extra extra friction
            self.x_vel -= 0.5
        elif self.x_vel < -12:
            self.x_vel += 0.5
        self.y_vel = clamp(self.y_vel, (-14, 14))   # y-terminal velocity

        if key[K_SPACE] and self.dash_counter <= 0:
            self.x_vel += self.x_dir
            self.dash_counter = 60

        if self.dash_counter > 0:
            self.dash_counter -= 1

        # jumping
        if (key[K_UP] or key[K_w]) and not self.previously_jumping:
            if self.on_ground:
                self.y_vel = -10
            elif self.double_jump and self.double_jump_counter > 5:
                self.y_vel = -10
                self.double_jump = False
        
        if key[K_UP] or key[K_w]:          # setting this frame's values for next frame
            self.previously_jumping = True
        else:
            self.previously_jumping = False

        if not self.on_ground:          # gravity
            self.y_vel += 0.3
            self.double_jump_counter += 1
            if key[K_DOWN] or key[K_s]:
                self.y_vel += 0.7
                
        self.on_ground = False  # assumes you aren't on the ground until later proven wrong
        
        self.collide(0, self.y_vel)          # separate collisions for x and y
        self.collide(self.x_vel, 0)

        self.previous_positions.append((self.rect.x, self.rect.y))  # adding previous position
        average_x = (self.rect.x + self.previous_positions[-1][0])/2        # getting an in-between frame
        average_y = (self.rect.y + self.previous_positions[-1][1])/2
        self.previous_positions.append((average_x, average_y))      # adding it
        del self.previous_positions[0]  # removing old frames
        del self.previous_positions[0]

    def collide(self, x, y):
        self.rect.y += y
        self.rect.x += x

        ground_touched_list = []
        for ent in entities:
            if ent.type == "Platform":
                if self.rect.colliderect(ent.rect):
                    
                    if ent.color == "Grass" or ent.color == "Dirt":     # does collisions with these walls
                        if x > 0:
                            self.rect.right = ent.rect.left
                            self.x_vel = 0
                        elif x < 0:
                            self.rect.left = ent.rect.right
                            self.x_vel = 0
                        if y > 0:
                            self.rect.bottom = ent.rect.top
                            self.y_vel = 0
                        elif y < 0:
                            self.rect.top = ent.rect.bottom
                        ground_touched_list.append("Dirt")
                    
                    else:                   # appends other things to the list to deal with later
                        ground_touched_list.append(ent.color)
                        if ent.color == "Bomb":
                            ground_touched_list.append(ent.rect.center)
                
                # if you are touching the top of grass/dirt, then you are considered on the ground.
                if (ent.color == "Grass" or ent.color == "Dirt") and self.rect.bottom == ent.rect.top and \
                        self.rect.left in range (ent.rect.left - self.rect.width, ent.rect.right):
                    self.on_ground = True
                    self.double_jump_counter = 0
                    self.double_jump = True

        # if you touched the ground, it overrides everything else
        if ground_touched_list.count("Dirt") == 0:

            if ground_touched_list.count("Trampoline") > 0:
                if -2 < self.y_vel > 2:  self.y_vel *= -1
                self.y_vel -= 1.5

            elif ground_touched_list.count("Side Trampoline") > 0:
                if x > 0:  # if you were moving right,
                    self.x_vel = -30
                if x < 0:  # if you were moving left,
                    self.x_vel = 30
                self.y_vel -= 4 
            
            elif ground_touched_list.count("Bomb") > 0:
                for value in ground_touched_list:
                    if type(value) == tuple:                      # bombs add another value, a tuple, including 
                        x_diff = self.rect.centerx - value[0]     #   their coords. a bit jank, but the cleanest
                        y_diff = self.rect.centery - value[1]     #   implementation with the current system
                        total_diff = (abs(x_diff) + abs(y_diff))  #   i could find

                        x_vector = x_diff / total_diff
                        y_vector = y_diff / total_diff

                        self.x_vel = int(x_vector * 50)
                        self.y_vel = int(y_vector * 100)
                        break

            elif ground_touched_list.count("Exit") > 0:
                self.ask_to_advance_level = True

            else:   # if you only touched lava, lava triggers
                if ground_touched_list.count("Lava") > 0:
                        self.reset_pos()
                
            
    def reset_pos(self):
        self.rect.x = self.pos_upon_reset[0]
        self.rect.y = self.pos_upon_reset[1]
        self.x_vel = 0
        self.y_vel = 0


def generate_level(level, player):
    # making a list of all platforms, then deleting them
    to_del = [ent for ent in entities if ent.type == "Platform"]
    for thing_to_del in to_del:
        thing_to_del.delete_self()
    
    # adding new platforms
    x = 0
    y = 0
    for row in level:
        for value in row:
            if value == "G":
                Platform(x, y, "Grass")
            if value == "D":
                Platform(x, y, "Dirt")
            if value == "T":
                Platform(x, y, "Trampoline")
            if value == "t":
                Platform(x, y, "Side Trampoline")
            if value == "B":
                Platform(x, y, "Bomb")
            if value == "L":
                Platform(x, y, "Lava")
            if value == "E":
                Platform(x, y, "Exit")
            if value == "R":
                player.pos_upon_reset = (x+5, y+10)
            x += 30
        x = 0
        y += 30

def max_camera_values(level):
    # starts values at 0 and adds 30 (platform height and width) for each additional platform there is 
    #       going right/down after the regular size of one screen (40 width, 20 height)
    max_length = 0
    for row in level:
        max_length = max(len(row), max_length)
    max_length = (max_length - 40) * 30
    max_height = (len(level) - 20) * 30
    return max_length, max_height

def main():
    # define
    player = Player(40, 550)
    
    level = 0
    generate_level(world[level], player)
    max_length, max_height = max_camera_values(world[level])
    player.reset_pos()

    previous_backspace = False
    show_FPS = False
    FPS_list = [60, 60, 60, 60]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        window.fill((0, 0, 0))

        # moving player
        player.move()

        # camera things
        x_distance = player.rect.x - 570    # finding how much displacement is needed to center player
        y_distance = player.rect.y - 300
        x_displacement = clamp(x_distance, (0, max_length)) # clamping the displacement so it doesn't show off-stage
        y_displacement = clamp(y_distance, (0, max_height))

        # drawing the entities
        for ent in entities:
            ent.draw(x_displacement, y_displacement)
        player.draw(x_displacement, y_displacement)     # drawing player again to make sure it's on top
        
        # drawing the tracer
        s = pygame.Surface((20, 20))
        for tracer in player.previous_positions:
            s.fill((0, 0, 255))
            s.set_alpha(player.previous_positions.index(tracer)/3)    # alpha based on index
            window.blit(s, (tracer[0] - x_displacement, tracer[1] - y_displacement))

        # going to next level
        if player.ask_to_advance_level:
            level += 1
            generate_level(world[level], player)
            max_length, max_height = max_camera_values(world[level])
            player.ask_to_advance_level = False
            player.reset_pos()
        
        if pygame.key.get_pressed()[K_BACKSPACE]:
            if previous_backspace == False:
                if show_FPS:      
                    show_FPS = False
                else:
                    show_FPS = True
            previous_backspace = True
        else:
            previous_backspace = False

        tick.tick()                                 # doing this calculation even when not using it so that
        FPS_list.append(int(tick.get_fps()))        # the FPS displayed when it is shown is more accurate
        del FPS_list[0]
        average_FPS = sum(FPS_list) / len(FPS_list)

        if show_FPS:
            if average_FPS < 15:
                color = (255, 0, 0)
            elif average_FPS < 30:
                color = (255, 255, 0)
            else:
                color = (255, 255, 255)
            window.blit(font.render(f"FPS: {average_FPS}", True, color), pygame.Rect(1000, 2, 0, 0))

        # making game run
        fpsClock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()
