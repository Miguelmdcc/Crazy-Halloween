from pgzero.builtins import Actor

TILE_SIZE = 70

TILE_MAP = {
    "p": {"image": "zombie/zombie_idle.png"},
    "#": {"image": "tiles/purplestonemid.png"},
    "*": {"image": "tiles/stonecenter.png"},
}
player = None


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
            "                   ",
            "                   ",
            "p                  ",
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
                    player = Actor(
                        tile_info["image"], midbottom=(center_x, center_y)
                    )
                    player.anchor = ("center", "bottom")
                else:
                    tile = {
                        "actor": Actor(tile_info["image"], topleft=(x, y)),
                    }
                    tiles.append(tile)

    return tiles, player
