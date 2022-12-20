import pygame
import sys
from pygame.locals import *
import draw
from draw import gold_from, pick_for_shop
from reactions import check_for_synergy
from functions import toggle, mouse_rect, playthrough_information, first_empty_slot_in

tick = pygame.time.Clock()

# Game set up
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
window_width = 1200
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Elemental Deck Builder')
icon = pygame.Surface((20, 20))
pygame.display.set_icon(icon)

# initializing font for later use
pygame.font.init()
big_font = pygame.font.SysFont('arial', 70)
font = pygame.font.SysFont('arial', 40)
medium_font = pygame.font.SysFont('arial', 30)
small_font = pygame.font.SysFont('arial', 20)
tiny_font = pygame.font.SysFont('arial', 12)

def menu():
    # assumes you already pressed space to prevent skipping through by mistake
    previous_space = True

    # menu on start
    while True:
        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()
                sys.exit()

        # used to see if space pressed
        key = pygame.key.get_pressed()
        
        # seeing if the mouse rect is colliding with the button rect
        mouse_touching_button = mouse_rect().colliderect(pygame.Rect(800, 400, 185, 50))

        # painting screen black, drawing menu
        window.fill((0, 0, 0))
        draw.main_menu(window, mouse_touching_button)

        # exits if button is clicked or space pressed
        if (mouse_touching_button and pygame.mouse.get_pressed()[0]) or (key[K_SPACE] and not previous_space):
            break
        
        # checking if pressed space for next frame
        previous_space = True if key[K_SPACE] else False

        pygame.display.flip()

    # assumes you already pressed space to prevent skipping through by mistake
    previous_space = True

    # how to play screen
    while True:
        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()
                sys.exit()
    
        # used to see if space pressed
        key = pygame.key.get_pressed()
        
        # seeing if the mouse rect is colliding with the button rect
        mouse_touching_button = mouse_rect().colliderect(pygame.Rect(830, 470, 95, 50))

        # painting screen black, drawing menu
        window.fill((0, 0, 0))
        draw.how_to_play_screen(window, mouse_touching_button)

        # exits if button is clicked or space pressed
        if (mouse_touching_button and pygame.mouse.get_pressed()[0]) or (key[K_SPACE] and not previous_space):
            break
        
        # checking if pressed space for next frame
        previous_space = True if key[K_SPACE] else False

        pygame.display.flip()
    
    # starts the game after menus are done
    main()


def lose_screen(gold, payment_cost):
    # getting results once to show in results
    results_summary = playthrough_information(payment_cost, gold)

    # assumes you already pressed space to prevent skipping through by mistake
    previous_space = True

    while True:
        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()
                sys.exit()

        # used to see if space pressed
        key = pygame.key.get_pressed()

        # seeing if the mouse rect is colliding with the button rect
        mouse_touching_button = mouse_rect().colliderect(pygame.Rect(420, 410, 320, 50))

        # painting screen black, drawing screen
        window.fill((0, 0, 0))
        draw.lose_screen(window, mouse_touching_button, results_summary)

        # exits if button is clicked or space pressed
        if (mouse_touching_button and pygame.mouse.get_pressed()[0]) or (key[K_SPACE] and not previous_space):
            break

        # checking if pressed space for next frame
        previous_space = True if key[K_SPACE] else False

        pygame.display.flip()

    # resetting particles when "exit to main menu" is pressed
    draw.gold_particle_list = []

    # resets game
    menu()


