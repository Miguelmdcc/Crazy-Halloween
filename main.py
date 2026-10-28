import math
from pgzero.builtins import Rect
from levels import build_level

WIDTH = 1280
HEIGHT = 720
TITLE = "Crazy Halloween"

RED = (200, 0, 0)
DARK_RED = (160, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 160, 0)
BLACK = (0, 0, 0)

stage = "menu"
is_music_on = True
animation_time = 0
level = 0

play_box = Rect((0, 0), (400, 80))
play_box.midbottom = (WIDTH / 2, HEIGHT / 2)
play_box_color = GREEN
play_hovered = False

quit_box = Rect((0, 0), (400, 80))
quit_box.midbottom = (WIDTH / 2, (HEIGHT / 2) + 100)
quit_box_color = RED
quit_hovered = False

title_box = Rect((0, 0), (910, 110))
music_box = Rect(((WIDTH - 150, HEIGHT - 150)), (32, 32))

music.play("halloween_title_music")

player = None
tiles = []
enemies = []
collectibles = []
exit_sign = None
win = False


def update(dt):
    global animation_time, win, level, player, tiles, enemies, collectibles, exit_sign, stage

    animation_time += 0.05

    if stage == "running" and player:
        walking = False

        # Fall into gap check
        if player.top > HEIGHT:
            level = 0
            tiles, player, enemies, collectibles, exit_sign = build_level(
                level
            )
            if is_music_on:
                music.play("halloween_level_music")
            return

        # Player inputs
        if keyboard.left and not win:
            player.walking(-1, tiles)
            walking = True
        if keyboard.right and not win:
            player.walking(1, tiles)
            walking = True
        if keyboard.up and not win:
            player.jump()

        # State updates
        if not walking and player.on_ground and not win:
            player.set_state("idle")
        if walking and player.on_ground and not win:
            player.set_state("walk")
        if not player.on_ground and not win:
            player.set_state("jump")

        # Collectibles logic
        for coin in collectibles[:]:
            if player.colliderect(coin):
                player.coins += 1
                if is_music_on:
                    sounds.coin.play()
                collectibles.remove(coin)

        # Level exit logic
        if not win and player.colliderect(exit_sign):
            win = True
            player.cheer()
            clock.schedule(up_level, 2)

        # Enemies update and collision logic
        for enemy in enemies[:]:
            enemy.update_enemy(dt)

            if enemy.should_remove:
                enemies.remove(enemy)
                continue

            if not win and not enemy.is_dead and player.colliderect(enemy):
                is_falling = player.vel_y > 0
                is_above = (player.bottom - player.vel_y) <= (enemy.top + 20)

                if is_falling and is_above and enemy.can_be_squished:
                    enemy.squish()
                    player.vel_y = -12
                    if is_music_on:
                        sounds.hit.play()
                else:
                    if not player.is_hurt:
                        player.take_damage(enemy.x)
                        if is_music_on:
                            sounds.switch_a.play()

                        if player.life <= 0:
                            level = 0
                            tiles, player, enemies, collectibles, exit_sign = (
                                build_level(level)
                            )
                            if is_music_on:
                                music.play("halloween_level_music")

        player.update_animation(dt)
        player.update_physics(tiles)


def up_level():
    global level, stage, win, tiles, player, enemies, collectibles, exit_sign

    level += 1
    if level == 1 and is_music_on:
        music.play("halloween_level_2_music")
    elif level == 2 and is_music_on:
        music.play("halloween_final_level_music")

    if level > 2:
        stage = "end"
        level = 0
        win = False
    else:
        saved_coins = player.coins
        tiles, player, enemies, collectibles, exit_sign = build_level(level)
        player.coins = saved_coins
        win = False


