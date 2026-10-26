import math
from pgzero.builtins import Rect

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


def update():
    global tempo_animacao
    tempo_animacao += 0.05


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
        music.stop()


def run_game():
    global stage
    stage = "running"


def on_mouse_down(pos, button):
    global stage, is_music_on

    if stage == "menu":
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
    if stage == "menu":
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
