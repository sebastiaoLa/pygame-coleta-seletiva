import random
import sys
import time

import pygame
from PIL import Image
from pygame.locals import K_ESCAPE, KEYDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT, K_f

from classes import Trash,Sprite
from constants import *

class Game():
	def __init__(self, *args, **kwargs):
		pygame.init()		
		pygame.display.set_caption('Coleta Seletiva')
		self.DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT),pygame.HWSURFACE)#|pygame.DOUBLEBUF)
		self.ponto = 0

		self.trashes = {
			ORGANICO:Trash('data/images/trash/organico.png'),
			METAL:Trash('data/images/trash/metal.png'),
			PAPEL:Trash('data/images/trash/papel.png'),
			PLASTICO:Trash('data/images/trash/plastico.png'),
			VIDRO:Trash('data/images/trash/vidro.png')
		}

		self.trashBins = {
			ORGANICO:pygame.Rect(int(WIDTH*0.245),int(HEIGHT*0.68),int(WIDTH*0.055),int(HEIGHT*0.10)),
			METAL:pygame.Rect(int(HEIGHT*0.167),int(HEIGHT*0.68),int(WIDTH*0.055),int(HEIGHT*0.10)),
			PAPEL:pygame.Rect(int(HEIGHT*0.249),int(HEIGHT*0.68),int(WIDTH*0.055),int(HEIGHT*0.10)),
			PLASTICO:pygame.Rect(int(HEIGHT*0.01),int(HEIGHT*0.68),int(WIDTH*0.055),int(HEIGHT*0.10)),
			VIDRO:pygame.Rect(int(HEIGHT*0.089),int(HEIGHT*0.68),int(WIDTH*0.055),int(HEIGHT*0.10))
		}

		self.cont = 0
		self.sol = False
		self.solObjRect = pygame.Rect(int(WIDTH*0.085),int( HEIGHT*0.013 ),int(WIDTH*0.09),int(HEIGHT*0.083))
		self.nivel = 1
		self.contsol = -1
		self.mousex = 0
		self.mousey = 0
		self.mousemox = 0
		self.mousemoy  = 0
		self.jogary = 60
		self.instrucoesy = 60
		self.fps = 144
		self.click = False
		self.jogando = False
		self.clicked = False
		self.instrucoesbool = False
		self.clickagain = False
		self.ponto = 0
		self.vidas = 3

		self.fpsClock = pygame.time.Clock()
		
		
		self.fontObj = pygame.font.Font('freesansbold.ttf', 28)
		# pygame.display.toggle_fullscreen()
		self.playingorgC = Image.open('data/images/background/playing.png').resize((WIDTH,HEIGHT),Image.LANCZOS)
		self.playingorgE = Image.open('data/images/background/playing2.png').resize((WIDTH,HEIGHT),Image.LANCZOS)

		self.playing = pygame.image.fromstring(self.playingorgC.tobytes(),self.playingorgC.size,self.playingorgC.mode)

		self.menu = pygame.image.load('data/images/menu/menu1.png')

		self.jogar = Sprite(pygame.image.load('data/images/menu/jogar1.png'))
		
		self.sair = pygame.image.load('data/images/menu/sair1.png')

		self.instrucoes = Sprite(pygame.image.load('data/images/menu/instrucoes1.png'))

		self.menuObjRect = self.menu.get_rect()
		self.menuObjRect.center = (int(WIDTH*0.9),60)

		self.playingObjRect = self.playing.get_rect()
		self.playingObjRect.center = (WIDTH/2,HEIGHT/2)

		self.jogar.set_center(self.menuObjRect.center)

		self.instrucoes.set_center(self.menuObjRect.center)

		self.sairObjRect = self.sair.get_rect()
		self.sairObjRect.right = self.menuObjRect.left - 15
		self.sairObjRect.top = self.menuObjRect.top

		self.DISPLAYSURF.blit(self.playing,self.playingObjRect)
		self.DISPLAYSURF.blit(self.menu,self.menuObjRect)	
		self.jogar.draw(self.DISPLAYSURF)
		self.instrucoes.draw(self.DISPLAYSURF)
		self.DISPLAYSURF.blit(self.sair,self.sairObjRect)

		self.textSurfaceObj = self.fontObj.render("", True, RED)

		self.restart()
	
	def displayHud(self):
		pontosObj = self.fontObj.render(str(self.ponto), True, BLACK)
		vidasObj = self.fontObj.render(str(self.vidas), True, RED)
		pontosObjRect = pontosObj.get_rect()
		vidasObjRect = vidasObj.get_rect()
		pontosObjRect.topright = (700,0)
		vidasObjRect.topleft = (0,0)
		self.DISPLAYSURF.blit(pontosObj,pontosObjRect)
		self.DISPLAYSURF.blit(vidasObj,vidasObjRect)

	def game_clicked(self,mouseClkPos):
		if self.sairObjRect.collidepoint(mouseClkPos):
			if self.jogando:
				self.jogando = False
			elif self.instrucoes.clicked:
				self.instrucoes.clicked = False
			else:
				sys.exit()
				pygame.quit()
				exit()
		if self.solObjRect.collidepoint(mouseClkPos):
			textSurfaceObj = self.fontObj.render("CUIDADO, O SOL QUEIMA!!!", True, RED)
			textRectObj = textSurfaceObj.get_rect()
			self.contsol = self.cont
			self.sol = True
		if self.jogando == False and self.instrucoes.clicked == False:					
			if self.jogar.rect.collidepoint(mouseClkPos) and self.jogar.rect.center[1] >= 90:
				self.jogando = True
				soundObj = pygame.mixer.Sound('data/sounds/click.ogg')
				soundObj.play()
				
			if self.instrucoes.rect.collidepoint(mouseClkPos) and self.jogar.rect.center[1] >= 90:
				self.instrucoes.clicked = True	
				soundObj = pygame.mixer.Sound('data/sounds/click.ogg')
				soundObj.play()

			if self.menuObjRect.collidepoint(mouseClkPos):
					self.click = True
					soundObj = pygame.mixer.Sound('data/sounds/click.ogg')
					soundObj.play()

			


	def main_loop(self):
		while True: #main game loop
			millis = time.time()*1000
			self.DISPLAYSURF.blit(self.playing,self.playingObjRect)
			for event in pygame.event.get():
				mouseClkPos = (0,0)
				mouseMotPos = (0,0)
				if event.type == QUIT:
					sys.exit()
					pygame.quit()
					exit()
				if event.type == MOUSEBUTTONUP:
					mouseClkPos = event.pos
					self.game_clicked(mouseClkPos)
					if self.jogando and True in [ self.trashes[x].clicked for x in self.trashes.keys()]:
						self.clickagain = True
				elif event.type ==  MOUSEMOTION:
					mouseMotPos = event.pos
					if self.sairObjRect.collidepoint(mouseMotPos):
						self.sair = pygame.image.load('data/images/menu/sair2.png')
					else:
						self.sair = pygame.image.load('data/images/menu/sair1.png')
					if self.jogando == False and self.instrucoes.clicked == False:
						if self.menuObjRect.collidepoint(mouseMotPos):
							self.menu = pygame.image.load('data/images/menu/menu2.png')
						else:
							self.menu = pygame.image.load('data/images/menu/menu1.png')
						
						if self.jogar.rect.collidepoint(mouseMotPos):
							self.jogar.surface = pygame.image.load('data/images/menu/jogar2.png')
						else:
							self.jogar.surface = pygame.image.load('data/images/menu/jogar1.png')
						
						if self.instrucoes.rect.collidepoint(mouseMotPos):
							self.instrucoes.surface = pygame.image.load('data/images/menu/instrucoes2.png')
						else:
							self.instrucoes.surface = pygame.image.load('data/images/menu/instrucoes1.png')
					mousemox,mousemoy = mouseMotPos 
				if event.type == KEYDOWN:
					if event.key == K_f:
						pygame.display.toggle_fullscreen()
					if event.key == K_ESCAPE:
						if self.jogando:
							self.jogando = False
						elif self.instrucoes.clicked:
							self.instrucoes.clicked = False
						else:
							sys.exit()
							pygame.quit()
							exit()
					

			if self.jogar.get_center()['y'] >= 90:
					self.click = False
					self.clicked = True 
				
			if self.click == True:
				self.jogar.move(0,int(HEIGHT*0.004))
				self.instrucoes.move(0,int(HEIGHT*0.004)*2)

			if self.instrucoes.clicked == True:
				instrucoescaixa = pygame.image.load('data/images/menu/instrucoescaixa.png')
				instrucoescaixaObjRect = instrucoescaixa.get_rect()
				instrucoescaixaObjRect.center = (WIDTH/2,HEIGHT/2)
				self.DISPLAYSURF.blit(self.menu,self.menuObjRect)
				self.DISPLAYSURF.blit(instrucoescaixa,instrucoescaixaObjRect)
				if self.menuObjRect.collidepoint(mouseClkPos):
					self.instrucoes.clicked = False
					soundObj = pygame.mixer.Sound('data/sounds/click.ogg')
					soundObj.play()
					
				
				if self.menuObjRect.collidepoint(mouseMotPos):
					self.menu = pygame.image.load('data/images/menu/menu2.png')
				else:
					self.menu = pygame.image.load('data/images/menu/menu1.png')
					
			elif self.jogando: #Eis o Real Jogo
				
				if self.clickagain == True:
					for i in self.trashes.keys():
						if self.trashes[i].clicked:
							if self.trashBins[i].collidepoint(mouseClkPos):
								self.acerto()
							else: 
								self.erro()
							self.trashes[i].clicked = self.trashes[i].in_screen = False

				if self.clicked:
					for i in self.trashes:
						if self.trashes[i].in_screen:
							self.trashes[i].check_clicked(mouseClkPos)


				for i in self.trashes.keys():
					if self.trashes[i].in_screen:
						if self.trashes[i].clicked:
							self.trashes[i].move_center(mouseMotPos)
						self.trashes[i].draw(self.DISPLAYSURF)
						
				
				
				if self.ponto == 15:
					self.jogando = False
					mousex = 0
					mousey = 0
					self.restart()
					self.vidaponto()
					textSurfaceObj = self.fontObj.render("Parabens, voce venceu", True, RED)
					textRectObj = textSurfaceObj.get_rect()
					textRectObj.center = (WIDTH/2,HEIGHT/2)
					textRectObj.top = 0
					self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
					pygame.display.update()
					time.sleep(3)
					
				if self.vidas == 0:
					soundObj = pygame.mixer.Sound('data/sounds/badswap.wav')
					soundObj.play()
					self.jogando = False
					self.restart()
					self.vidaponto()
					textSurfaceObj = self.fontObj.render("Game Over", True, RED)
					textRectObj = textSurfaceObj.get_rect()
					textRectObj.center = (WIDTH/2,HEIGHT/2)
					textRectObj.top = 0
					self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
					pygame.display.update()
					time.sleep(3)
				
				if True not in [ self.trashes[x].in_screen for x in self.trashes.keys() ]:
					#jogando = False
					self.restart()
					self.nivel += 1
					nivelstr = "Nivel: "+str(self.nivel)
					textSurfaceObj = self.fontObj.render(nivelstr, True, RED)
					textRectObj = textSurfaceObj.get_rect()
					self.contsol = self.cont
					self.sol = True
			
			if self.sol==True:
				if self.cont != self.contsol+3*self.fps:
					textRectObj = textSurfaceObj.get_rect()
					textRectObj.center = (WIDTH/2,HEIGHT/2)
					textRectObj.top = 0
					self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
				else:
					self.sol = False
			if self.jogando == False and self.instrucoes.clicked == False:
				self.jogar.draw(self.DISPLAYSURF)
				self.instrucoes.draw(self.DISPLAYSURF)
				self.DISPLAYSURF.blit(self.menu,self.menuObjRect)
			
			self.DISPLAYSURF.blit(self.sair,self.sairObjRect)
			# self.DISPLAYSURF.fill(BROWN,self.trashBins[ORGANICO])
			# self.DISPLAYSURF.fill(RED,self.trashBins[PLASTICO])
			# self.DISPLAYSURF.fill(GREEN,self.trashBins[VIDRO])
			# self.DISPLAYSURF.fill(BLUE,self.trashBins[PAPEL])
			# self.DISPLAYSURF.fill(YELLOW,self.trashBins[METAL])
			pygame.display.update()
			self.cont+= 1
			# self.fpsClock.tick(self.fps)
			print 'fps:',1000/((time.time()*1000)-millis)
				

	def vidaponto(self):
		self.vidas = 3
		self.ponto = 0

	def acerto(self):
		soundObj = pygame.mixer.Sound('data/sounds/match0.wav')
		soundObj.play()
		self.ponto +=1
		self.playing = pygame.image.fromstring(self.playingorgC.tobytes(),self.playingorgC.size,self.playingorgC.mode)
		self.clickagain = False

	def erro(self):
		self.vidas = self.vidas - 1
		
		self.playing = pygame.image.fromstring(self.playingorgE.tobytes(),self.playingorgE.size,self.playingorgE.mode)
		
		self.clickagain = False

	def restart(self):

		for i in self.trashes.keys():
			test = True
			while test:
				self.trashes[i].move_center((random.randint(int(WIDTH*0.1),int(WIDTH*0.9)),random.randint(int(HEIGHT*0.85),int(HEIGHT*0.9))))
				print self.trashes[i].rect.center
				test = False
				for j in self.trashes.keys():
					if i != j:
						if self.trashes[i].rect.colliderect(self.trashes[j].rect) == 1:
							test = True
							break
			self.trashes[i].in_screen = True
			self.trashes[i].clicked = False


game = Game()
game.main_loop()
