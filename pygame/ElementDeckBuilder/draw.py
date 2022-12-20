import pygame
import random

pygame.font.init()
massive_font = pygame.font.SysFont('arial', 150)
big_font = pygame.font.SysFont('arial', 70)
font = pygame.font.SysFont('arial', 40)
medium_font = pygame.font.SysFont('arial', 30)
small_font = pygame.font.SysFont('arial', 25)
tiny_font = pygame.font.SysFont('arial', 15)

gold_particle_list = []

################# no drawing stuff yet, starts later.

def reset_gold_particle_list():
    global gold_particle_list
    gold_particle_list = []

element_list = (
#       element           price     description
        ("Air",             1,      "Nitrogen and oxygen among other gasses."),
        ("Earth",           1,      "Made up of minerals and matter in the ground."),
        ("Fire",            1,      "Product of combustion."),
        ("Water",           1,      "Life's basis."),
        ("Dust",            2,      "Various fine particles."),
        ("Energy",          2,      "Supposedly the ability to do work."),
        ("Clay",            2,      "Soil with ceramic properties."),
        ("Wind",            2,      "Air in motion."),
        ("Lava",            2,      "The molten form of rocks."),
        ("Cold",            2,      "A lack of heat."),
        ("Steam",           2,      "The gaseous form of water."),
        ("Stone",           2,      "A solid collection of minerals."),
        ("Carbon Dioxide",  2,      "A greenhouse gas made from combustion."),
        ("Metal",           3,      "Lustrous, ductile, conductive, malleable."),
        ("Ceramic",         3,      "A product of pottery."),
        ("Tornado",         3,      "Fast-spinning and destructive wind."),
        ("Electricity",     3,      "Formed from electric charges."),
        ("Sand",            3,      "Apparently course, rough, and irritating."),
        ("Ice",             3,      "Solid form of water."),
        ("Cloud",           3,      "Tiny and floating particles."),
        ("Mountain",        3,      "A big pile of ground."),
        ("Lake",            3,      "Water, but more of it."),
        ("Earthquake",      3,      "Moving ground."),
        ("Egg",             3,      "A shell containing life."),
        ("Ash",             3,      "Remains of the fuel of combustion."),
        ("Permafrost",      3,      "Frozen ground."),
        ("Light",           3,      "Illuminating radiation."),
        ("Tumbleweed",      3,      "A part of a plant that has detached and moved through wind."),
        ("Glassware",       4,      "Transparent and brittle."),
        ("Life",            4,      "The characteristic that differentiates the animate and inanimate."),
        ("Hurricane",       4,      "Spiral columns of hot and wet air."),
        ("Rain",            4,      "Falling clouds."),
        ("Volcano",         4,      "A mountain that can shoot lava."),
        ("Wave",            4,      "The ocean's preferred method of energy transfer."),
        ("Plants",          4,      "Generally photosynthesize."),
        ("Bird",            4,      "A feathered animal closely related to dinosaurs."),
        ("Fish",            4,      "Aquatic animals with gils."),
        ("House",           4,      "A nice place to live."),
        ("Landslide",       4,      "When gravity meets slopes."),
        ("Human",           4,      "Featherless biped."),
        ("Glacier",         4,      "Like ice, but denser."),
        ("Turtle",          4,      "Semi-aquatic omnivores with shells."),
        ("Seeds",           4,      "Like an egg, but for a plant."),
        ("Ice Brick",       4,      "Ice that has been turned into building material."),
        ("Ocean",           4,      "A big salty lake."),
        ("Sun",             4,      "An incredible source of illumination and energy."),
        ("Desert",          4,      "An ocean of sand that becomes delicious with another s."),
        ("Beast",           5,      "Fish who learnt to walk and developed lungs."),
        ("Sandstorm",       5,      "Wind with sand in it."),
        ("Cactus",          5,      "Like other plants, but stronger."),
        ("Alcohol",         5,      "Seems a bit dangerous to just leave here."),
        ("Cola",            5,      "Water with some spice to it."),
        ("Angler",          5,      "One who angles."),
        ("Miner",           5,      "Likely is also a crafter."),
        ("Blizzard",        5,      "The worst parts of snow and wind."),
        ("Duststorm",       5,      "Wind with dust in it."),
        ("Snow",            5,      "A mix between ice and powdered sugar."),
        ("Tsunami",         5,      "Strong waves that hold huge amounts of water."),
        ("Robot",           5,      "A programmable machine."),
        ("Island",          5,      "A lot of ground in the ocean."),
        ("Beach",           5,      "A coast with lots of tiny rocks."),
        ("Wood",            5,      "The stem of a tree."),
        ("Coal",            5,      "Rocks that burn well."),
        ("Oil",             5,      "A burnable liquid."),
        ("Natural Gas",     5,      "Like oil, but lighter."),
        ("Boat",            5,      "A means for land creatures to traverse water."),
        ("Pirate",          5,      "Someone who would download a car."),
        ("Will o' Wisp",    5,      "A ghost light that misleads travellers."),
        ("Penguin",         5,      "A flightless bird that lives in the cold."),
        ("Ice Wall",        5,      "A solid layer of ice brick that insulates quite well."),
        ("Tree",            5,      "Plants that are larger, stronger, and useful in data science."),
        ("Oasis",           5,      "A fertile part of land in an otherwise harsh landscape."),
        ("Circuit",         5,      "A programming chip that tastes quite bitter."),
        ("Gold",            6,      "Heavy, soft, and pretty."),
        ("Music",           6,      "Arranged sounds."),
        ("Thunder",         6,      "The power of Zeus."),
        ("Avalanche",       6,      "The mass-movement of snow."),
        ("Snowman",         6,      "A cute sculpture of snow."),
        ("AI",              6,      "The ability for a machine to act based on the environment."),
        ("Ice Building",    6,      "A entire structure composed of ice, fascinating."),
        ("Forest",          6,      "A terrain in which trees have decided to form their own society."),
        ("Swamp",           6,      "Marshy, tree-y, and bacteria-y."),
        ("Mangrove",        6,      "The trees have spread to the coasts."),
        ("Android",         7,      "An artifically-created humanoid."),
        ("Vocaloid",        7,      "A robot who loves to sing."),
        ("Hero",            7,      "A brave saviour with power, wisdom, and courage."),
        ("Angel",           7,      "A divine creature that should have many more eyes than depicted here."),
        ("Royalty",         7,      "A ruler given the divine right but sadly never the divine left."),
        ("Ice Mansion",     7,      "An expensive and quite cold place to live in."),
        ("Love",            8,      "Attraction from living beings."),
        ("Phoenix",         8,      "A legendary immortal bird made of fire."),
        ("Dragon",          8,      "A large, wise, and flying mythical creature."),
        ("Ice Palace",      8,      "A home to only the most extravagant."),
        ("World Tree",      8,      "The symbol of nature that brings life to all it knows."),
        ("Black Hole",      50,     "A dense mass that destroys the very fabric of reality."),
    )

def gold_from(element):
    if element == "Empty":
        return 0
    for item in element_list:
        if item[0] == element:
            return item[1]
    return 0                        # if can't be identified

def description_of(element):
    description = []
    for line in element_list:
        if line[0] == element:
            text = line[2]

            # wrap-text implementation
            # transforms the description into a list of each word
            words = []
            word = ""
            for letter in text:
                word += letter
                if letter == " " or letter == "." or letter == "," or letter == "!" \
                            or letter == "?" or letter == ":" or letter == ";":
                    words.append(word)
                    word = ""
            
            # turns the list of each word into a list of each line
            i = 0

            # keeps trying to add words so long as there are some in the list.
            while len(words) >= (i+1):
                
                current_line = []
                current_line_length = 0

                # keeps adding words, stops when it exceeds
                while current_line_length < 380 and len(words) >= (i+1): 
                    current_line.append(words[i])

                    current_line_length = 0
                    for a_word in current_line:
                        current_line_length += small_font.size(a_word)[0]
                    
                    i += 1
                
                # removes most recent word if exceeded and goes back a word for the next iteration
                if current_line_length >= 380:
                    i -= 1
                    del current_line[-1]

                # converts the list of words into one string and adds it it to the description
                sentence = ""
                for b_word in current_line:
                    sentence += b_word
                description.append(sentence)
            
            # returns description of list of strings, where each string is a line
            return description
    
    # if nothing is found, prints the element for bug-testing and gives error message in description.
    print(element)
    return ["This element is broken.", "Please inform the developer about this."]

