from pgzero.builtins import Actor
from zombie import Zombie
from enemy import Enemy

TILE_SIZE = 70

TILE_MAP = {
    "p": {"image": "zombie/idle/zombie_stand"},
    "#": {"image": "tiles/purplestonemid"},
    "*": {"image": "tiles/stonecenter"},
    "b": {"image": "tiles/box"},
    "f": {"image": "tiles/signexit"},
    "s": {"image": "enemies/slime/slimegreen1"},
    "g": {"image": "enemies/ghost/ghost1"},
    "m": {"image": "enemies/bat/bat1"},
    "c": {"image": "itens/coingold"},
}


def build_level(level):
    player = None
    enemies = []
    collectibles = []
    exit_sign = None
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
    elif level == 1:
        level_map = [
            "                   ",
            "                   ",
            "                   ",
            "                   ",
            "                   ",
            "                f  ",
            "           c  ###  ",
            "        c  b       ",
            "p  cs  gb  b   c s ",
            "#########  ########",
            "*********  ********",
        ]
    elif level == 2:
        level_map = [
            "                   ",
            "                   ",
            "     c   m         ",
            " f   b   s         ",
            " #   #######    s  ",
            "              #####",
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
                center_y = y + TILE_SIZE

                if col == "p":
                    player = Zombie(
                        tile_info["image"], midbottom=(center_x, center_y)
                    )
                elif col == "s":
                    slime = Enemy(
                        "slime/slimegreen",
                        tile_info["image"],
                        patrol_range=100,
                        midbottom=(center_x, center_y),
                    )
                    enemies.append(slime)
                elif col == "g":
                    ghost = Enemy(
                        "ghost/ghost",
                        tile_info["image"],
                        patrol_range=140,
                        num_frames=2,
                        midbottom=(center_x, center_y),
                    )
                    enemies.append(ghost)
                elif col == "m":
                    bat = Enemy(
                        "bat/bat",
                        tile_info["image"],
                        patrol_range=200,
                        midbottom=(center_x, center_y),
                    )
                    enemies.append(bat)
                elif col == "c":
                    coin = Actor(tile_info["image"], topleft=(x, y))
                    collectibles.append(coin)
                elif col == "f":
                    exit_sign = Actor(tile_info["image"], topleft=(x, y))
                else:
                    tile = {
                        "actor": Actor(tile_info["image"], topleft=(x, y)),
                    }
                    tiles.append(tile)

    return tiles, player, enemies, collectibles, exit_sign
