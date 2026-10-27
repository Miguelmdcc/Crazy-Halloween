import math
from pgzero.builtins import Rect
from levels import build_fase
from zombie import Zombie

# Imagem de background do menu de título fornecida por:
# https://www.magnific.com/free-vector/flat-background-halloween-season_65581192.htm#fromView=search&page=1&position=4&uuid=1c3c5604-a239-43b6-b1a1-8816005d31ef&track=ais_hybrid&query=Halloween+graveyard+background
# Musicas utilizadas fornecidas por:
# https://pixabay.com/music/search/halloween%20cartoon/

WIDTH = 1280
HEIGHT = 720

TITLE = "Crazy Halloween"

RED = 200, 0, 0
DARK_RED = 160, 0, 0
GREEN = 0, 200, 0
DARK_GREEN = 0, 160, 0
BLACK = 0, 0, 0

stage = "menu"
is_music_on = True

tempo_animacao = 0

level = 0

gravidade = 0.8

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
collectables = []
signexit = None
win = False


def update(dt):
    global tempo_animacao, win
    tempo_animacao += 0.05
    if stage == "running" and player:
        walking = False
        if keyboard.left and not win:
            player.walking(-1, tiles)
            walking = True
        if keyboard.right and not win:
            player.walking(1, tiles)
            walking = True
        if keyboard.up and not win:
            player.jump()
        if not walking and player.on_ground and not win:
            player.set_state("idle")
        if walking and player.on_ground and not win:
            player.set_state("walk")
        if not player.on_ground and not win:
            player.set_state("jump")
        for coin in collectables[:]:
            if player.colliderect(coin):
                player.coins += 1
                collectables.remove(coin)
        if not win and player.colliderect(signexit):
            win = True
            player.cheer()
            clock.schedule(up_level, 2)

        player.update_animation(dt)
        player.update_physics(tiles)


def up_level():
    global level, stage, win, tiles, player, enemies, collectables, signexit
    level += 1
    if level == 1:
        music.play("halloween_level_2_music")
    if level == 2:
        music.play("halloween_final_level_music")
    if level > 2:
        stage = "fim"
        level = 0
        win = False
    else:
        coins = player.coins
        tiles, player, enemies, collectables, signexit = build_fase(level)
        player.coins = coins
        win = False


def draw():
    screen.clear()
    if stage == "menu":
        screen.blit("title_screen/bg_title_screen.jpg", (0, 0))
        flutuacao_y = math.sin(tempo_animacao) * 10
        screen.draw.text(
            "Crazy Halloween",
            midbottom=(WIDTH / 2, 250 + flutuacao_y),
            fontname="creepyhouse.otf",
            fontsize=120,
            shadow=(2, 2),
            scolor="#202020",
            color="green",
            gcolor="orange",
            align="center",
        )
        title_box.midbottom = (WIDTH / 2, 250 + flutuacao_y)

        screen.draw.filled_rect(play_box, play_box_color)
        screen.draw.rect(play_box, BLACK)
        screen.draw.textbox(
            "Começar Aventura!",
            play_box,
            fontname="kenneyfuture.ttf",
            color="black",
        )
        screen.draw.filled_rect(quit_box, quit_box_color)
        screen.draw.rect(quit_box, BLACK)
        screen.draw.textbox(
            "Sair", quit_box, fontname="kenneyfuture.ttf", color="black"
        )
        if is_music_on:
            screen.blit(
                "title_screen/check_square_color_checkmark.png",
                (WIDTH - 150, HEIGHT - 150),
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
        else:
            screen.blit(
                "title_screen/check_square_color.png",
                (WIDTH - 150, HEIGHT - 150),
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
    if stage == "loading":
        screen.blit("title_screen/bg_title_screen.jpg", (0, 0))
        flutuacao_y = math.sin(tempo_animacao) * 10
        screen.draw.text(
            "Saindo da tumba...",
            midbottom=(WIDTH / 2, HEIGHT / 2 + flutuacao_y),
            fontname="creepyhouse.otf",
            fontsize=120,
            shadow=(2, 2),
            scolor="#202020",
            color="green",
            gcolor="orange",
            align="center",
        )
    if stage == "running":
        screen.blit("level/skyboxnight.png", (0, 0))
        if player.life == 2:
            screen.blit("hud/hud_heartfull", (20, 20))
        if player.life == 1:
            screen.blit("hud/hud_hearhalf", (20, 20))
        if player.life == 0:
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
            signexit.draw()
            player.draw()
            for tile in tiles:
                tile["actor"].draw()
            for enemy in enemies:
                enemy.draw()
            for coin in collectables:
                coin.draw()
    if stage == "fim":
        screen.blit("title_screen/bg_title_screen.jpg", (0, 0))
        flutuacao_y = math.sin(tempo_animacao) * 10
        screen.draw.text(
            "De volta para a tumba...",
            midbottom=(WIDTH / 2, 250 + flutuacao_y),
            fontname="creepyhouse.otf",
            fontsize=120,
            shadow=(2, 2),
            scolor="#202020",
            color="green",
            gcolor="orange",
            align="center",
        )
        title_box.midbottom = (WIDTH / 2, 250 + flutuacao_y)

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
        if is_music_on:
            screen.blit(
                "title_screen/check_square_color_checkmark.png",
                (WIDTH - 150, HEIGHT - 150),
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
        else:
            screen.blit(
                "title_screen/check_square_color.png",
                (WIDTH - 150, HEIGHT - 150),
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
    global stage, tiles, player, enemies, collectables, signexit
    tiles, player, enemies, collectables, signexit = build_fase(level)
    stage = "running"
    if is_music_on:
        music.play("halloween_level_music")


def on_mouse_down(pos, button):
    global stage, is_music_on

    if stage == "menu" or stage == "fim":
        if button == mouse.LEFT:
            if play_box.collidepoint(pos):
                print("game")
                if is_music_on:
                    sounds.click_a.play()
                stage = "loading"
                clock.schedule(run_game, 3)
            if quit_box.collidepoint(pos):
                print("exit")
                if is_music_on:
                    sounds.click_a.play()
                exit()
            if music_box.collidepoint(pos):
                if is_music_on:
                    if is_music_on:
                        sounds.switch_a.play()
                    is_music_on = False
                    music.pause()
                else:
                    sounds.switch_a.play()
                    is_music_on = True
                    music.unpause()
            if title_box.collidepoint(pos):
                if is_music_on:
                    sounds.crazyhalloween.play()


def on_mouse_move(pos):
    global play_box_color, quit_box_color, play_hovered, quit_hovered
    if stage == "menu" or stage == "fim":
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