def pick_for_shop(luck):
    # gives a random selection of items such that the sum of their golds per turn are equal to or less than luck
    # not perfect but this is one implementation

    shop_list = []
    i = 3               # used to make sure enough gold per turn remains to ensure elements of 1 gold can be added
    
    # repeats until 4 items are present
    while len(shop_list) < 4:

        # element stored as list to allow for gold per turn to be stored next to it
        element = ["Empty", luck]
        
        # keeps trying to find an element from the list that costs less than the maximum permitted
        while element[1] > (luck - i):

            # gets random element index, tries that element and element price
            rand = random.randint(0, len(element_list) - 1)
            element = [element_list[rand][0], element_list[rand][1]]

        # moves onto next element, subtracts 1 from i to accomodate for next element
        i -= 1

        # instead of removing from luck, adds more to i
        i += element[1]

        # adds element to list
        shop_list.append(element[0])

    return shop_list

################# drawing stuff starts from here

def colored_box(width, height, color = (255, 255, 0)):
    selected_box = pygame.Surface((width, height))      # making a surface to get a translucent rect
    selected_box.set_alpha(30)                          # alpha level
    selected_box.fill(color)                            # yellow by default
    return selected_box

def main_menu(window, mouse_touching_button):
    # rects of buttons
    rect = pygame.Rect(800, 400, 185, 50)
    back_rect = pygame.Rect(795, 395, 195, 60)

    # back & front of button
    pygame.draw.rect(window, (30, 30, 30), back_rect)
    pygame.draw.rect(window, (50, 50, 50), rect)

    # making button yellow if touched
    if mouse_touching_button:
        window.blit(colored_box(195, 60), (795, 395))

    # drawing the text on buttons
    window.blit(font.render(" New Game", True, (255, 255, 255)), rect)

    # game title
    window.blit(massive_font.render("Elements for Money", True, (200, 200, 255)), pygame.Rect(50, 50, 195, 60))

    # element banner
    x = 150
    while x < 800:
        element_interior(window, x, 200, "Air", (0, 0, 0, 0))
        element_interior(window, x+59, 200, "Earth", (0, 0, 0, 0))
        element_interior(window, x+110, 200, "Fire", (0, 0, 0, 0))
        element_interior(window, x+160, 202, "Water", (0, 0, 0, 0))
        x += 205

def how_to_play_screen(window, mouse_touching_button):
    # rects of buttons
    rect = pygame.Rect(830, 470, 95, 50)
    back_rect = pygame.Rect(825, 465, 105, 60)

    # back & front of button
    pygame.draw.rect(window, (30, 30, 30), back_rect)
    pygame.draw.rect(window, (50, 50, 50), rect)

    # making button yellow if touched
    if mouse_touching_button:
        window.blit(colored_box(105, 60), (825, 465))

    # drawing the text on buttons
    window.blit(font.render(" Start", True, (255, 255, 255)), rect)

    # drawing the instructions
    text = "Place elements next to each other to set up a reaction."
    window.blit(font.render(text, True, (255, 255, 255)), pygame.Rect(50, 50, 50, 50))
    text = "  *Press tab to see shortcuts."
    window.blit(medium_font.render(text, True, (255, 255, 255)), pygame.Rect(50, 200, 50, 50))
    text = "You may pick a new element from the shop each cycle."
    window.blit(font.render(text, True, (255, 255, 255)), pygame.Rect(50, 150, 50, 50))
    text = "Advance to the next cycle to do all reactions and gain gold."
    window.blit(font.render(text, True, (255, 255, 255)), pygame.Rect(50, 250, 50, 50))
    text = "  *Mouse1 (normally left click) or space to advance 1"
    window.blit(medium_font.render(text, True, (255, 255, 255)), pygame.Rect(50, 295, 50, 50))
    text = "  **Mouse2 (normally right click) or enter to advance many."
    window.blit(medium_font.render(text, True, (255, 255, 255)), pygame.Rect(50, 330, 50, 50))
    text = "Get enough gold to pay off each payment."
    window.blit(font.render(text, True, (255, 255, 255)), pygame.Rect(50, 380, 50, 50))

def lose_screen(window, mouse_touching_button, results_summary):
    # button rects
    rect = pygame.Rect(420, 410, 320, 50)
    back_rect = pygame.Rect(415, 405, 330, 60)

    # back & front of the buttons
    pygame.draw.rect(window, (30, 30, 30), back_rect)
    pygame.draw.rect(window, (50, 50, 50), rect)

    # making button yellow if touched
    if mouse_touching_button:
        window.blit(colored_box(330, 60), (415, 405))
    
    # button text
    window.blit(font.render(" Return to Main Menu", True, (255, 255, 255)), rect)
    
    # unpacking results tuple    
    gold, rank, rank_color, payment_reached, total_gold_earnt, = results_summary

    # blitting text
    window.blit(big_font.render("You missed payment.", True, (200, 200, 255)), pygame.Rect(50, 50, 195, 60))
    window.blit(font.render(f"You lost at payment {payment_reached}.", True, 
                            (200, 200, 255)), pygame.Rect(70, 150, 195, 60))
    window.blit(font.render(f"You missed payment by {abs(gold)}g.", True, 
                            (200, 200, 255)), pygame.Rect(70, 200, 195, 60))
    window.blit(font.render(f"You earnt a total of {total_gold_earnt}g.", True, 
                            (200, 200, 255)), pygame.Rect(70, 250, 195, 60))
    window.blit(font.render(f"{rank} Rank", True, rank_color), pygame.Rect(70, 300, 195, 60))

def ui(window, gold):
    # Board
    pygame.draw.rect(window, (30, 30, 30), pygame.Rect(50, 50, 670, 500))
    pygame.draw.rect(window, (40, 40, 40), pygame.Rect(60, 60, 650, 100))
    pygame.draw.rect(window, (40, 40, 40), pygame.Rect(60, 170, 650, 370))
    window.blit(big_font.render("Elements on Board:", False, (255, 255, 255)), (70, 65))

    # Right side
    pygame.draw.rect(window, (30, 30, 30), pygame.Rect(735, 50, 415, 500))
    pygame.draw.rect(window, (40, 40, 40), pygame.Rect(745, 60, 395, 100))
    pygame.draw.rect(window, (40, 40, 40), pygame.Rect(745, 170, 395, 105))
    pygame.draw.rect(window, (40, 40, 40), pygame.Rect(745, 285, 395, 255))
    window.blit(big_font.render("Store:", False, (255, 255, 255)), (755, 65))

    window.blit(font.render("Gold: " + str(gold), False, (200, 200, 50)), (20, 550))

def previous_reactions(window, previous_reactions, scroll):
    # picks first 14 reactions if scroll is 0. skips first <scroll> number of reactions otherwise.
    new_reactions_list = []
    while scroll < len(previous_reactions) and len(new_reactions_list) < 14:
        new_reactions_list.append(previous_reactions[scroll])
        scroll += 1
    
    # drawing reactions
    window.blit(medium_font.render("Previous Turn's Reactions:", False, (180, 180, 180)), (752, 287))
    y = 320
    for reaction in new_reactions_list:
        reactants, products, gold_from_reaction = reaction

        # dividing into two sides
        left_side = f"{reactants[0]} + {reactants[1]} --> "
        right_side =  f"{products[0]} + {products[1]} + {str(gold_from_reaction)} g"
        
        # replacing "Empty" with blanks
        if products[1] == "Empty":
            right_side =  f"{products[0]} + {str(gold_from_reaction)} g"
            if products[0] == "Empty":
                right_side = str(gold_from_reaction) + "g"
        elif products[0] == "Empty":
                right_side = f"{products[1]} + {str(gold_from_reaction)} g"
            
        # combining sides then drawing
        text = left_side + right_side
        window.blit(tiny_font.render(text, False, (180, 180, 180)), (752, y))
        y += 15

