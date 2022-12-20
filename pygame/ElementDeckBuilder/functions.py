import pygame

def mouse_rect():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse = pygame.Rect(mouse_x, mouse_y, 1, 1)
    return mouse

def playthrough_information(payment_reached, gold_left):
    # getting game info
    payment_lost_at = int((payment_reached/100)-1)
    total_gold_earnt = 50*(payment_lost_at**2 + payment_lost_at) + gold_left     # quadratic equation

    # getting rank
    score_list = (
        (0, 250, "F", (255, 0, 0)),
        (251, 1000, "D", (200, 50, 50)),
        (1001, 3000, "C", (200, 100, 0)),
        (3001, 10000, "B", (100, 100, 0)),
        (10001, 50000, "A", (0, 240, 0)),
        (50001, 175000, "S", (240, 180, 0)),
        (175001, 300000, "SS", (240, 220, 0)),
    )
    # first seeing the if top and bottom ranks
    if total_gold_earnt > 300000:
        rank = "SSS"
        rank_color = (255, 255, 0)
    elif total_gold_earnt < 0:
        rank = "FFF"
        rank_color = (100, 0, 0)
    for score in score_list:
        if score[0] <= total_gold_earnt <= score[1]:
            rank = score[2]
            rank_color = score[3]
            break
    return gold_left, rank, rank_color, payment_reached, total_gold_earnt

def toggle(variable):
    if variable:
            return False
    else:
        return True

def first_empty_slot_in(deck):
    # cycles through deck
    for y, row in enumerate(deck):
        for x, element in enumerate(row):
            # returns cell if it is empty
            if element == "Empty":
                return (y, x)