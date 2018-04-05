"""
Mini game de reciclagem criado por @sebastiaoLa
"""

import random
import sys
import time


from PIL import Image
import pygame
from pygame.constants import (K_ESCAPE, KEYDOWN, MOUSEBUTTONUP, MOUSEMOTION,
                              QUIT, K_f)

from classes import Batch, Sprite, Text, Trash
from constants import (BLACK, FPS, HEIGHT, METAL, ORGANICO, PAPEL, PLASTICO,
                       RED, VIDRO, WHITE, WIDTH)


def sair():
    sys.exit()
    pygame.quit()
    exit()

GAME_CLOCK = pygame.time.Clock()

class Game(object):
    """Classe principal com todos os elementos do jogo"""
    def __init__(self):
        """Inicializa todas as variaveis"""
        self.animate = False
        pygame.init()
        pygame.display.set_caption('Coleta Seletiva')
        self.batch = Batch()
        self.displaysurf = pygame.display.set_mode(
            (WIDTH, HEIGHT), pygame.HWSURFACE)  # |pygame.DOUBLEBUF)
        self.ponto = 0

        self.trashes = {
            ORGANICO: Trash('data/images/trash/organico.png', self.batch),
            METAL: Trash('data/images/trash/metal.png', self.batch),
            PAPEL: Trash('data/images/trash/papel.png', self.batch),
            PLASTICO: Trash('data/images/trash/plastico.png', self.batch),
            VIDRO: Trash('data/images/trash/vidro.png', self.batch)
        }

        self.trash_bins = {
            ORGANICO: pygame.Rect(
                int(WIDTH*0.245),
                int(HEIGHT*0.68),
                int(WIDTH*0.055),
                int(HEIGHT*0.10)
            ),
            METAL: pygame.Rect(
                int(WIDTH*0.126),
                int(HEIGHT*0.68),
                int(WIDTH*0.055),
                int(HEIGHT*0.10)
            ),
            PAPEL: pygame.Rect(
                int(WIDTH*0.186),
                int(HEIGHT*0.68),
                int(WIDTH*0.055),
                int(HEIGHT*0.10)
            ),
            PLASTICO: pygame.Rect(
                int(WIDTH*0.0075),
                int(HEIGHT*0.68),
                int(WIDTH*0.055),
                int(HEIGHT*0.10)
            ),
            VIDRO: pygame.Rect(
                int(WIDTH*0.0674),
                int(HEIGHT*0.68),
                int(WIDTH*0.055),
                int(HEIGHT*0.10)
            )
        }

        self.timer = False
        self.sol_obj_rect = pygame.Rect(
            int(WIDTH*0.085),
            int(HEIGHT*0.013),
            int(WIDTH*0.09),
            int(HEIGHT*0.083)
        )
        self.nivel = 1
        self.temporizer = -1
        self.mousex = 0
        self.mousey = 0
        self.mousemox = 0
        self.mousemoy = 0
        self.jogary = 60
        self.instrucoesy = 60
        self.fps = 30
        self.click = False
        self.jogando = False
        self.clicked = False
        self.instrucoesbool = False
        self.clickagain = False
        self.ponto = 0
        self.vidas = 3

        self.text = Text()

        # pygame.display.toggle_fullscreen()
        self.playing_orig_crt = Image.open(
            'data/images/background/playing.png'
            ).resize((WIDTH, HEIGHT), Image.LANCZOS)
        self.playing_orig_err = Image.open(
            'data/images/background/playing2.png'
            ).resize((WIDTH, HEIGHT), Image.LANCZOS)

        self.playing = Sprite(
            pygame.image.fromstring(
                self.playing_orig_crt.tobytes(),
                self.playing_orig_crt.size,
                self.playing_orig_crt.mode
            ),
            self.batch
        )

        self.menu = Sprite('data/images/menu/menu1.png', self.batch)

        self.jogar = Sprite(
            pygame.image.load('data/images/menu/jogar1.png'),
            self.batch
        )

        self.sair = Sprite(
            pygame.image.load('data/images/menu/sair1.png'),
            self.batch
        )

        self.instrucoes = Sprite(
            pygame.image.load('data/images/menu/instrucoes1.png'),
            self.batch
        )

        self.menu.set_center((int(WIDTH*0.9), 60))

        self.playing.set_center((WIDTH/2, HEIGHT/2))

        self.jogar.set_center(self.menu.rect.center)

        self.instrucoes.set_center(self.menu.rect.center)

        self.sair.rect.right = self.menu.rect.left - 15
        self.sair.rect.top = self.menu.rect.top

        self.playing.draw(self.displaysurf)
        self.menu.draw(self.displaysurf)
        self.jogar.draw(self.displaysurf)
        self.instrucoes.draw(self.displaysurf)
        self.sair.draw(self.displaysurf)

        self.text_surface_obj = Text(text="", color=RED, batch=self.batch)
        self.text_surface_obj.set_center(WIDTH/2, HEIGHT/2)
        self.text_surface_obj.get_rect().top = 0

        self.pontos_obj = None
        self.vidas_obj = None
        self.fps = None
        self.restart()

    def display_hud(self):
        if not self.pontos_obj:
            self.pontos_obj = Text(str(self.ponto), BLACK, self.batch)
            self.pontos_obj.get_rect().topright = (WIDTH, 0)
        if not self.vidas_obj:
            self.vidas_obj = Text(str(self.vidas), RED, self.batch)
            self.vidas_obj.get_rect().topleft = (0, 0)

        self.pontos_obj.draw(self.displaysurf)
        self.vidas_obj.draw(self.displaysurf)

    def game_clicked(self, mouse_clk_pos):
        if self.sair.check_collide(mouse_clk_pos):
            if self.jogando:
                self.jogando = False
                self.restart()
            elif self.instrucoes.clicked:
                self.instrucoes.clicked = False
            else:
                sair()
        if not self.jogando:
            sound_obj = pygame.mixer.Sound('data/sounds/click.ogg')
            sound_obj.play()
            if not self.instrucoes.clicked:
                if (self.jogar.rect.collidepoint(mouse_clk_pos) and
                        self.jogar.rect.center[1] >= 90):
                    self.jogando = True

                if (self.instrucoes.rect.collidepoint(mouse_clk_pos) and
                        self.jogar.rect.center[1] >= 90):
                    self.instrucoes.clicked = True

                if self.menu.check_collide(mouse_clk_pos):
                    self.animate = True
            else:
                if self.menu.check_collide(mouse_clk_pos):
                    self.instrucoes.clicked = False

        elif self.jogando:
            if self.sol_obj_rect.collidepoint(mouse_clk_pos):
                self.text_surface_obj.update("CUIDADO, O SOL QUEIMA!!!")
                self.temporizer = time.time()+3
                self.timer = True
            elif True in [
                    self.trashes[x].clicked for x in self.trashes
                ]:
                for i in self.trashes:
                    if self.trashes[i].clicked:
                        if self.trash_bins[i].collidepoint(mouse_clk_pos):
                            self.acerto()
                        else:
                            self.erro()

                        self.trashes[i].clicked = False
                        self.trashes[i].in_screen = False
                        break

            for i in self.trashes:
                if (self.trashes[i].in_screen and
                        self.trashes[i].check_clicked(mouse_clk_pos)):
                    break

            if True not in [
                    self.trashes[x].in_screen for x in self.trashes
                ]:
                # jogando = False
                self.restart()
                self.nivel += 1
                self.text_surface_obj.update("Nivel: "+str(self.nivel))
                self.temporizer = time.time()+3
                self.timer = True

    def mouse_moved(self, mouse_mot_pos):
        if self.instrucoes.clicked:
            if self.menu.check_collide(mouse_mot_pos):
                self.menu.surface = pygame.image.load(
                    'data/images/menu/menu2.png')
            else:
                self.menu.surface = pygame.image.load(
                    'data/images/menu/menu1.png')
        if self.sair.check_collide(mouse_mot_pos):
            self.sair.surface = pygame.image.load('data/images/menu/sair2.png')
        else:
            self.sair.surface = pygame.image.load('data/images/menu/sair1.png')
        if self.jogando is False and self.instrucoes.clicked is False:
            if self.menu.check_collide(mouse_mot_pos):
                self.menu.surface = pygame.image.load('data/images/menu/menu2.png')
            else:
                self.menu.surface = pygame.image.load('data/images/menu/menu1.png')

            if self.jogar.rect.collidepoint(mouse_mot_pos):
                self.jogar.surface = pygame.image.load('data/images/menu/jogar2.png')
            else:
                self.jogar.surface = pygame.image.load('data/images/menu/jogar1.png')

            if self.instrucoes.rect.collidepoint(mouse_mot_pos):
                self.instrucoes.surface = pygame.image.load('data/images/menu/instrucoes2.png')
            else:
                self.instrucoes.surface = pygame.image.load('data/images/menu/instrucoes1.png')
        elif self.jogando:
            for i in self.trashes:
                if self.trashes[i].in_screen:
                    if self.trashes[i].clicked:
                        self.trashes[i].move_center(mouse_mot_pos)

    def main_loop(self):
        while True:  # main game loop
            event_happen = self.animate
            for event in pygame.event.get():
                event_happen = True
                mouse_clk_pos = (0, 0)
                mouse_mot_pos = (0, 0)
                if event.type == QUIT:
                    sair()
                if event.type == MOUSEBUTTONUP:
                    mouse_clk_pos = event.pos
                    self.game_clicked(mouse_clk_pos)
                elif event.type == MOUSEMOTION:
                    mouse_mot_pos = event.pos
                    self.mouse_moved(mouse_mot_pos)
                if event.type == KEYDOWN:
                    if event.key == K_f:
                        pygame.display.toggle_fullscreen()
                    if event.key == K_ESCAPE:
                        if self.jogando:
                            self.jogando = False
                        elif self.instrucoes.clicked:
                            self.instrucoes.clicked = False
                        else:
                            sair()

            if event_happen:
                self.playing.draw(self.displaysurf)

                if self.animate:
                    if self.jogar.get_center()['y'] >= 90:
                        self.animate = False
                    else:
                        self.jogar.move(0, int(60.0/FPS))
                        self.instrucoes.move(0, int(60.0/FPS)*2)
                
                if self.instrucoes.clicked is True:
                    instrucoescaixa = Sprite(pygame.image.load(
                        'data/images/menu/instrucoescaixa.png'), self.batch)
                    instrucoescaixa.set_center((WIDTH/2, HEIGHT/2))
                    instrucoescaixa.draw(self.displaysurf)
                    self.menu.draw(self.displaysurf)

                elif self.jogando:
                    self.display_hud()
                    for i in self.trashes:
                        if self.trashes[i].in_screen:
                            self.trashes[i].draw(self.displaysurf)

                if self.jogando is False and self.instrucoes.clicked is False:
                    self.jogar.draw(self.displaysurf)
                    self.instrucoes.draw(self.displaysurf)
                    self.menu.draw(self.displaysurf)
                self.sair.draw(self.displaysurf)

            if self.timer is True:
                if self.temporizer >= time.time():
                    self.text_surface_obj.draw(self.displaysurf)
                else:
                    self.playing.draw(self.displaysurf)
                    self.timer = False
            # self.displaysurf.fill(BROWN,self.trash_bins[ORGANICO])
            # self.displaysurf.fill(PINK,self.trash_bins[PLASTICO])
            # self.displaysurf.fill(GREEN,self.trash_bins[VIDRO])
            # self.displaysurf.fill(BLUE,self.trash_bins[PAPEL])
            # self.displaysurf.fill(YELLOW,self.trash_bins[METAL])
            # self.batch.draw()
            GAME_CLOCK.tick(FPS)
            if not self.fps:
                self.fps = Text(
                    text='fps: %.2f' % (GAME_CLOCK.get_fps()),
                    batch=self.batch,
                    size=12,
                    background=WHITE
                )
                self.fps.get_rect().bottomleft = (0, HEIGHT)
            else:
                self.fps.update('fps: %.2f' % (GAME_CLOCK.get_fps()))
            self.fps.draw(self.displaysurf)
            self.batch.draw()

    def vidaponto(self):
        self.vidas = 3
        self.ponto = 0

    def acerto(self):
        sound_obj = pygame.mixer.Sound('data/sounds/match0.wav')
        sound_obj.play()
        self.ponto += 1
        self.playing.surface = pygame.image.fromstring(
            self.playing_orig_crt.tobytes(),
            self.playing_orig_crt.size,
            self.playing_orig_crt.mode
        ).convert(self.displaysurf)
        if self.ponto == 15:
            self.jogando = False
            self.restart()
            self.vidaponto()
            self.text_surface_obj.update("Parabens, voce venceu")
            self.text_surface_obj.draw(self.displaysurf)
            self.batch.draw()
            time.sleep(3)

    def erro(self):
        self.vidas = self.vidas - 1

        self.playing.surface = pygame.image.fromstring(
            self.playing_orig_err.tobytes(),
            self.playing_orig_err.size,
            self.playing_orig_err.mode
        ).convert(self.displaysurf)
        if self.vidas == 0:
            sound_obj = pygame.mixer.Sound('data/sounds/badswap.wav')
            sound_obj.play()
            self.jogando = False
            self.restart()
            self.vidaponto()
            self.text_surface_obj.update("Game Over")
            self.text_surface_obj.draw(self.displaysurf)
            self.batch.draw()
            time.sleep(3)

    def restart(self):
        for i in self.trashes:
            test = True
            while test:
                self.trashes[i].move_center(
                    (
                        random.randint(
                            int(WIDTH*0.1),
                            int(WIDTH*0.9)
                        ),
                        random.randint(
                            int(HEIGHT*0.85),
                            int(HEIGHT*0.9)
                        )
                    )
                )
                test = False
                for j in self.trashes:
                    if i != j:
                        j_trash_rect = self.trashes[i].rect
                        i_trash_rect = self.trashes[j].rect
                        if i_trash_rect.colliderect(j_trash_rect) == 1:
                            test = True
                            break
            self.trashes[i].in_screen = True
            self.trashes[i].clicked = False

    

GAME = Game()
GAME.main_loop()
