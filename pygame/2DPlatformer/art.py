import pygame

# tiles are decided based on their color. this was the best way I could think to implement it based
# on how the program was made, though it does make it a bit harder to do this.
tile_art = {
    "Trampoline": (
        "          ",
        "BB      BB",
        "BBB    BBB",
        "wBBBBBBBBw",
        "w BBBBBB w",
        "w        w",
        "w        w",
        "w        w",
        "w        w",
        "w        w",
        
    ),
    "Side Trampoline": (
        "BwwwwwwwwB",
        "BB      BB",
        " BB    BB ",
        "  BB  BB  ",
        "  BBBBBB  ",
        "  BBBBBB  ",
        "  BB  BB  ",
        " BB    BB ",
        "BB      BB",
        "BwwwwwwwwB",
    ),
    "Bomb": (
        "    bb    ",
        "  nnnnnn  ",
        " nnrnnrnn ",
        "nnnrnnrnnn",
        "nnnrnnrnnn",
        "nnnnrrnnnn",
        "nnnrnnrnnn",
        "nnnrnnrnnn",
        " nnrnnrnn ",
        "  nnnnnn  ",
    ),
    "Exit": (
        "WNWNWNWNWN",
        "NWNWNWNWNW",
        "WNWNWNWNWN",
        "NWNWNWNWNW",
        "WNWNWNWNWN",
        "NWNWNWNWNW",
        "WNWNWNWNWN",
        "NWNWNWNWNW",
        "WNWNWNWNWN",
        "NWNWNWNWNW",
    )
}

color_list = (
        ("Y", (200, 200, 50)),      # Y | yellow
        ("y", (250, 250, 120)),     # y | bright yellow
        ("d", (30, 100, 30)),       # d | dark green
        ("G", (50, 250, 50)),       # G | green
        ("B", (50, 50, 250)),       # B | blue
        ("b", (150, 100, 30)),      # b | brown
        ("R", (250, 50, 50)),       # R | red
        ("r", (150, 30, 30)),       # r | dark red
        ("w", (110, 110, 110)),     # w | light gray
        ("n", (30, 30, 30)),        # n | light black
        ("W", (250, 250, 250)),     # W | white
        ("N", (10, 10, 10)),        # N | black
    )

def draw_tile(window, x, y, tile):
    if tile == "Dirt":                  # drawing dirt quick to avoid lag from too much of it.
        pygame.draw.rect(window, (150, 100, 30), pygame.Rect(x, y, 30, 30))
        return
    if tile == "Grass":                  # drawing grass quick to avoid lag from too much of it.
        pygame.draw.rect(window, (150, 100, 30), pygame.Rect(x, y, 30, 30))
        pygame.draw.rect(window, (50, 250, 50), pygame.Rect(x, y, 30, 12))
        pygame.draw.rect(window, (150, 100, 30), pygame.Rect(x+12, y+9, 12, 3))
        pygame.draw.rect(window, (50, 250, 50), pygame.Rect(x+3, y+12, 6, 3))
        return
    if tile == "Lava":                  # drawing lava quick to avoid lag from too much of it.
        pygame.draw.rect(window, (250, 50, 50), pygame.Rect(x, y+12, 30, 18))
        pygame.draw.rect(window, (250, 50, 50), pygame.Rect(x, y+6, 6, 6))
        pygame.draw.rect(window, (250, 50, 50), pygame.Rect(x+6, y+9, 3, 3))
        pygame.draw.rect(window, (250, 50, 50), pygame.Rect(x+18, y+9, 6, 3))
        pygame.draw.rect(window, (250, 50, 50), pygame.Rect(x+21, y+6, 9, 6))
        return

    icon = []                   # blank for if tile not defined.
    if tile in tile_art:        # to stop crashes
        icon = tile_art[tile]

    # looping through the whole image.
    x_ = x
    y_ = y
    for row in icon:
        for value in row:
            # picking color and drawing
            for color in color_list:
                if value == color[0]:
                    pygame.draw.rect(window, color[1], pygame.Rect(x_, y_, 3, 3))
                    break
            x_ += 3
        x_ = x
        y_ += 3
