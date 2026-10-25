

# Imagem de background do menu de título fornecida por: https://www.magnific.com/free-vector/flat-background-halloween-season_65581192.htm#fromView=search&page=1&position=4&uuid=1c3c5604-a239-43b6-b1a1-8816005d31ef&track=ais_hybrid&query=Halloween+graveyard+background

WIDTH = 1280
HEIGHT = 720
TITLE = "Crazy Halloween"

stage = "menu"


def draw():
    if stage == "menu":
        screen.clear()
        screen.blit("bg_title_screen.jpg", (0, 0))
        screen.draw.text("Crazy Halloween", (WIDTH/6, HEIGHT/4),
                            fontname="creepyhouse.otf", fontsize=120,
                            shadow=(2,2), scolor="#202020",
                            color="green", gcolor="orange",
                            align="center"
                            )