from pgzero.builtins import Actor
from zombie import Zombie

TILE_SIZE = 70

TILE_MAP = {
    "p": {"image": "zombie/idle/zombie_stand.png"},
    "#": {"image": "tiles/purplestonemid.png"},
    "*": {"image": "tiles/stonecenter.png"},
    "b": {"image": "tiles/box.png"},
    "e": {"image": "enemies/slime/slimegreen.png"},
    "f": {"image": "tiles/signexit.png"},
    "c": {"image": "itens/coingold.png"},
}
player = None
enemies = []


def build_fase(level):
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
            "         c         ",
            "       c b         ",
            "p      b b    e  f ",
            "###################",
            "*******************",
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
                elif col == "e":
                    enemy = Actor(
                        tile_info["image"], midbottom=(center_x, center_y)
                    )
                    enemy.anchor = ("center", "bottom")
                    enemies.append(enemy)
                else:
                    tile = {
                        "actor": Actor(tile_info["image"], topleft=(x, y)),
                    }
                    tiles.append(tile)

    return tiles, player, enemies
