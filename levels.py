from pgzero.builtins import Actor
from zombie import Zombie

TILE_SIZE = 70

TILE_MAP = {
    "p": {"image": "zombie/idle/zombie_stand.png"},
    "#": {"image": "tiles/purplestonemid.png"},
    "*": {"image": "tiles/stonecenter.png"},
    "b": {"image": "tiles/box.png"},
    "f": {"image": "tiles/signexit.png"},
    "s": {"image": "enemies/slime/slimegreen.png"},
    "g": {"image": "enemies/ghost/ghost.png"},
    "m": {"image": "enemies/bat/bat.png"},
    "c": {"image": "itens/coingold.png"},
}


def build_fase(level):
    player = None
    enemies = []
    collectables = []
    signexit = None
    # x_tiles_count = 1280/70 = 19
    # y_tiles_count = 720/70 = 11
    tiles = []
    if level == 0:
        level_map = [
            "                   ",
            "                   ",
            "                   ",
            "                   ",
            "                   ",
            "                   ",
            "          c        ",
            "       c  b        ",
            "p      b  b   s  f ",
            "###################",
            "*******************",
        ]
    if level == 1:
        level_map = [
            "                   ",
            "                   ",
            "                   ",
            "                   ",
            "                   ",
            "     m          f  ",
            "           c  ###  ",
            "        c  b       ",
            "p  cs  gb  b   c s ",
            "#########  ########",
            "*********  ********",
        ]
    if level == 2:
        level_map = [
            "                   ",
            "                   ",
            "     c   m         ",
            " f   b     s       ",
            " #   #######    s  ",
            "              ###  ",
            "             c     ",
            "        c ####     ",
            "p      gb          ",
            "###  ##############",
            "***  **************",
        ]

    for line_idx, line in enumerate(level_map):
        for col_idx, col in enumerate(line):
            if col in TILE_MAP:
                x = col_idx * TILE_SIZE
                y = line_idx * TILE_SIZE
                tile_info = TILE_MAP[col]

                center_x = x + (TILE_SIZE / 2)
                center_y = y + (TILE_SIZE)

                if col == "p":
                    player = Zombie(
                        tile_info["image"], midbottom=(center_x, center_y)
                    )
                elif col == "s":
                    slime = Actor(
                        tile_info["image"], midbottom=(center_x, center_y)
                    )
                    slime.anchor = ("center", "bottom")
                    enemies.append(slime)
                elif col == "g":
                    ghost = Actor(
                        tile_info["image"], midbottom=(center_x, center_y)
                    )
                    ghost.anchor = ("center", "bottom")
                    enemies.append(ghost)
                elif col == "m":
                    bat = Actor(
                        tile_info["image"], midbottom=(center_x, center_y)
                    )
                    bat.anchor = ("center", "bottom")
                    enemies.append(bat)
                elif col == "c":
                    coin = Actor(tile_info["image"], topleft=(x, y))
                    collectables.append(coin)
                elif col == "f":
                    signexit = Actor(tile_info["image"], topleft=(x, y))
                else:
                    tile = {
                        "actor": Actor(tile_info["image"], topleft=(x, y)),
                    }
                    tiles.append(tile)

    return tiles, player, enemies, collectables, signexit
