import random
import sys
import time

import pygame
from pygame.locals import QUIT,MOUSEBUTTONUP,MOUSEMOTION,KEYDOWN,K_ESCAPE


class Game():
	def __init__(self, *args, **kwargs):
		self.RED = (255,000,000)
		self.GREEN = (000,255,000)
		self.BLUE = (000,000,255)
		self.WHITE = (255,255,255)
		self.BLACK = (000,000,000)
		self.ponto = 0

		self.cont = 0
		self.sol = False
		self.solObjRect = pygame.Rect(68,80,72,50)
		self.nivel = 1
		self.contsol = -1
		self.mousex = 0
		self.mousey = 0
		self.mousemox = 0
		self.mousemoy  = 0
		self.jogarx = 600
		self.jogary = 60
		self.instrucoesx = 600
		self.instrucoesy = 60
		self.fps = 60
		self.click = False
		self.jogando = False
		self.clicked = False
		self.instrucoesbool = False
		self.clickagain = False
		self.ponto = 0
		self.vidas = 3

		self.fpsClock = pygame.time.Clock()

		pygame.init()
		self.fontObj = pygame.font.Font('freesansbold.ttf', 28)
		pygame.display.set_caption('Coleta Seletiva')
		self.DISPLAYSURF = pygame.display.set_mode((700, 550))
		# pygame.display.toggle_fullscreen()
		self.playing = pygame.image.load('data/images/background/playing.png')

		self.menu = pygame.image.load('data/images/menu/menu1.png')

		self.jogar = pygame.image.load('data/images/menu/jogar1.png')

		self.sair = pygame.image.load('data/images/menu/sair1.png')

		self.instrucoes = pygame.image.load('data/images/menu/instrucoes1.png')

		self.organicoimg = pygame.image.load('data/images/trash/organico.png')

		self.metalimg = pygame.image.load('data/images/trash/metal.png')

		self.vidroimg = pygame.image.load('data/images/trash/vidro.png')

		self.plasticoimg = pygame.image.load('data/images/trash/plastico.png')

		self.papelimg = pygame.image.load('data/images/trash/papel.png')

		self.menuObjRect = self.menu.get_rect()
		self.menuObjRect.center = (600,60)

		self.playingObjRect = self.playing.get_rect()
		self.playingObjRect.center = (350,275)

		self.jogarObjRect = self.jogar.get_rect()
		self.jogarObjRect.center = self.menuObjRect.center

		self.instrucoesObjRect = self.instrucoes.get_rect()
		self.instrucoesObjRect.center = self.menuObjRect.center

		self.sairObjRect = self.sair.get_rect()
		self.sairObjRect.right = self.menuObjRect.left - 15
		self.sairObjRect.top = self.menuObjRect.top

		self.DISPLAYSURF.blit(self.playing,self.playingObjRect)
		self.DISPLAYSURF.blit(self.menu,self.menuObjRect)	
		self.DISPLAYSURF.blit(self.jogar,self.jogarObjRect)
		self.DISPLAYSURF.blit(self.instrucoes,self.instrucoesObjRect)
		self.DISPLAYSURF.blit(self.sair,self.sairObjRect)

		self.textSurfaceObj = self.fontObj.render("", True, (255,0,0))


		self.restart()

	def check_hover(self,mousePos,objRect):
		return (mousePos[0] >= objRect.left and mousePos[0] <= objRect.right) and (mousePos[1] >= objRect.top and mousePos[1] <= objRect.bottom)

	def draw(self):
		self.DISPLAYSURF.blit(self.playing,self.playingObjRect)
		if self.instrucoesbool:
			instrucoescaixa = pygame.image.load('data/images/menu/instrucoescaixa.png')
			instrucoescaixaObjRect = instrucoescaixa.get_rect()
			instrucoescaixaObjRect.center = (350,275)
			self.DISPLAYSURF.blit(self.menu,self.menuObjRect)
			self.DISPLAYSURF.blit(instrucoescaixa,instrucoescaixaObjRect)
		elif self.jogando:
			if self.organico:
				self.DISPLAYSURF.blit(self.organicoimg,self.organicoimgObjRect)

			if self.plastico:
				self.DISPLAYSURF.blit(self.plasticoimg,self.plasticoimgObjRect)

			if self.metal:
				self.DISPLAYSURF.blit(self.metalimg,self.metalimgObjRect)
					
			if self.vidro:
				self.DISPLAYSURF.blit(self.vidroimg,self.vidroimgObjRect)
					
			if self.papel:
				self.DISPLAYSURF.blit(self.papelimg,self.papelimgObjRect)
			
			pontosObj = self.fontObj.render(str(self.ponto), True, self.BLACK)
			vidasObj = self.fontObj.render(str(self.vidas), True, self.RED)
			pontosObjRect = pontosObj.get_rect()
			vidasObjRect = vidasObj.get_rect()
			pontosObjRect.topright = (700,0)
			vidasObjRect.topleft = (0,0)
			self.DISPLAYSURF.blit(pontosObj,pontosObjRect)
			self.DISPLAYSURF.blit(vidasObj,vidasObjRect)

			if self.ponto == 15:
				textSurfaceObj = self.fontObj.render("Parabens, voce venceu", True, self.RED)
				textRectObj = textSurfaceObj.get_rect()
				textRectObj.center = (350,275)
				textRectObj.top = 0
				self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
			
			if self.vidas == 0:
				textSurfaceObj = self.fontObj.render("Game Over", True, self.RED)
				textRectObj = textSurfaceObj.get_rect()
				textRectObj.center = (350,275)
				textRectObj.top = 0
				self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)

			
	def main_loop(self):
		while True: #main game loop
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
					mousex,mousey = mouseClkPos
					print mousex,mousey
					if self.jogando and True in [self.plasticoclicked,self.metalclicked,self.papelclicked,self.organicoclicked,self.vidroclicked]:
						self.clickagain = True
				if event.type ==  MOUSEMOTION:
					mouseMotPos = event.pos
					mousemox,mousemoy = mouseMotPos 
					print mousemox,mousemoy
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					if self.jogando:
						self.jogando = False
					elif self.instrucoesbool:
						self.instrucoesbool = False
					else:
						sys.exit()
						pygame.quit()
						exit()
				
			if self.sairObjRect.collidepoint(mouseMotPos):
				self.sair = pygame.image.load('data/menu/sair2.png')
			else:
				self.sair = pygame.image.load('data/menu/sair1.png')
			if self.sairObjRect.collidepoint(mouseMotPos):
					if self.jogando:
						self.jogando = False
					elif self.instrucoesbool:
						self.instrucoesbool = False
					else:
						sys.exit()
						pygame.quit()
						exit()
			if self.jogando == False and self.instrucoesbool == False:
				if self.menuObjRect.collidepoint(mouseMotPos):
					self.menu = pygame.image.load('data/menu/menu2.png')
				else:
					self.menu = pygame.image.load('data/menu/menu1.png')
				
				if self.jogarObjRect.collidepoint(mouseMotPos):
					self.jogar = pygame.image.load('data/menu/jogar2.png')
				else:
					self.jogar = pygame.image.load('data/menu/jogar1.png')
				
				if self.instrucoesObjRect.collidepoint(mouseMotPos):
					self.instrucoes = pygame.image.load('data/menu/instrucoes2.png')
				else:
					self.instrucoes = pygame.image.load('data/menu/instrucoes1.png')
					
				if self.clicked:
					if self.jogarObjRect.collidepoint(mouseClkPos):
						self.jogando = True
						soundObj = pygame.mixer.Sound('data/sounds/click.ogg')
						soundObj.play()
						
					if self.instrucoesObjRect.collidepoint(mouseClkPos):
						self.instrucoesbool = True	
						soundObj = pygame.mixer.Sound('data/sounds/click.ogg')
						soundObj.play()
						
				
				if self.menuObjRect.collidepoint(mouseClkPos):
					self.click = True
					soundObj = pygame.mixer.Sound('data/sounds/click.ogg')
					soundObj.play()
					
					
				if self.jogary >= 90:
					self.click = False
					self.clicked = True 
				
				if self.click == True:
					self.jogary += 2
					self.instrucoesy += 4
					self.jogarObjRect.center = (self.jogarx,self.jogary)
					self.instrucoesObjRect.center = (self.instrucoesx,self.instrucoesy)
			
			elif self.instrucoesbool == True:
				instrucoescaixa = pygame.image.load('data/images/menu/instrucoescaixa.png')
				instrucoescaixaObjRect = instrucoescaixa.get_rect()
				instrucoescaixaObjRect.center = (350,275)
				self.DISPLAYSURF.blit(self.menu,self.menuObjRect)
				self.DISPLAYSURF.blit(instrucoescaixa,instrucoescaixaObjRect)
				if self.menuObjRect.collidepoint(mouseClkPos):
					self.instrucoesbool = False
					soundObj = pygame.mixer.Sound('data/sounds/click.ogg')
					soundObj.play()
					
				
				if self.menuObjRect.collidepoint(mouseMotPos):
					self.menu = pygame.image.load('data/images/menu/menu2.png')
				else:
					self.menu = pygame.image.load('data/images/menu/menu1.png')
					
			elif self.jogando == True: #Eis o Real Jogo
				
				if self.clickagain == True:
					if self.plasticoclicked:	
						if pygame.Rect(4,370,43-4,430-370).collidepoint(mouseClkPos):
							self.acerto()
							self.plastico = False
							self.plasticoclicked = False
						else:
							self.erro()
							self.plastico = False
							self.plasticoclicked = False
						
					if self.organicoclicked:
						if pygame.Rect(171,370,210-171,430-370).collidepoint(mouseClkPos):
							self.organico = False
							self.organicoclicked = False
							self.acerto()
						else:
							self.organico = False
							self.organicoclicked = False
							self.erro()
							
					if self.metalclicked:
						if pygame.Rect(86,370,126-86,430-126).collidepoint(mouseClkPos):
							self.metal = False
							self.metalclicked = False
							self.acerto()
						else:
							self.metal = False
							self.metalclicked = False
							self.erro()
							
					if self.vidroclicked:
						if pygame.Rect(45,370,90-45,430-370).collidepoint(mouseClkPos):
							self.vidro = False
							self.vidroclicked = False
							self.acerto()
						else:
							self.vidro = False
							self.vidroclicked = False
							self.erro()
				
					if self.organicoclicked:
						if pygame.Rect(170,370,210-170,430-370).collidepoint(mouseClkPos):
							self.organico = False
							self.organicoclicked = False
							self.acerto()
						else:
							self.organico = False
							self.organicoclicked = False
							self.erro()
							
					if self.papelclicked:
						if pygame.Rect(128,370,170-128,430-370).collidepoint(mouseClkPos):
							self.papel = False
							self.papelclicked = False
							self.acerto()
							
						else:
							self.papel = False
							self.papelclicked = False
							self.erro()
							
				if self.organico:
					self.DISPLAYSURF.blit(self.organicoimg,self.organicoimgObjRect)
					if self.organicoimgObjRect.collidepoint(mouseClkPos):
						self.organicoclicked = True
						
				if self.plastico:
					self.DISPLAYSURF.blit(self.plasticoimg,self.plasticoimgObjRect)
					if self.plasticoimgObjRect.collidepoint(mouseClkPos):
						self.plasticoclicked = True
						
				if self.metal:
					self.DISPLAYSURF.blit(self.metalimg,self.metalimgObjRect)
					if self.metalimgObjRect.collidepoint(mouseClkPos):
						self.metalclicked = True
						
				if self.vidro:
					self.DISPLAYSURF.blit(self.vidroimg,self.vidroimgObjRect)
					if self.vidroimgObjRect.collidepoint(mouseClkPos):
						self.vidroclicked = True
						
				if self.papel:
					self.DISPLAYSURF.blit(self.papelimg,self.papelimgObjRect)
					if self.papelimgObjRect.collidepoint(mouseClkPos):
						self.papelclicked = True
						
				if self.organicoclicked:
					self.organicoimgObjRect.center = mouseMotPos
				if self.plasticoclicked:
					self.plasticoimgObjRect.center = mouseMotPos
				if self.metalclicked:
					self.metalimgObjRect.center = mouseMotPos
				if self.papelclicked:
					self.papelimgObjRect.center = mouseMotPos
				if self.vidroclicked:
					self.vidroimgObjRect.center = mouseMotPos
				
				pontosObj = self.fontObj.render(str(self.ponto), True, self.BLACK)
				vidasObj = self.fontObj.render(str(self.vidas), True, self.RED)
				pontosObjRect = pontosObj.get_rect()
				vidasObjRect = vidasObj.get_rect()
				pontosObjRect.topright = (700,0)
				vidasObjRect.topleft = (0,0)
				self.DISPLAYSURF.blit(pontosObj,pontosObjRect)
				self.DISPLAYSURF.blit(vidasObj,vidasObjRect)
				
				if self.ponto == 15:
					self.jogando = False
					mousex = 0
					mousey = 0
					self.restart()
					self.vidaponto()
					textSurfaceObj = self.fontObj.render("Parabens, voce venceu", True, self.RED)
					textRectObj = textSurfaceObj.get_rect()
					textRectObj.center = (350,275)
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
					textSurfaceObj = self.fontObj.render("Game Over", True, self.RED)
					textRectObj = textSurfaceObj.get_rect()
					textRectObj.center = (350,275)
					textRectObj.top = 0
					self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
					pygame.display.update()
					time.sleep(3)
				
				if True not in [self.organico,self.plastico,self.metal,self.vidro,self.papel]:
					#jogando = False
					self.restart()
					self.nivel += 1
					nivelstr = "Nivel: "+str(self.nivel)
					textSurfaceObj = self.fontObj.render(nivelstr, True, self.RED)
					textRectObj = textSurfaceObj.get_rect()
					self.contsol = self.cont
					self.sol = True
					
				
			if self.solObjRect.collidepoint(mouseClkPos):
					textSurfaceObj = self.fontObj.render("CUIDADO, O SOL QUEIMA!!!", True, self.RED)
					textRectObj = textSurfaceObj.get_rect()
					self.contsol = self.cont
					self.sol = True
			if self.sol==True:
				if self.cont != self.contsol+3*self.fps:
					textRectObj = textSurfaceObj.get_rect()
					textRectObj.center = (350,275)
					textRectObj.top = 0
					self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
				else:
					self.sol = False
			if self.jogando == False and self.instrucoesbool == False:
				self.DISPLAYSURF.blit(self.jogar,self.jogarObjRect)
				self.DISPLAYSURF.blit(self.instrucoes,self.instrucoesObjRect)
				self.DISPLAYSURF.blit(self.menu,self.menuObjRect)
			
			self.DISPLAYSURF.blit(self.sair,self.sairObjRect)
			# self.draw()
			pygame.display.update()
			self.cont+= 1
			self.fpsClock.tick(self.fps)
				

	def vidaponto(self):
		self.vidas = 3
		self.ponto = 0

	def acerto(self):
		soundObj = pygame.mixer.Sound('data/sounds/match0.wav')
		soundObj.play()
		self.ponto +=1
		self.playing = pygame.image.load('data/images/background/playing.png')
		self.clickagain = False

	def erro(self):
		self.vidas = self.vidas - 1
		self.playing = pygame.image.load('data/images/background/playing2.png')
		
		self.clickagain = False

	def restart(self):
		self.organicoimgObjRect = self.organicoimg.get_rect()
		self.organicoimgObjRect.center = (random.randint(40,600),random.randint(450,500))
		self.metalimgObjRect = self.metalimg.get_rect()
		self.metalimgObjRect.center = (random.randint(40,600),random.randint(450,500))
		self.vidroimgObjRect = self.vidroimg.get_rect()
		self.vidroimgObjRect.center = (random.randint(40,600),random.randint(450,500))
		self.plasticoimgObjRect = self.plasticoimg.get_rect()
		self.plasticoimgObjRect.center = (random.randint(40,600),random.randint(450,500))
		self.papelimgObjRect = self.papelimg.get_rect()
		self.papelimgObjRect.center = (random.randint(40,600),random.randint(450,500))
		
		
		self.organico = True
		self.organicoclicked = False
		self.metal = True
		self.metalclicked = False
		self.papel = True
		self.papelclicked = False
		self.plastico = True
		self.plasticoclicked = False
		self.vidro = True
		self.vidroclicked = False


game = Game()
game.main_loop()