def draw():
    screen.clear()

    if stage == "menu":
        screen.blit("title_screen/bg_title_screen.jpg", (0, 0))
        y_float = math.sin(animation_time) * 10

        screen.draw.text(
            "Crazy Halloween",
            midbottom=(WIDTH / 2, 250 + y_float),
            fontname="creepyhouse.otf",
            fontsize=120,
            shadow=(2, 2),
            scolor="#202020",
            color="green",
            gcolor="orange",
            align="center",
        )
        title_box.midbottom = (WIDTH / 2, 250 + y_float)

        screen.draw.filled_rect(play_box, play_box_color)
        screen.draw.rect(play_box, BLACK)
        screen.draw.textbox(
            "Iniciar Aventura!",
            play_box,
            fontname="kenneyfuture.ttf",
            color="black",
        )

        screen.draw.filled_rect(quit_box, quit_box_color)
        screen.draw.rect(quit_box, BLACK)
        screen.draw.textbox(
            "Sair", quit_box, fontname="kenneyfuture.ttf", color="black"
        )

        checkbox_img = (
            "check_square_color_checkmark.png"
            if is_music_on
            else "check_square_color.png"
        )
        screen.blit(
            f"title_screen/{checkbox_img}", (WIDTH - 150, HEIGHT - 150)
        )
        screen.draw.text(
            "Musica e Sons",
            midbottom=(WIDTH - 135, HEIGHT - 90),
            fontname="kenneyfuture.ttf",
            fontsize=15,
            shadow=(2, 2),
            scolor="#202020",
            color="white",
        )

    elif stage == "loading":
        screen.blit("title_screen/bg_title_screen.jpg", (0, 0))
        y_float = math.sin(animation_time) * 10
        screen.draw.text(
            "Saindo da tumba...",
            midbottom=(WIDTH / 2, HEIGHT / 2 + y_float),
            fontname="creepyhouse.otf",
            fontsize=120,
            shadow=(2, 2),
            scolor="#202020",
            color="green",
            gcolor="orange",
            align="center",
        )

    elif stage == "running":
        screen.blit("level/skyboxnight.png", (0, 0))

        if player.life == 2:
            screen.blit("hud/hud_heartfull", (20, 20))
        elif player.life == 1:
            screen.blit("hud/hud_hearthalf", (20, 20))
        elif player.life == 0:
            screen.blit("hud/hud_heartempty", (20, 20))

        screen.blit("hud/hud_coins", (20, 80))
        screen.blit(f"hud/hud_{player.coins}", (80, 85))

        if level == 0:
            screen.blit(
                "level/keyboard_arrows_horizontal.png", (WIDTH / 4, HEIGHT / 4)
            )
            screen.draw.text(
                "Movimentar!",
                fontname="kenneyfuture.ttf",
                fontsize=20,
                color="white",
                midbottom=(WIDTH / 4 + 40, HEIGHT / 4 + 100),
            )
            screen.blit(
                "level/keyboard_arrows_up.png", (WIDTH / 2, HEIGHT / 4)
            )
            screen.draw.text(
                "Pular!",
                fontname="kenneyfuture.ttf",
                fontsize=20,
                color="white",
                midbottom=(WIDTH / 2 + 40, HEIGHT / 4 + 100),
            )

        if player:
            exit_sign.draw()
            player.draw()
            for tile in tiles:
                tile["actor"].draw()
            for enemy in enemies:
                enemy.draw()
            for coin in collectibles:
                coin.draw()

    elif stage == "end":
        screen.blit("title_screen/bg_title_screen.jpg", (0, 0))
        y_float = math.sin(animation_time) * 10

        screen.draw.text(
            "De volta para a tumba...",
            midbottom=(WIDTH / 2, 250 + y_float),
            fontname="creepyhouse.otf",
            fontsize=120,
            shadow=(2, 2),
            scolor="#202020",
            color="green",
            gcolor="orange",
            align="center",
        )
        title_box.midbottom = (WIDTH / 2, 250 + y_float)

        screen.draw.filled_rect(play_box, play_box_color)
        screen.draw.rect(play_box, BLACK)
        screen.draw.textbox(
            "Jogar novamente!",
            play_box,
            fontname="kenneyfuture.ttf",
            color="black",
        )

        screen.draw.filled_rect(quit_box, quit_box_color)
        screen.draw.rect(quit_box, BLACK)
        screen.draw.textbox(
            "Sair", quit_box, fontname="kenneyfuture.ttf", color="black"
        )

        checkbox_img = (
            "check_square_color_checkmark.png"
            if is_music_on
            else "check_square_color.png"
        )
        screen.blit(
            f"title_screen/{checkbox_img}", (WIDTH - 150, HEIGHT - 150)
        )
        screen.draw.text(
            "Musica e Sons",
            midbottom=(WIDTH - 135, HEIGHT - 90),
            fontname="kenneyfuture.ttf",
            fontsize=15,
            shadow=(2, 2),
            scolor="#202020",
            color="white",
        )


def run_game():
    global stage, tiles, player, enemies, collectibles, exit_sign
    tiles, player, enemies, collectibles, exit_sign = build_level(level)
    stage = "running"
    if is_music_on:
        music.play("halloween_level_music")


def on_mouse_down(pos, button):
    global stage, is_music_on

    if stage in ("menu", "end") and button == mouse.LEFT:
        if play_box.collidepoint(pos):
            if is_music_on:
                sounds.click_a.play()
            stage = "loading"
            clock.schedule(run_game, 3)

        elif quit_box.collidepoint(pos):
            if is_music_on:
                sounds.click_a.play()
            exit()

        elif music_box.collidepoint(pos):
            if is_music_on:
                sounds.switch_a.play()
                is_music_on = False
                music.pause()
            else:
                sounds.switch_a.play()
                is_music_on = True
                music.unpause()

        elif title_box.collidepoint(pos) and is_music_on:
            sounds.crazyhalloween.play()


def on_mouse_move(pos):
    global play_box_color, quit_box_color, play_hovered, quit_hovered

    if stage in ("menu", "end"):
        if play_box.collidepoint(pos):
            play_box_color = DARK_GREEN
            if not play_hovered:
                if is_music_on:
                    sounds.click_a.play()
                play_hovered = True
        else:
            play_box_color = GREEN
            play_hovered = False

        if quit_box.collidepoint(pos):
            quit_box_color = DARK_RED
            if not quit_hovered:
                if is_music_on:
                    sounds.click_a.play()
                quit_hovered = True
        else:
            quit_box_color = RED
            quit_hovered = False