def main():
    # grid items
    deck = [
    ["Air", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"],
    ["Empty", "Empty", "Earth", "Empty", "Empty", "Empty","Empty"],
    ["Empty", "Empty", "Empty", "Empty", "Fire", "Empty", "Empty"],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Water"]
    ]

    # store stuffs
    purchase_selection = ["Air", "Earth", "Fire", "Water"]
    bought_from_store = False

    # selected item
    pick = []
    pick2 = []
    pick2_timer = 0
    
    # reactions from previous cycle & level of scroll through reaction list
    previous_reactions = []
    scroll = 0

    # starting statuses
    gold = 100
    payment = 100
    turns_to_next_cycle = 10
    luck = 4

    # FPS stuff
    show_FPS = False
    FPS_list = [60, 60, 60, 60]     # FPS from last 4 frames

    # seeing whether certain key(s) or mouse was pressed the frame prior to prevent holding the key from repeating effect
    previous_click_status = False
    previous_backspace = False
    previous_tab = False
    previous_space = True
    previous_grid_key_pressed = False

    # used to allow keyboard shortcuts instead of clicks
    shop_keys = {0: K_9,    1: K_0,    2: K_MINUS,    3: K_EQUALS}
    grid_keys = {
        (0, 0) : K_1,   (1, 0) : K_2,   (2, 0) : K_3,   (3, 0) : K_4,   (4, 0) : K_5,   (5, 0) : K_6,   (6, 0) : K_7,
        (0, 1) : K_q,   (1, 1) : K_w,   (2, 1) : K_e,   (3, 1) : K_r,   (4, 1) : K_t,   (5, 1) : K_y,   (6, 1) : K_u,
        (0, 2) : K_a,   (1, 2) : K_s,   (2, 2) : K_d,   (3, 2) : K_f,   (4, 2) : K_g,   (5, 2) : K_h,   (6, 2) : K_j,
        (0, 3) : K_z,   (1, 3) : K_x,   (2, 3) : K_c,   (3, 3) : K_v,   (4, 3) : K_b,   (5, 3) : K_n,   (6, 3) : K_m }
    
    show_shortcuts = False

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        window.fill((5, 5, 5))

        # repeated definitions
        key = pygame.key.get_pressed()          # used throughout for keyboard input
        elements_clicked = 0                    # used later to cancel selection if nothing is clicked
        cursor_rect = mouse_rect()              # doing this so the rect only needs to be made once per frame

        # drawing
        draw.ui(window, gold)
        draw.previous_reactions(window, previous_reactions, scroll)

        # seeing if left-clicked without holding
        if pygame.mouse.get_pressed()[0] and not previous_click_status:
            valid_click = True
        else:        
            valid_click = False

        # scoll button things
        if scroll > 0:
            touching_up_button = mouse_rect().colliderect(pygame.Rect(1100, 295, 30, 30))
            if touching_up_button and (valid_click or pygame.mouse.get_pressed()[2]) or key[K_UP]:
                scroll -= 1
            draw.up_scroll_button(window, touching_up_button)
        if len(previous_reactions) > 14 + scroll:
            touching_down_button = mouse_rect().colliderect(pygame.Rect(1100, 499, 30, 30))
            if touching_down_button and (valid_click or pygame.mouse.get_pressed()[2]) or key[K_DOWN]:
                scroll += 1
            draw.down_scroll_button(window, touching_down_button)
        
        # drawing & selection loop
        x = 75; y = 184
        # cycles through entire deck
        for grid_y, row in enumerate(deck):
            for grid_x, element in enumerate(row):
                
                # first, selection
                # selects if mouse clicked the element or if the matching keyboard shortcut was used
                element_rect = pygame.Rect(x, y, 75, 75)    
                if (cursor_rect.colliderect(element_rect) and valid_click) or \
                        (key[grid_keys[(grid_x, grid_y)]] and not previous_grid_key_pressed):
                    
                    # changes these statuses to stop from holding the mouse/keys
                    valid_click = False
                    previous_grid_key_pressed = True

                    # registers as a clicked element
                    elements_clicked += 1

                    # if nothing has been selected, it selects the clicked grid spot
                    if pick == []:
                        pick = [grid_x, grid_y]
                    
                    # otherwise, it swaps and leaves selected element as blank (saying there is none)
                    else:
                        deck[pick[1]][pick[0]], deck[grid_y][grid_x] = deck[grid_y][grid_x], deck[pick[1]][pick[0]]
                        pick = []
                        # selected becomes pick2; used to add green effect on last picked
                        pick2 = [grid_x, grid_y]
                        pick2_timer = 8    
                
                # second, drawing. 
                draw.element_background(window, x, y, grid_x, grid_y, cursor_rect, pick, pick2)
                draw.element_interior(window, x, y, element, cursor_rect)

                x += 90
            y += 89
            x = 75

        # 30 frame time where pick2 is green, counting down here
        if pick2_timer > 0:
            pick2_timer -= 1
            if pick2_timer == 0:
                pick2 = []

        # store (shop) things
        if not bought_from_store:
            x = 765; y = 184
            for item_number, element in enumerate(purchase_selection):
                element_rect = pygame.Rect(x, y, 75, 75)  
                draw.shop_background(window, x, y, cursor_rect)
                draw.element_interior(window, x, y, element, cursor_rect)

                # if clicking or pressing key of item, buys it if nothing has been bought
                if (cursor_rect.colliderect(element_rect) and valid_click) or key[shop_keys[item_number]]:
                    
                    # places into first slot of deck if nothing selected
                    if pick == []:

                        # first checking if a first slot exists
                        if first_empty_slot_in(deck) != None:
                            
                            # finally, placing into first slot
                            y_location, x_location = first_empty_slot_in(deck)
                            deck[y_location][x_location] = element
                            
                            # sets bought as true and gets new items
                            bought_from_store = True
                            purchase_selection = pick_for_shop(luck)

                    # if the slot selected is empty, buys it in that slot
                    elif deck[pick[1]][pick[0]] == "Empty":
                        deck[pick[1]][pick[0]] = purchase_selection[item_number]
                        pick = []

                        # sets bought as true and gets new items
                        bought_from_store = True
                        purchase_selection = pick_for_shop(luck)
                    
                    # note nothing is bought if the selected cell contains an element

                x += 93

        # if no elements were clicked during a click, cancels selection.
        if valid_click and elements_clicked == 0:
            pick = []

        # seeing if mouse is hovering over next cycle button 
        touching_next_cycle_button = cursor_rect.colliderect(pygame.Rect(480, 555, 135, 40))

        # drawing next cycle button
        draw.next_cycle(window, touching_next_cycle_button, turns_to_next_cycle, payment)

        # advances cycle once if clicking or pressing space, multiple if pressing enter or right click
        if (touching_next_cycle_button and (valid_click or pygame.mouse.get_pressed()[2])) \
            or key[K_RETURN] or (key[K_SPACE] and previous_space == False):

            scroll = 0                      # resets scroll for the previous reactions
            turns_to_next_cycle -= 1        # advancing a cycle
            bought_from_store = False       # resetting store
            change_list = []                # resetting change list
            previous_reactions = []         # resetting previous reaction list

            # cycles through each element for reactions
            for y, row in enumerate(deck):                  # enumerate keeps track of index without needing y += 1
                for x, element in enumerate(row):

                    # gold earnt is tracked throughout, given all at once in the end.
                    gold_earnt = gold_from(element)

                    # seeing adjacent elements
                    if element != "Empty":
                        adjacenct_list = ((x-1, y+1), (x, y+1), (x+1, y+1), (x-1, y), (x+1, y),
                                    (x-1, y-1), (x, y-1), (x+1, y-1),)
                        for adjacency in adjacenct_list:

                            # only does it for valid adjacencies (i.e. not off the map, not empty)
                            if 0 <= adjacency[1] <= 3 and 0 <= adjacency[0] <= 6:
                                elements_to_check = (deck[y][x], deck[adjacency[1]][adjacency[0]])
                                if elements_to_check[1] != "Empty":

                                    # seeing if adjacent element creates a synergy
                                    synergy_present, synergy = check_for_synergy(elements_to_check)
                                    if synergy_present:
                                        
                                        # unpacks synergy to determine products and gold
                                        reactants, products, gold_from_reaction = synergy

                                        # assumes synergy is valid. invalidates if the first element has already been consumed.
                                        valid = True
                                        for change in change_list:
                                            if change[0] == y and change[1] == x:     # seeing if the element is in the list
                                                if deck[y][x] != change[2]:           # seeing if it was used (i.e. changed)
                                                    valid = False                     # if consumed, cannot do another synergy.
                                                    break

                                        if valid:   # only valid changes are done.
                                            gold_earnt += gold_from_reaction
                                            if reactants[0] != products[0]:               # only adds the change if it changes something.
                                                change_list.append((y, x, products[0]))

                                            # seeing how the adjacent should react.
                                            if reactants[1] != products[1]:
                                                change = True
                                                for change_2 in change_list:
                                                    # if it was already consumed before, won't react.
                                                    # you can still double-use it if it always is the adjacent, never if it is the main.
                                                    if change_2[0] == adjacency[1] and change_2[1] == adjacency[0]:
                                                        change = False
                                                        break
                                                if change:
                                                    change_list.append((adjacency[1], adjacency[0], products[1]))
                                            previous_reactions.append(synergy)
                    
                    # giving gold
                    gold += gold_earnt
                    draw.add_gold(str(gold_earnt), ((90*x)+98), ((y*89)+184))
            
            for change in change_list:                  # does all changes at once at the end.
                deck[change[0]][change[1]] = change[2]

        # playing the animation for the coins and doing payment things if the turns to next cycle is 0.
        draw.gold_animation(window)
        if turns_to_next_cycle == 0:
            gold -= payment
            turns_to_next_cycle = 8
            payment += 100   
            luck += 0.5
            if gold < 0:
                break
        
        # drawing shortcuts if needed
        if show_shortcuts:
            draw.shortcuts(window)
        
        # covering up store if bought already
        if bought_from_store:
            draw.shop_curtains(window)

        # toggling shortcuts with tab
        if key[K_TAB] and not previous_tab:
            show_shortcuts = toggle(show_shortcuts)
        
        # toggling FPS display with backspace
        if key[K_BACKSPACE] and not previous_backspace:
            show_FPS = toggle(show_FPS)

        # changing statuses of buttons based on current frame to be used next frame.
        previous_click_status = True if pygame.mouse.get_pressed()[0]   else False
        previous_space        = True if key[K_SPACE]                    else False
        previous_backspace    = True if key[K_BACKSPACE]                else False
        previous_tab          = True if key[K_TAB]                      else False

        # same thing but with grid keys, longer since there are multiple
        previous_grid_key_pressed = False
        for val in list(grid_keys):
            if key[grid_keys[val]]:
                previous_grid_key_pressed = True
                break

        # getting average FPS then displaying
        tick.tick()                                 # doing this calculation even when not FPS not displayed so
        FPS_list.append(int(tick.get_fps()))        # when it is displayed, it is more accurate
        del FPS_list[0]
        average_FPS = sum(FPS_list) / len(FPS_list)

        # colored-coded FPS display
        if show_FPS:
            if average_FPS < 15:
                color = (255, 0, 0)
            elif average_FPS < 30:
                color = (255, 255, 0)
            else:
                color = (255, 255, 255)
            window.blit(font.render(f"FPS: {average_FPS}", True, color), pygame.Rect(1000, 2, 0, 0))

        fpsClock.tick(FPS)
        pygame.display.update()
    
    # upon end of game, plays end screen
    lose_screen(gold, payment)


if __name__ == "__main__":
    menu()