def up_scroll_button(window, touching_mouse):
    pygame.draw.rect(window, (30, 30, 30), pygame.Rect(1100, 295, 30, 30))
    pygame.draw.rect(window, (40, 40, 40), pygame.Rect(1103, 298, 24, 24))
    pygame.draw.rect(window, (20, 20, 20), pygame.Rect(1106, 307, 18, 12))
    pygame.draw.rect(window, (20, 20, 20), pygame.Rect(1109, 304, 12, 3))
    pygame.draw.rect(window, (20, 20, 20), pygame.Rect(1112, 301, 6, 3))

    # yellow if touching mouse
    if touching_mouse:
        window.blit(colored_box(30, 30), (1100, 295))

def down_scroll_button(window, touching_mouse):
    pygame.draw.rect(window, (30, 30, 30), pygame.Rect(1100, 499, 30, 30))
    pygame.draw.rect(window, (40, 40, 40), pygame.Rect(1103, 502, 24, 24))
    pygame.draw.rect(window, (20, 20, 20), pygame.Rect(1106, 505, 18, 12))
    pygame.draw.rect(window, (20, 20, 20), pygame.Rect(1109, 517, 12, 3))
    pygame.draw.rect(window, (20, 20, 20), pygame.Rect(1112, 520, 6, 3))

    # yellow if touching mouse
    if touching_mouse:
        window.blit(colored_box(30, 30), (1100, 499))

def next_cycle(window, touching_mouse, turns, payment):
    pygame.draw.rect(window, (50, 50, 50), pygame.Rect(480, 555, 135, 40))
    pygame.draw.rect(window, (60, 60, 60), pygame.Rect(485, 560, 125, 30))
    if touching_mouse:          # gold
        window.blit(colored_box(135, 40), (480, 555))
    window.blit(medium_font.render("Next Cycle", False, (200, 200, 200)), (489, 556))
    window.blit(medium_font.render("Cycles 'til Payment: " + str(turns), False, (200, 200, 200)), (900, 556))
    window.blit(medium_font.render("Payment: " + str(payment), False, (200, 200, 200)), (700, 556))

def element_background(window, x, y, grid_x, grid_y, mouse_rect, element_selected, second_element_selected):
    element_rect = pygame.Rect(x, y, 75, 75)
    element_rect_interior = pygame.Rect(x+5, y+5, 65, 65)

    pygame.draw.rect(window, (20, 20, 20), element_rect)
    pygame.draw.rect(window, (30, 30, 30), element_rect_interior)

    # blitting additional color based on status
    if element_selected == [grid_x, grid_y]:                                            # orange for selected elements
        window.blit(colored_box(75, 75, (200, 150, 0)), (x, y))
    
    elif second_element_selected == [grid_x, grid_y]:      # green if clicked
        window.blit(colored_box(75, 75, (0, 255, 0)), (x, y))

    elif mouse_rect.colliderect(element_rect):                                          # yellow if hovering
        window.blit(colored_box(75, 75), (x, y))

grid_shortcuts = {
        (0, 0) : "1",   (1, 0) : "2",   (2, 0) : "3",   (3, 0) : "4",   (4, 0) : "5",   (5, 0) : "6",   (6, 0) : "7",
        (0, 1) : "q",   (1, 1) : "w",   (2, 1) : "e",   (3, 1) : "r",   (4, 1) : "t",   (5, 1) : "y",   (6, 1) : "u",
        (0, 2) : "a",   (1, 2) : "s",   (2, 2) : "d",   (3, 2) : "f",   (4, 2) : "g",   (5, 2) : "h",   (6, 2) : "j",
        (0, 3) : "z",   (1, 3) : "x",   (2, 3) : "c",   (3, 3) : "v",   (4, 3) : "b",   (5, 3) : "n",   (6, 3) : "m" }

shop_shortcuts = {0: "9", 1: "0", 2: "-", 3: "=" }

def shortcuts(window):
    # cycling same way as elements in the deck, drawing shortcuts
    x = 75; y = 184
    for grid_y in range(0, 4):
        for grid_x in range(0, 7):
            window.blit(small_font.render(grid_shortcuts[(grid_x, grid_y)], False, (200, 200, 200)), (x+7, y+1))
            x += 90
        y += 89
        x = 75
    
    # drawing shop shortcuts
    x = 765; y = 184
    for gride_x in range(0, 4):
        window.blit(small_font.render(shop_shortcuts[gride_x], False, (200, 200, 200)), (x+7, y+1))
        x += 93

    # drawing next cycle button shortcuts
    window.blit(tiny_font.render("Space", False, (200, 200, 200)), (478, 548))
    window.blit(tiny_font.render("Enter", False, (200, 200, 200)), (592, 548))

def shop_background(window, x, y, mouse_rect):
    element_rect = pygame.Rect(x, y, 75, 75)
    element_rect_interior = pygame.Rect(x+5, y+5, 65, 65)

    # drawing element box background
    pygame.draw.rect(window, (20, 20, 20), element_rect)
    pygame.draw.rect(window, (30, 30, 30), element_rect_interior)

    # making yellow is selected
    if mouse_rect.colliderect(element_rect):
        window.blit(colored_box(75, 75), (x, y))

def shop_curtains(window):
    pygame.draw.rect(window, (10, 0, 0), pygame.Rect(735, 50, 415, 225))

def add_gold(value, x, y):
    # adds values to the list to move (used in next function)
    if value != "0":
        gold_particle_list.append([value, x, y, -3, random.randint(-3, 3)])

def gold_animation(window):
    # moves all values in the list
    for particle in gold_particle_list:
        window.blit(font.render(particle[0], False, (250, 250, 50)), (particle[1], particle[2]))
        particle[1] += particle[4]      # changes x by the pre-set random velocity
        particle[2] += particle[3]      # changes y by gravity
        particle[3] += 0.3              # increases y gravity
        if particle[2] > 600:
            gold_particle_list.remove(particle)

# <name>: (
#     "              ",
#     "              ",
#     "              ",
#     "              ",
#     "              ",
#     "              ",
#     "              ",
#     "              ",
#     "              ",
#     "              ",
#     "              ",
#     "              ",
#     "              ",
#     "              "
# )

