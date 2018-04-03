import random
import sys
import time

import pygame
from PIL import Image
from pygame.locals import K_ESCAPE, KEYDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT, K_f

from classes import Trash,Sprite,Batch,Text
from constants import *

class Game():
	def __init__(self, *args, **kwargs):
		self.animate = False
		pygame.init()		
		pygame.display.set_caption('Coleta Seletiva')
		self.batch = Batch()
		self.DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT),pygame.HWSURFACE)#|pygame.DOUBLEBUF)
		self.ponto = 0

		self.trashes = {
			ORGANICO:Trash('data/images/trash/organico.png',self.batch),
			METAL:Trash('data/images/trash/metal.png',self.batch),
			PAPEL:Trash('data/images/trash/papel.png',self.batch),
			PLASTICO:Trash('data/images/trash/plastico.png',self.batch),
			VIDRO:Trash('data/images/trash/vidro.png',self.batch)
		}

		self.trashBins = {
			ORGANICO:pygame.Rect(int(WIDTH*0.245),int(HEIGHT*0.68),int(WIDTH*0.055),int(HEIGHT*0.10)),
			METAL:pygame.Rect(int(WIDTH*0.126),int(HEIGHT*0.68),int(WIDTH*0.055),int(HEIGHT*0.10)),
			PAPEL:pygame.Rect(int(WIDTH*0.186),int(HEIGHT*0.68),int(WIDTH*0.055),int(HEIGHT*0.10)),
			PLASTICO:pygame.Rect(int(WIDTH*0.0075),int(HEIGHT*0.68),int(WIDTH*0.055),int(HEIGHT*0.10)),
			VIDRO:pygame.Rect(int(WIDTH*0.0674),int(HEIGHT*0.68),int(WIDTH*0.055),int(HEIGHT*0.10))
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
		self.fps = 30
		self.click = False
		self.jogando = False
		self.clicked = False
		self.instrucoesbool = False
		self.clickagain = False
		self.ponto = 0
		self.vidas = 3

		self.fpsClock = pygame.time.Clock()
		
		self.text = Text()
		
		# pygame.display.toggle_fullscreen()
		self.playingorgC = Image.open('data/images/background/playing.png').resize((WIDTH,HEIGHT),Image.LANCZOS)
		self.playingorgE = Image.open('data/images/background/playing2.png').resize((WIDTH,HEIGHT),Image.LANCZOS)

		self.playing = Sprite(pygame.image.fromstring(self.playingorgC.tobytes(),self.playingorgC.size,self.playingorgC.mode),self.batch)

		self.menu = Sprite('data/images/menu/menu1.png',self.batch)

		self.jogar = Sprite(pygame.image.load('data/images/menu/jogar1.png'),self.batch)
		
		self.sair = Sprite(pygame.image.load('data/images/menu/sair1.png'),self.batch)

		self.instrucoes = Sprite(pygame.image.load('data/images/menu/instrucoes1.png'),self.batch)

		self.menu.set_center((int(WIDTH*0.9),60))
		
		self.playing.set_center((WIDTH/2,HEIGHT/2))

		self.jogar.set_center(self.menu.rect.center)

		self.instrucoes.set_center(self.menu.rect.center)

		self.sair.rect.right, self.sair.rect.top = self.menu.rect.left - 15, self.menu.rect.top

		self.playing.draw(self.DISPLAYSURF)
		self.menu.draw(self.DISPLAYSURF)
		self.jogar.draw(self.DISPLAYSURF)
		self.instrucoes.draw(self.DISPLAYSURF)
		self.sair.draw(self.DISPLAYSURF)

		self.textSurfaceObj = Text(text="",color=RED,batch=self.batch)
		self.textSurfaceObj.set_center(WIDTH/2,HEIGHT/2)
		self.textSurfaceObj.get_rect().top = 0

		self.pontosObj = None
		self.vidasObj = None

		self.restart()

	
	def displayHud(self):
		if not self.pontosObj:
			self.pontosObj = Text(str(self.ponto),BLACK,self.batch)
			self.pontosObj.get_rect().topright = (WIDTH,0)
		if not self.vidasObj:
			self.vidasObj = Text(str(self.vidas),RED,self.batch)
			self.vidasObj.get_rect().topleft = (0,0)
			
		self.pontosObj.draw(self.DISPLAYSURF)
		self.vidasObj.draw(self.DISPLAYSURF)

	def game_clicked(self,mouseClkPos):
		if self.sair.check_collide(mouseClkPos):
			if self.jogando:
				self.jogando = False
				self.restart()
			elif self.instrucoes.clicked:
				self.instrucoes.clicked = False
			else:
				sys.exit()
				pygame.quit()
				exit()rue
		if not self.jogando:
			soundObj = pygame.mixer.Sound('data/sounds/click.ogg')
			soundObj.play()
			if self.instrucoes.clicked == False:						
				if self.jogar.rect.collidepoint(mouseClkPos) and self.jogar.rect.center[1] >= 90:
					self.jogando = True

				if self.instrucoes.rect.collidepoint(mouseClkPos) and self.jogar.rect.center[1] >= 90:
					self.instrucoes.clicked = True	

				if self.menu.check_collide(mouseClkPos):
					self.click = True
			else::
				if self.menu.check_collide(mouseClkPos):
					self.instrucoes.clicked = False

		elif self.jogando:	
			if self.solObjRect.collidepoint(mouseClkPos):
				self.textSurfaceObj.update("CUIDADO, O SOL QUEIMA!!!")
				self.contsol = self.cont
				self.sol = T
			elif True in [ self.trashes[x].clicked for x in self.trashes.keys()]:
				for i in self.trashes.keys():
					if self.trashes[i].clicked:
						if self.trashBins[i].collidepoint(mouseClkPos):
							self.acerto()
						else: 
							self.erro()
						self.trashes[i].clicked = self.trashes[i].in_screen = False
						break

		

	def mouse_moved(self,mouseMotPos):
		if self.instrucoes.clicked:
			if self.menu.check_collide(mouseMotPos):
				self.menu.surface = pygame.image.load('data/images/menu/menu2.png')
			else:
				self.menu.surface = pygame.image.load('data/images/menu/menu1.png')
		if self.sair.check_collide(mouseMotPos):
			self.sair.surface = pygame.image.load('data/images/menu/sair2.png')
		else:
			self.sair.surface = pygame.image.load('data/images/menu/sair1.png')
		if self.jogando == False and self.instrucoes.clicked == False:
			if self.menu.check_collide(mouseMotPos):
				self.menu.surface = pygame.image.load('data/images/menu/menu2.png')
			else:
				self.menu.surface = pygame.image.load('data/images/menu/menu1.png')
			
			if self.jogar.rect.collidepoint(mouseMotPos):
				self.jogar.surface = pygame.image.load('data/images/menu/jogar2.png')
			else:
				self.jogar.surface = pygame.image.load('data/images/menu/jogar1.png')
			
			if self.instrucoes.rect.collidepoint(mouseMotPos):
				self.instrucoes.surface = pygame.image.load('data/images/menu/instrucoes2.png')
			else:
				self.instrucoes.surface = pygame.image.load('data/images/menu/instrucoes1.png')
		elif self.jogando:
			for i in self.trashes.keys():
				if self.trashes[i].in_screen:
					if self.trashes[i].clicked:
						self.trashes[i].move_center(mouseMotPos)


	def main_loop(self):
		while True: #main game loop
			millis = time.time()*1000
			eventHappen = False if not self.animate else True
			for event in pygame.event.get():
				eventHappen = True
				mouseClkPos = (0,0)
				mouseMotPos = (0,0)
				if event.type == QUIT:
					sys.exit()
					pygame.quit()
					exit()
				if event.type == MOUSEBUTTONUP:
					mouseClkPos = event.pos
					self.game_clicked(mouseClkPos)
				elif event.type ==  MOUSEMOTION:
					mouseMotPos = event.pos
					self.mouse_moved(mouseMotPos)
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
					
			if self.animate:
				if self.jogar.get_center()['y'] >= 90:
					self.animate = False
				else:
					self.jogar.move(0,int(HEIGHT*0.004))
					self.instrucoes.move(0,int(HEIGHT*0.004)*2)

			if eventHappen:
				self.playing.draw(self.DISPLAYSURF)
				
				if self.instrucoes.clicked == True:
					instrucoescaixa = Sprite(pygame.image.load('data/images/menu/instrucoescaixa.png'),self.batch)
					instrucoescaixa.set_center((WIDTH/2,HEIGHT/2))
					instrucoescaixa.draw(self.DISPLAYSURF)
					self.menu.draw(self.DISPLAYSURF)
						
				elif self.jogando: 
					for i in self.trashes.keys():
						if self.trashes[i].in_screen:
							self.trashes[i].draw(self.DISPLAYSURF)
							
					if True not in [ self.trashes[x].in_screen for x in self.trashes.keys() ]:
						#jogando = False
						self.restart()
						self.nivel += 1
						self.textSurfaceObj.update("Nivel: "+str(self.nivel))
						self.contsol = self.cont
						self.sol = True
				
				if self.sol==True:
					if self.cont != self.contsol+3*self.fps:
						self.textSurfaceObj.draw(self.DISPLAYSURF)
					else:
						self.sol = False
				if self.jogando == False and self.instrucoes.clicked == False:
					self.jogar.draw(self.DISPLAYSURF)
					self.instrucoes.draw(self.DISPLAYSURF)
					self.menu.draw(self.DISPLAYSURF)
				
				self.sair.draw(self.DISPLAYSURF)
				self.batch.draw()
			
			# self.DISPLAYSURF.fill(BROWN,self.trashBins[ORGANICO])
			# self.DISPLAYSURF.fill(PINK,self.trashBins[PLASTICO])
			# self.DISPLAYSURF.fill(GREEN,self.trashBins[VIDRO])
			# self.DISPLAYSURF.fill(BLUE,self.trashBins[PAPEL])
			# self.DISPLAYSURF.fill(YELLOW,self.trashBins[METAL])
			# self.batch.draw()
			self.cont+= 1
			self.fpsClock.tick(self.fps)
			print 'fps:',1000/((time.time()*1000)-millis)
				

	def vidaponto(self):
		self.vidas = 3
		self.ponto = 0

	def acerto(self):
		soundObj = pygame.mixer.Sound('data/sounds/match0.wav')
		soundObj.play()
		self.ponto +=1
		self.playing.surface = pygame.image.fromstring(self.playingorgC.tobytes(),self.playingorgC.size,self.playingorgC.mode)
		if self.ponto == 15:
			self.jogando = False
			mousex = 0
			mousey = 0
			self.restart()
			self.vidaponto()
			self.textSurfaceObj.update("Parabens, voce venceu")
			self.textSurfaceObj.draw(self.DISPLAYSURF)
			self.batch.draw()
			time.sleep(3)

	def erro(self):
		self.vidas = self.vidas - 1
		
		self.playing.surface = pygame.image.fromstring(self.playingorgE.tobytes(),self.playingorgE.size,self.playingorgE.mode)
		if self.vidas == 0:
			soundObj = pygame.mixer.Sound('data/sounds/badswap.wav')
			soundObj.play()
			self.jogando = False
			self.restart()
			self.vidaponto()
			self.textSurfaceObj.update("Game Over")
			self.textSurfaceObj.draw(self.DISPLAYSURF)
			self.batch.draw()
			time.sleep(3)

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