icon_dictionary = {
"Air": (
    "      YYY     ",
    "     YY YY    ",
    "    YY   YY   ",
    "   YY     YY  ",
    "   YY  YY  YY ",
    "   YY   YY  YY",
    "    YY   Y   Y",
    "     YY YY   Y",
    "      YYY    Y",
    "            YY",
    "           YY ",
    "          YY  ",
    "        YYY   ",
    "  YYYYYYY     "
),
"Earth": (
    "              ",
    "              ",
    "         GGGG ",
    "       GGGGGG ",
    "      GGGGG   ",
    "      GG      ",
    "      GG      ",
    " GGGGGGGGGGGG ",
    " GbbGbbbGGbbG ",
    " bbbbbbbbbbbb ",
    "  bbbbbbbbbb  ",
    "   bbbbbbbb   ",
    "    bbbbbb    ",
    "              "
),
"Fire": (
    "              ",
    "       YY     ",
    "      YYY     ",
    "     YYOY    ",
    "    YYOOY     ",
    "    OOOO  O   ",
    "   OOOO  OO   ",
    "  OOOR  OORR  ",
    "  OOOR  OORRR ",
    "  OORR OOORRR ",
    "  ORRRROORRRR ",
    "  RRRRRRRRRRR ",
    "   RRRRRRRRR  ",
    "    RRRRRRR   "
),
"Water": (
    "              ",
    "     B        ",
    "     BB       ",
    "      BB      ",
    "     BBBB     ",
    "    BBBBBB    ",
    "   BBBBBBBB   ",
    "   BBBBBBBB   ",
    "  BBBBBBBBBB  ",
    "  BBBBBBBBBB  ",
    "  BBBBBBBBBB  ",
    "   BBBBBBBB   ",
    "    BBBBBB    ",
    "              "
),
"Dust": (
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "    gbbb      ",
    "   gggbbb     ",
    "   gggbbb     ",
    "              "
),
"Energy": (
    "      gg      ",
    " gg  O  g  gg ",
    "g  g g  P g  g",
    " g  gg  gg  g ",
    "  g  g  g  g  ",
    " ggPggggggggg ",
    "g    g  g    g",
    "g    g  O    g",
    " gggggggggPgg ",
    "  g  g  g  g  ",
    " g  gg  gg  g ",
    "g  P g  O g  g",
    " gg  g  g  gg ",
    "      gg      "
),
"Cold": (
    "   ll     ll  ",
    "  ll  l l  ll ",
    " l l   l   l l",
    "    l  l  l   ",
    "     l l l    ",
    "  l   lll   l ",
    "   lllllllll  ",
    "  l   lll   l ",
    "     l l l    ",
    "    l  l  l   ",
    " l l   l   l l",
    "  ll  l l  ll ",
    "   ll     ll  ",
    "              "
),
"Lava": (
    "              ",
    "        YY    ",
    "       YO     ",
    "      OO      ",
    "     OOOO     ",
    "    OOOOOO    ",
    "   RRROOOOO   ",
    "   RRRRROOO   ",
    "  RRRRRRRROO  ",
    "  rrrRRRRRRR  ",
    "  rrrrrrRRRR  ",
    "   rrrrrrrr   ",
    "    rrrrrr    ",
    "              "
),
"Clay": (
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "       bb     ",
    "    bbbbbbb   ",
    "   bbbbbbbbb  "
),
"Steam": (
    "              ",
    "          ww ",
    "   www   wwww ",
    "  wwwwwwwwwww ",
    " wwwwwwwwwww  ",
    " wwwwwwwwww   ",
    "  wwwwwwwww   ",
    "    wwwwwwww  ",
    "    wwwwwwww ",
    "   wwwwwwwwwww",
    "    wwwww www",
    "       ww     ",
    "       ww     ",
    "       ww     "
),
"Stone": (
    "              ",
    "              ",
    "              ",
    "     gggggg   ",
    "    ggggggggg ",
    "   gggggggggg ",
    "  gggggggggg  ",
    "  gggggggggg  ",
    "  gggggggggg  ",
    "   gggggggg   ",
    "    gggggg    ",
    "              ",
    "              ",
    "              "
),
"Metal": (
    "              ",
    "              ",
    "  wwwwwwwwww  ",
    "  wgwwwwwwgw  ",
    "  wwwwwwwwww  ",
    "  wwwwwwwwww  ",
    "  wwwwwwwwww  ",
    "  wwwwwwwwww  ",
    "  wwwwwwwwww  ",
    "  wwwwwwwwww  ",
    "  wgwwwwwwgw  ",
    "  wwwwwwwwww  ",
    "              ",
    "              "
),
"Electricity": (
    "              ",
    "        YY    ",
    "       YY   Y ",
    " Y    YY      ",
    "     YY       ",
    "    YY        ",
    "   YYYYYYYY   ",
    "        YY    ",
    "       YY     ",
    " Y    YY      ",
    "     YY    Y  ",
    "    YY        ",
    "   YY    Y    ",
    "              "
),
"Plants": (
    "      YY      ",
    "      YY      ",
    "    YYPPYY    ",
    "    YYPPYY    ",
    "      YY      ",
    "      YY      ",
    "      GG GGG  ",
    "      GGGG    ",
    "      GG      ",
    "      GG      ",
    "      GG      ",
    "      GG      ",
    "GGGGGGGGGGGGGG",
    "bbbbbbbbbbbbbb"
),
"Life": (
    " l          l ",
    " lYYYRYYPYYYl ",
    "  l        l  ",
    "  l        l  ",
    "   lYYYBYYl   ",
    "    l    l    ",
    "     llll     ",
    "     l  l     ",
    "    l    l    ",
    "   lYPYYYYl   ",
    "  l        l  ",
    "  l        l  ",
    " lYYBYYPYYYYl ",
    " l          l "
),
"Human": (
    "      bb      ",
    "     bbbb     ",
    "     bbbb     ",
    "      bb      ",
    "    bbbbbb    ",
    "   b bbbb b   ",
    "   b bbbb b   ",
    "   b bbbb b   ",
    "   b bbbb b   ",
    "     bbbb     ",
    "     b  b     ",
    "     b  b     ",
    "     b  b     ",
    "     b  b     "
),
"Love": (
    "              ",
    "   RR    RR   ",
    "  RRRR  RRRR  ",
    " RRRRRRRRRRRR ",
    "RRRRRRRRRRRRRR",
    "RRRRRRRRRRRRRR",
    " RRRRRRRRRRRR ",
    " RRRRRRRRRRRR ",
    "  RRRRRRRRRR  ",
    "   RRRRRRRR   ",
    "    RRRRRR    ",
    "     RRRR     ",
    "      RR      ",
    "              "
),
"Robot": (
    "     wwww     ",
    "     wwww     ",
    "     wwww     ",
    "      ww      ",
    "   wwwwwwww   ",
    "   w wwww w   ",
    "   w wwww w   ",
    "   w wwww w   ",
    "   w wwww w   ",
    "     wwww     ",
    "     w  w     ",
    "     w  w     ",
    "     w  w     ",
    "     w  w     "
),
"Ceramic": (
    "     bbbb     ",
    "      bb      ",
    "      bb      ",
    "      bb      ",
    "     bbbb     ",
    "    bbbbbb    ",
    "   bbbbbbbb   ",
    "  bbbbbbbbbb  ",
    " bbbbbbbbbbbb ",
    " bbbbbbbbbbbb ",
    " bbbbbbbbbbbb ",
    "  bbbbbbbbbb  ",
    "   bbbbbbbb   ",
    "    bbbbbb    "
),
"Wind": (
    "        YYYY  ",
    "       YY  YY ",
    "      YY    Y ",
    "       YY  YY ",
    "          YY  ",
    " YYYYYYYYYY   ",
    "              ",
    "        YYYY  ",
    "       YY  YY ",
    "      YY    YY",
    "     YY  YY  Y",
    "      YYYY  YY",
    "           YY ",
    "  YYYYYYYYYY  "
),
"Tornado": (
    "     YYYYYY   ",
    "    YY    YY  ",
    "   YY  YY  YY ",
    "  YY  YY  YY  ",
    "  YY   YYYY   ",
    "   YY       Y ",
    "    YYYY   YY ",
    "     YYYYYYY  ",
    "     YYYYYY   ",
    "      YYYY    ",
    "     YYYY     ",
    "    YYYY      ",
    "     YYY      ",
    "       YY     "
),
"Sand": (
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "      YYYY    ",
    "   YYYYYYYYY  ",
    " YYYYYYYYYYYY "
),
"Sandstorm": (
    "  YY YYYYYY   ",
    " YY YY    YY  ",
    " Y YY      YY ",
    " Y  YY  YY  YY",
    " YY  YYYY   YY",
    "  YY       YY ",
    "   YYYYY  YYY ",
    "    YYYYYYYY  ",
    "     YYYYYY   ",
    "   Y  YYYY    ",
    "     YYYY   Y ",
    "    YYYY      ",
    " Y   YYY   Y  ",
    "       YY     "
),
"Ice": (
    "              ",
    "              ",
    "     BBBBBBBB ",
    "    BlllllBlB ",
    "   BlllllBllB ",
    "  BllBBBBlllB ",
    " BBBBBllBlllB ",
    " BllllllBlllB ",
    " BllllllBlllB ",
    " BllllllBlllB ",
    " BllllllBllB  ",
    " BllllllBBB   ",
    " BlllBBBB     ",
    " BBBBB        "
),
"Blizzard": (
    "     llllll   ",
    "    ll    ll  ",
    "   ll      ll ",
    " l  ll  ll  ll",
    " ll  llll   ll",
    " lll       ll ",
    "  llllll  lll ",
    "   lllllllll  ",
    " l   llllll  l",
    "      llll    ",
    "   l  llll    ",
    "     llll     ",
    "     lll     ",
    "       ll  l  "
),
"Cloud": (
    "     WWWW     ",
    "  WWWWWWWWW   ",
    "WWWWWWWWWWWWW ",
    "   WWWWWWWWWW ",
    "  WWWWWWWWWW  ",
    "   WWWWWWWW   ",
    "              ",
    "       WWWWW  ",
    "      WWWWWWWW",
    "         WWWW ",
    "              ",
    "              ",
    "              ",
    "              "
),
"Rain": (
    "     gggg     ",
    "  ggggggggg   ",
    "gggggggggggg  ",
    " ggggggggggg  ",
    "  ggggg  B    ",
    "         B    ",
    "   B          ",
    "   B  gggggg  ",
    "     gggggggg ",
    " B      gggg  ",
    " B            ",
    "    B   B     ",
    "    B       B ",
    "              "
),
"Thunder": (
    "     gggg     ",
    "  ggggggggg   ",
    "gggggggggggg  ",
    " ggggggggggg  ",
    "  ggggg  B    ",
    "         B    ",
    "  YY          ",
    " YY    ggggg  ",
    "YY    ggggggg ",
    "YYYY    gggg  ",
    "  YY         ",
    " YY     B     ",
    "YY      B   B ",
    "            B "
),
"Snow": (
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "      WW      ",
    "     WWWWWW   ",
    "   WWWWWWWWW  ",
    " WWWWWWWWWWWW "
),
"Snowman": (
    "              ",
    "     WWWW     ",
    "    WNWWNW    ",
    "    WWWWWW    ",
    "     WWWW     ",
    "    WWWWWW    ",
    "   WWWNNWWW   ",
    "   WWWWWWWW   ",
    "    WWNNWW    ",
    "   WWWWWWWW   ",
    "  WWWWNNWWWW  ",
    "  WWWWWWWWWW  ",
    "  WWWWWWWWWW  ",
    "   WWWWWWWW   "
),
"Avalanche": (
    "              ",
    "              ",
    "              ",
    "      WWWWWW  ",
    "    WWWWWWWWW ",
    "   WWWWWWWWWW ",
    "  WWWWWWWWWWWW",
    " WWWWWWWWWWWW ",
    " WWWWWWW  WWW ",
    " WWWWW     WWW",
    "  WWW       WW",
    "  WWW      WW ",
    " WWWWW        ",
    "  WWWWWW      "
),
"Volcano": (
    "              ",
    "  RO    R  OR ",
    "    RO  R OR  ",
    "     RR   R   ",
    "      RR      ",
    "     RbRRb    ",
    "    Rbbbbb    ",
    "    bbbbbbbR  ",
    "   bbbbbbbbR  ",
    "  RbbbbbbbbRO ",
    " RbbbbbbbbbbR ",
    " RbbbbbbbbbbR ",
    " bbbbbbbbbbbb ",
    "Rbbbbbbbbbbbb "
),
"Mountain": (
    "              ",
    "              ",
    "              ",
    "              ",
    "      bb      ",
    "     bbbb     ",
    "    bbbbbb    ",
    "    bbbbbb    ",
    "   bbbbbbbb   ",
    "   bbbbbbbb   ",
    "  bbbbbbbbbb  ",
    "  bbbbbbbbbb  ",
    " bbbbbbbbbbbb ",
    " bbbbbbbbbbbb "
),
"Ocean": (
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "  BBB    BBBB ",
    "BBBBBBBBBBBBBB",
    "BBBBBBBBBBBBBB",
    "BBBBBBBBBBBBBB",
    "BBBBBBBBBBBBBB"
),
"Wave": (
    "              ",
    "              ",
    "    BBBBB     ",
    "   BBBBBBB    ",
    "  BBB   BBB   ",
    " BBB     BBB  ",
    "BBB       BBB ",
    "BB        BBB ",
    "BBB      BBB  ",
    "BBBB   BBB    ",
    "BBBBB         ",
    "BBBBBBBBBBBBBB",
    "BBBBBBBBBBBBBB",
    "BBBBBBBBBBBBBB"
),
"Earthquake": (
    "bb  bbbbb     ",
    "bbb   bbbbb   ",
    "bbbbb  bbbbb  ",
    "  bbbbb  bbbb ",
    "   bbbbb  bbb ",
    "  bbbbb  b bb ",
    " bbbbb  bbbb  ",
    "bbb b  bbbbbb ",
    "bbbb  b b bbb ",
    " bbbb bb bbbb ",
    " bbbb b bbbbb ",
    " bbbb  bbbbb  ",
    " bbbb bbbbb   ",
    "  bbbb bbbbb  "
),
"Tsunami": (
    "              ",
    "BB       BBBB ",
    " BB     BB  BB",
    "       BB    B",
    "  BBBBBBBBB BB",
    " BBB    BBB   ",
    "BBB      BBB  ",
    "BB       BBB  ",
    "BBB     BBB BB",
    "BBBB  BBB  BB ",
    "BBBBB     BB  ",
    "BBBBBBBBBBBBBB",
    "BBBBBBBBBBBBBB",
    "BBBBBBBBBBBBBB"
),
"Landslide": (
    "              ",
    "              ",
    "              ",
    "GG  bbb       ",
    "bGG bbbb      ",
    "bbG  bbb      ",
    "bbb  bbbb     ",
    "bbb  b b b    ",
    "bbb  bb   b   ",
    "bbb   b b     ",
    "bbb   b   b   ",
    "bbb   b b     ",
    "bbb b    b    ",
    "bbb   b   b   "
),
"Egg": (
    "              ",
    "              ",
    "      WW      ",
    "     WWWW     ",
    "    WWWWWW    ",
    "    WWWWWW    ",
    "   WWWWWWWW   ",
    "   WWWWWWWW   ",
    "   WWWWWWWW   ",
    "   WWWWWWWW   ",
    "   WWWWWWWW   ",
    "    WWWWWW    ",
    "     WWWW     ",
    "              "
),
"AI": (
    "              ",
    "              ",
    "              ",
    "              ",
    "   llllllll   ",
    "  llllllllll  ",
    "  llllllllll  ",
    "  llllllllll  ",
    "  llllllllll  ",
    "   llllllll   ",
    "  llll        ",
    "  ll          ",
    "              ",
    "              "
),
"Android": (
    "    G    G    ",
    "     G  G     ",
    "    GGGGGG    ",
    "   GGWGGWGG   ",
    "   GGGGGGGG   ",
    "    WWWWWW    ",
    " GWGGGGGGGGWG ",
    " G GGGGGGGG G ",
    " G GGGGGGGG G ",
    "   GGGGGGGG   ",
    "    GG  GG    ",
    "    GG  GG    ",
    "    GG  GG    ",
    "    GG  GG    "
),
"Bird": (
    "              ",
    "              ",
    "              ",
    "        wwww  ",
    "       wwNwwYY",
    "   wwwwwwwww  ",
    "  wwwwwwwww   ",
    "wwwwwwwwww    ",
    "   wwwwww     ",
    "    Y  Y      ",
    "    YY YY     ",
    "              ",
    "              ",
    "              "
),
"Beast": (
    "              ",
    "              ",
    "              ",
    "        gg  gg",
    "         gggg ",
    "        gNggNg",
    " ggggggggggggg",
    "ggggggggggggg ",
    "gggggggggggg  ",
    "  ggggggggg   ",
    "   w     w    ",
    "   ww    ww   ",
    "              ",
    "              "
),
"Fish": (
    "              ",
    "              ",
    "              ",
    " B     BBBB   ",
    " BB   BBBBBB  ",
    " BBB BBBBBWWB ",
    " BBBBBBBBBWNBB",
    " BBBBBBBBBBBBB",
    " BBB BBBBBBBB ",
    " BB   BBBBBB  ",
    " B     BBBB   ",
    "              ",
    "              ",
    "              "
),
"Phoenix": (
    "              ",
    "   OO    OOO  ",
    " R  OO  OO    ",
    " RR OORRRRR   ",
    "  RRORRRNRRYY ",
    "   RRRRRRRRR  ",
    "   RRRRRRRR   ",
    "RRRRRRRRRR    ",
    "   RRRRRR     ",
    "    Y  Y      ",
    "    YY YY     ",
    "              ",
    "              ",
    "              "
),
"Seeds": (
    "              ",
    "              ",
    "      RRR     ",
    "WW    RR      ",
    "WW        OO  ",
    "W        OOO  ",
    "   YY         ",
    "   YYY    b   ",
    "          bb  ",
    "    rr    bb  ",
    "    rrr       ",
    "         qq   ",
    "         qqq  ",
    "              "
),
"Beach": (
    "       YYYYYYY",
    "    YYYYYYYYBB",
    "   YYYYYYBBBBB",
    " YYYYYYYBBBBBB",
    "YYYYYBBBBBBBBB",
    "YYYYBBBBBBBBBB",
    "YYYBBBBBBBBBBB",
    "YYYBBBBBBBBBBB",
    "YYYYBBBBBBBBBB",
    "YYYYYYYBBBBBBB",
    " YYYYYYYBBBBBB",
    "  YYYYYYYBBBBB",
    "   YYYYYYYYBBB",
    "    YYYYYYYYYY"
),
"Hurricane": (
    "  BB BBBBB    ",
    " BB BB  BBB  B",
    " B BB     BB  ",
    " B  BB  B  BB ",
    " BB  BBBB  BB ",
    " BBB       BB ",
    "  BBBBB   BBB ",
    "    BBBB  BBB ",
    " B    BB BBB  ",
    "      BBBBB   ",
    "   B  BBBB    ",
    "     BBBB     ",
    "     BBB      ",
    "   BBBB    B  "
),
"Island": (
    "              ",
    "     GG   GG  ",
    "    G  G G  G ",
    "      GGGGG   ",
    "     G  b  G  ",
    " BBBBBBBbBBBBB",
    "BBYYYYYYbYYYYB",
    "BYYdddddbdYYYY",
    "BYYdddddddddYY",
    "BBYYddddddddYB",
    "BBYYYYYdddYYYB",
    " BBBBYYYYYYYBB",
    "  BBBBBBBBBBB ",
    "              "
),
"Wood": (
    "              ",
    "    bbbbbb    ",
    "   boooooob   ",
    "  boobbbboob  ",
    " boobooooboob ",
    " bboobbbboobb ",
    " boboooooobob ",
    " boobbbbbboob ",
    " boooooooooob ",
    " boooooooooob ",
    " boooooooooob ",
    "  boooooooob  ",
    "   boooooob   ",
    "    bbbbbb     "
),
"Duststorm": (
    "     wwbwww   ",
    "    ww    ww  ",
    "   ww      ww ",
    " w  ww  ww  bw",
    " wb  wwww  w w",
    " w w      www ",
    "  wwwwww  www ",
    "   ww wwww w  ",
    " w   www ww   ",
    "      wwww  w ",
    "   b  wwww    ",
    "     wwww     ",
    "     wwb     ",
    "    wwwww  w  "
),
"Cactus": (
    "      dd      ",
    "     dddd     ",
    "     dddd     ",
    "     dddd  dd ",
    "     dddd  dd ",
    "  ddddddddddd ",
    " ddddddddddd  ",
    " dd  dddd     ",
    " dd  dddd     ",
    " dd  dddd     ",
    "     dddd     ",
    "     dddd     ",
    "  YYYYYYYYYY  ",
    "YYYYYYYYYYYYYY"
),
"Glassware": (
    "              ",
    "    wwwwww    ",
    "   w      w   ",
    "   ww    ww   ",
    "   wwwwwwww   ",
    "   wwwwwwww   ",
    "    wwwwww    ",
    "    wwwwww    ",
    "     wwww     ",
    "      ww      ",
    "      ww      ",
    "      ww      ",
    "    wwwwww    ",
    "   wwwwwwww   "
),
"Alcohol": (
    "              ",
    "              ",
    "      bb      ",
    "      dd      ",
    "      dd      ",
    "     dddd     ",
    "    dddddd    ",
    "    dddddd    ",
    "    wwwwww    ",
    "    wwwwww    ",
    "    dddddd    ",
    "    dddddd    ",
    "    dddddd    ",
    "    dddddd    "
),
"Ash": (
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "       N      ",
    "      NNN     ",
    "    NNNNNN    ",
    "  NNNNNNNNN   ",
    " NNNNNNNNNNN  ",
    "              "
),
"Angler": (
    "              ",
    "     wwww     ",
    "    wwwwww    ",
    "     qqqq     ",
    "      qq      ",
    "    WWWWWW    ",
    "   WWWWWW W   ",
    "   W WWWW  q  ",
    "   W WWWW BBB ",
    "   q NNNN  B  ",
    "     NNNN BBB ",
    "     N  N BBB ",
    "     N  N  B  ",
    "     q  q     "
),
"Miner": (
    "     YYYY     ",
    "    YYYYYY    ",
    "     bbbb     ",
    "      bb      ",
    "    OOOOOO    ",
    "   O OOOO O   ",
    "   O OOOO O   ",
    "   O OOOO O   ",
    "   b OOOO b   ",
    "w b  OOOO     ",
    "wb   O  O     ",
    " ww  O  O     ",
    "     b  b     ",
    "     b  b     "
),
"Gold": (
    "              ",
    "              ",
    "        AAA   ",
    "       AAAAA  ",
    "      AAAAAAA ",
    "     AAAAAAAA ",
    "    AAAAAAAA  ",
    "   AAAAAAAA   ",
    "  AAAAAAAA    ",
    "  AAAAAAA     ",
    "   AAAAA      ",
    "    AAA       ",
    "              ",
    "              "
),
"Pirate": (
    "     NNNN     ",
    "    NNWWNN    ",
    "   NNNNNNNN   ",
    "     QQQQ     ",
    "      QQ      ",
    "    NNWWNN    ",
    "  YN NWWN NY  ",
    "  YY NWWN YY  ",
    " w   BBBB   w ",
    "w    NNNN    w",
    "     NNNN     ",
    "     N  N     ",
    "     N  N     ",
    "     N  N     "
),
"Boat": (
    "      W       ",
    "      WRR     ",
    "      WRRR    ",
    "      WRRRR   ",
    "      WRR     ",
    "      WR      ",
    "      W       ",
    "bb    W     bb",
    "bbbb  W   bbbb",
    " bbbbbbbbbbbb ",
    "  bbbbbbbbbb  ",
    "   bbbbbbbb   ",
    "    bbbbbb    ",
),
"Coal": (
    "              ",
    "   nnnn       ",
    "  nnnnnn      ",
    " nnnnnnn  nnn ",
    "nnnnnnn  nnnnn",
    " nnnnn  nnnnnn",
    "            nn",
    "    nnnnnnn   ",
    "   nnnnnnnnn  ",
    "  nnnnnnnnnn  ",
    "  nnnnnnnnn   ",
    "    nnnnn     ",
    "              ",
    "              "
),
"Oil": (
        "       N      ",
    "       NN     ",
    "       NNN    ",
    "      NNNN    ",
    "     NNNNN    ",
    "    NNNNNN    ",
    "   NNNNNNNN   ",
    "   NNNNNNNN   ",
    "  NNNNNNNNNN  ",
    "  NNNNNNNNNN  ",
    "  NNNNNNNNNN  ",
    "   NNNNNNNN   ",
    "    NNNNNN    ",
    "              "
),
"Natural Gas": (
    "              ",
    "              ",
    "      OOO     ",
    "   OOOOOOOO   ",
    "      OOOOOO  ",
    "     OOOOO    ",
    " OOOOOOOO     ",
    "     OOOOOOO  ",
    "  OOOOOOOO    ",
    "    OOOOOOO   ",
    "   OOOOO      ",
    "  OOOOOOOOO   ",
    "              ",
    "              "
),
"House": (
    "         ww   ",
    "         w    ",
    "              ",
    "        RR    ",
    "        RR    ",
    "   RRRRRRRR   ",
    "  RRRRRRRRRR  ",
    "  RRRRRRRRRR  ",
    "   WWWWWWWW   ",
    "   WllWWllW   ",
    "   WllWWllW   ",
    "   WWWWWWWW   ",
    "   WWWbbWWW   ",
    "   WWWbbWWW   "
),
"Music": (
    "              ",
    "           BB ",
    "           B  ",
    "  RR       BB ",
    "  R   YY  BB  ",
    "  R   YY  BB  ",
    " RR           ",
    " RR  GGGG     ",
    "     G  G     ",
    "     G  G     ",
    "    GG GG     ",
    "    GG GG     ",
    "              ",
    "              "
),
"Vocaloid": (
    "    Tp  pT    ",
    "   TTpTTpTT   ",
    "  TTTTWWTTTT  ",
    "  TT WWWW TT  ",
    "  T   WW   T  ",
    " T  WwTTwW  T ",
    " T  WwTTwW  T ",
    "   N wwTw N   ",
    "   N wwww N   ",
    "   W NwwN W   ",
    "     NNNN     ",
    "     W  W     ",
    "     N  N     ",
    "     N  N     "
),
"Dragon": (
    "   NN   BBBBBB",
    "  NN  BBBBB   ",
    " NN  BBBB     ",
    " BBBBBBBBBBB  ",
    "BBBBBBBBBBBBB ",
    "BBBB       BBB",
    "      BBB   BB",
    "     BB  B  BB",
    "B   BBB    BBB",
    "BB BBB    BBB ",
    "BBBBB    BBBBB",
    "  BBB   BBB BB",
    "   BBBBBBB   B",
    "    BBBBB     "
),
"Hero": (
    "       GG     ",
    "     GGGGG    ",
    "    GGGG      ",
    "    hhhh      ",
    "    hhhh      ",
    "     hh       ",
    "   GGGGGG     ",
    "  G GGGG G    ",
    "  G GGGG GB   ",
    "  h GGGG hBWWW",
    "    GGGG  B   ",
    "    b  b      ",
    "    b  b      ",
    "    b  b      "
),
"Carbon Dioxide": (
    "              ",
    "      NNNN    ",
    "    NNNNNNN   ",
    " NNNNNNNNNNN  ",
    "   NNNNNNNN   ",
    "     NNNNN    ",
    " NNNNNNNNN    ",
    "   NNNNNNNNN  ",
    " NNNNNNNNNN   ",
    "   NNNNNNN    ",
    " NNNNNNN      ",
    "  NNNNNNNN    ",
    "      NNNNNN  ",
    "              "
),
"Cola": (
    "      RR      ",
    "      NN      ",
    "      NN      ",
    "     NNNN     ",
    "    NNNNNN    ",
    "    NNNNNN    ",
    "    RRRRRR    ",
    "    RWRWWR    ",
    "    RRWRWR    ",
    "    RRRRRR    ",
    "    NNNNNN    ",
    "    NNNNNN    ",
    "    NNNNNN    ",
    "    NNNNNN    "
),
"Glacier": (
    "        W     ",
    "       WW     ",
    "       WW     ",
    "      WWW     ",
    "      WWWW    ",
    "     WWWWWW   ",
    "    WWWWWWW   ",
    "   WWWWlWWW   ",
    "   WWWllWWWWW ",
    " WWWWWlllWWWWW",
    "WWWWllllllWWWW",
    "   llllllllll ",
    "    lllllll   ",
    "      ll      "
),
"Permafrost": (
    "              ",
    "              ",
    "              ",
    "              ",
    "              ",
    "       W      ",
    "   W  WW  WW  ",
    " WWWWWWWWWWWW ",
    " WiiWWWiWWiiW ",
    " iiiiWWiiWiii ",
    "  iiiiWiiiii  ",
    "   iiiiiiii   ",
    "    iiiiii    ",
    "              "
),
"Light": (
    "              ",
    "       Y      ",
    "      YYY     ",
    "   Y   Y   Y  ",
    "    Y  Y  Y   ",
    "     Y Y Y    ",
    "  Y   YYY   Y ",
    " YYYYYYYYYYYYY",
    "  Y   YYY   Y ",
    "     Y Y Y    ",
    "    Y  Y  Y   ",
    "   Y   Y   Y  ",
    "      YYY     ",
    "       Y      "
),
"Will o' Wisp": (
    " YYYY    YY   ",
    "YYWWYY YYY  YY",
    "YWWWWYYYY  YY ",
    "YWWWWYYY  YYY ",
    "YYWWYY    YY  ",
    " YYYY    YYYY ",
    "        YYWWYY",
    "        YWWWWY",
    " YYYY   YWWWWY",
    "YYWWYY  YYWWYY",
    "YWWWWYY  YYYY ",
    "YWWWWYYY      ",
    "YYWWYYYYYY    ",
    " YYYYY        "
),
"Penguin": (
    "              ",
    "     NNNN     ",
    "    NNWWNN    ",
    "    NlWWlN    ",
    "    NWYYWN    ",
    "     NNNN     ",
    "    NNWWNN    ",
    "   NNWWWWNN  ",
    "  NNWWWWWWNN  ",
    " NNNWWWWWWNNN ",
    " N NNWWWWNN N ",
    "    NNNNNN    ",
    "     Y  Y     ",
    "    YY  YY    "
),
"Turtle": (
    "              ",
    "              ",
    "              ",
    "              ",
    "       ddd    ",
    " J    ddddd   ",
    "JNJ  ddddddd  ",
    "JJJJdddddddd J",
    " JJddddddddddJ",
    "   ddddddddd  ",
    "      J   J   ",
    "     JJ  JJ   ",
    "              ",
    "              "
),
"Tumbleweed": (
    "              ",
    "              ",
    "b  b      b  b",
    "b b  b  b  b b",
    " b  b    b  b ",
    "  bb b  b bb  ",
    "  b b bb b b  ",
    "b  b b  b b  b",
    "b bb b  b bb b",
    " b  b    b  b ",
    "  b  b  b  b  ",
    "bb b b  b b bb",
    "    b bb b    ",
    "     bbbb     "
),
"Angel": (
    "    YYYYYY    ",
    "yy         WW ",
    "  y   WWWWWW  ",
    "     WqqWW    ",
    "WWW WqqqqW WWW",
    " WWW  qq  WWW ",
    "    WWWWWW    ",
    "   WWWWWWWW   ",
    "yy W WWWW W yy",
    "   q WWWW q   ",
    "   q WWWW q   ",
    "     WW q     ",
    "  yy q  q  yy ",
    " y   q  q    y"
),
"Royalty": (
    "    A AA A    ",
    "    AAAAAA     ",
    "     bbbb     ",
    "     bbbb     ",
    "      bb      ",
    "    PPWWPP    ",
    "   PPPWWPPP   ",
    "   P PWWP P   ",
    "   b PWWP b   ",
    "   b NNNN b   ",
    "     PPPP     ",
    "    PPPPPP    ",
    " AA  b  b     ",
    "AAAA W  W   AA"
),
"Ice Brick": (
    "              ",
    "              ",
    "              ",
    "              ",
    "    iiiiiiii  ",
    "   iiiiiiiil  ",
    "  iiiiiiiill  ",
    " iiiiiiiilll  ",
    " lllllllill   ",
    " lllllllli    ",
    "  lllllll     ",
    "              ",
    "              ",
    "              "
),
"Ice Wall": (
    "              ",
    "              ",
    " lll llll lll ",
    "liiiliiiiliiil",
    "liiiliiiiliiil",
    " llllllllllll ",
    "liiiliiiiliiil",
    "liiiliiiiliiil",
    " llllllllllll ",
    "liiiliiiiliiil",
    "liiiliiiiliiil",
    " lll llll lll ",
    "              ",
    "              "
),
"Ice Building": (
    "              ",
    "              ",
    "              ",
    "  llllllllll  ",
    " llllllllllll ",
    "llliiiiiiiilll",
    " liiiiiiiiiil ",
    " lillillillil ",
    " lillillillil ",
    " liiiilliiiil ",
    " llllllllllll ",
    "              ",
    "              ",
    "              "
),
"Ice Mansion": (
    "              ",
    "  llllllllll  ",
    " llllllllllll ",
    "llliiiiiiiilll",
    " liililliliil ",
    " lillillillil ",
    " liiiiiiiiiil ",
    " llllllllllll ",
    " liiiiiiiiiil ",
    " lillillillil ",
    " lillillillil ",
    " liiiilliiiil ",
    " llllllllllll ",
    "              "
),
"Ice Palace": (
    "     A        ",
    "     ll       ",
    "    lllll     ",
    "   lllllll    ",
    "    liiil     ",
    "    lilil  Y  ",
    "  Y lilil  l  ",
    "  l lilil lll ",
    " ll liiilllll ",
    " lllliiiiilil ",
    " liliilliilil ",
    " liliilliilil ",
    " liliilliilil ",
    "WllllllllllllW"
),
"Tree": (
    "     dddd     ",
    "    dddddd    ",
    "   dddddddd   ",
    "   dddddddd   ",
    "  dddddddddd  ",
    "  dddddddddd  ",
    "   dddddddd   ",
    "   dddddddd   ",
    "     dddd     ",
    "      bb      ",
    "      bb      ",
    "      bb      ",
    "      bb      ",
    "      bb      "
),
"Forest": (
    "              ",
    "              ",
    "              ",
    "    ddd   ddd ",
    "  dddddddddddd",
    " ddddddddddddd",
    " ddddddddddddd",
    " dddddddddddd  ",
    "  dddddddd b  ",
    "   b bdddb b  ",
    "   b b b b b  ",
    "   b   b   b  ",
    "       b      ",
    "              "
),
"Lake": (
    "              ",
    "   BBB     BB ",
    "  BBBBBBB BBBB",
    "   BBBBBBBBBBB",
    "    BBBBBBBBBB",
    "    BBBBBBBBB ",
    "   BBBBBBBBBB ",
    "  BBBBBBBBBBB ",
    " BBBBBBBBBBBB ",
    "BBBBBBBBBBBB  ",
    "BBBBBB  BBB   ",
    " BBBBB        ",
    "  BBB         ",
    "              "
),
"Swamp": (
    "              ",
    "              ",
    "              ",
    "  d           ",
    " dd       d   ",
    "BddBB  BBddBB ",
    "BdddBBBBBddBBB",
    "BddddBBBBdddBB",
    "ddddddBBddddBd",
    "dddddddddddddd",
    "  dddddddddd  ",
    "              ",
    "              ",
    "              "
),
"Mangrove": (
    "              ",
    "  ddd    ddd  ",
    " dddddd ddddd ",
    "   b      b   ",
    "  b  ddd  b   ",
    "  b   b    b  ",
    "b bbbb     b  ",
    " bb       bb b",
    "bBBbBbBBBbBbbB",
    "bBbBbBBBbbBbBb",
    "bBbBbBBbBbBbBb",
    "BBbBbBBbBbBbBB",
    " BBBbBBBBbBBB ",
    "  BBBBBBBBBB  "
),
"Sun": (
    "              ",
    "              ",
    "     O  O     ",
    "    O OO      ",
    "     OYYO O   ",
    "  O OYYYYO O  ",
    "   OYYYYYYO   ",
    "   OYYYYYYO   ",
    "  O OYYYYO O  ",
    "   O OYYO     ",
    "      OO O    ",
    "     O  O     ",
    "              ",
    "              "
),
"Black Hole": (
    "   NNNN       ",
    "  N     N NN  ",
    " N  N  NNN  N ",
    " N N  N N N  N",
    "  N  N N   N N",
    " NNN NN NN   N",
    "  N N NNN N  N",
    "N  N NNN N N  ",
    "N   NN NN NNN ",
    "N N   N N  N  ",
    "N  N N N  N N ",
    " N  NNN  N  N ",
    "  NN N     N  ",
    "       NNNN   "
),
"Desert": (
    "              ",
    "        yy    ",
    "       y  y   ",
    "   yy   y y   ",
    "     yy   y   ",
    "       yyy    ",
    "              ",
    "           YY ",
    "  YYYY    YYYY",
    " YYYYYY  YYYYY",
    "YYYYYYYYYYYYYY",
    "YYYYYYYYYYYYYY",
    "YYYYYYYYYYYYYY",
    "YYYYYYYYYYYYYY"
),
"Oasis": (
    "              ",
    "              ",
    "              ",
    "              ",
    " d d d        ",
    "  ddd         ",
    "   b d        ",
    "  b           ",
    " b            ",
    " b            ",
    "YYYBBBBBBBBBYY",
    "YYYYBBBBBBYYYY",
    " YYYYYYYYYYYY ",
    "  YYYYYYYYYY  "
),
"Circuit": (
    "              ",
    "              ",
    "              ",
    "YYYYYYYYYYddd ",
    "YYYYddYddddddd",
    "  ddddYYYYYdYd",
    "  dYddYdddddYd",
    "  dYYYYYYYYYYd",
    "  dYdddddddYdd",
    "  dddYYYYYYYdd",
    "   dddddddddd ",
    "              ",
    "              ",
    "              "
),
"World Tree": (
    "    dddddd    ",
    "   dd   d d   ",
    "  d  dd  d dd ",
    " d  dddd dd d ",
    " d dd  dd d dd",
    " d dd d d dd d",
    " d  dd dd dd d",
    " ddd  dd dd dd",
    "   dddbd d  d ",
    "     bbbdddd  ",
    "      bbbb    ",
    "     bbbbb    ",
    "    bbbbbbb   ",
    "  bbbbbbbbbbb "
),
}

color_list = (
        ("Y", (200, 200, 50)),      # Y | yellow
        ("y", (250, 250, 120)),     # y | bright yellow
        ("d", (30, 100, 30)),       # d | dark green
        ("G", (50, 250, 50)),       # G | green
        ("J", (150, 250, 150)),     # J | light green
        ("g", (80, 80, 80)),        # g | gray
        ("i", (150, 150, 240)),     # i | lighter blue
        ("l", (100, 100, 200)),     # l | light blue
        ("B", (50, 50, 250)),       # B | blue
        ("b", (150, 100, 30)),      # b | brown
        ("R", (250, 50, 50)),       # R | red
        ("r", (150, 30, 30)),       # r | dark red
        ("O", (250, 120, 50)),      # O | orange
        ("o", (250, 170, 100)),     # o | weaker orange
        ("W", (255, 255, 255)),     # W | white
        ("w", (110, 110, 110)),     # w | light gray
        ("P", (180, 50, 250)),      # P | purple
        ("N", (0, 0, 0)),           # N | black
        ("p", (220, 50, 250)),      # p | pink
        ("q", (250, 180, 200)),     # q | pale peach
        ("Q", (200, 180, 100)),     # Q | yellowish-white
        ("h", (200, 160, 90)),      # h | brownish-white
        ("A", (255, 220, 0)),       # A | gold 
        ("n", (10, 10, 10)),        # n | light black  
        ("T", (100, 200, 255)),     # T | turquoise
    )

def element_interior(window, x, y, element, mouse_rect):
    interior_rect = pygame.Rect(x, y, 75, 75)           
    x += 9          # minor off-setting of x and y to better fit inside
    y += 9

    icon = []                                   # image is blank if not replaced by an existing image
    if element != "Empty":
        if element in icon_dictionary:          # all elements that have an image get theirs added, replacing
            icon = icon_dictionary[element]     #  the blank image


    # looping through the whole image. using different x/y since it's used again.
    x_ = x
    y_ = y
    for row in icon:
        for value in row:
            
            # picking color and drawing
            for color in color_list:
                if value == color[0]:
                    pygame.draw.rect(window, color[1], pygame.Rect(x_, y_, 4, 4))
                    break

            x_ += 4
        x_ = x
        y_ += 4

    # drawing name and description
    if element != "Empty" and interior_rect.colliderect(mouse_rect):
        
        # making background blank to display stuff
        pygame.draw.rect(window, (40, 40, 40), pygame.Rect(745, 285, 395, 255))

        # black bar
        name_tag = pygame.Surface((385, 50))    # making a surface to get a transparent rect
        name_tag.fill((0, 0, 0))                # making surface black
        name_tag.set_alpha(100)                 # getting transparency
        window.blit(name_tag, (750, 290))

        # element name and gold
        window.blit(font.render(element, False, (255, 255, 255)), (755, 290))
        window.blit(font.render(str(gold_from(element)) + "g", False, (250, 250, 100)), (1080, 290))
        
        # description
        y = 340
        for line in description_of(element):
            window.blit(small_font.render(line, False, (180, 180, 180)), (755, y))
            y += 20
