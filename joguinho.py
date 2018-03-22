import random
import sys
import time

import pygame
from pygame.locals import *


class Game():
	def __init__(self, *args, **kwargs):
		self.RED = (255,000,000)
		self.GREEN = (000,255,000)
		self.BLUE = (000,000,255)
		self.WHITE = (255,255,255)
		self.BLACK = (000,000,000)
		self.organicolist = []
		self.metallist = []
		self.plasticolist = []
		self.papellist = []
		self.vidrolist = []
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
		self.playing = pygame.image.load('playing.png')

		self.menu = pygame.image.load('menu1.png')

		self.jogar = pygame.image.load('jogar1.png')

		self.sair = pygame.image.load('sair1.png')

		self.instrucoes = pygame.image.load('instrucoes1.png')

		self.organicoimg = pygame.image.load('organico.png')

		self.metalimg = pygame.image.load('metal.png')

		self.vidroimg = pygame.image.load('vidro.png')

		self.plasticoimg = pygame.image.load('Plastico.png')

		self.papelimg = pygame.image.load('papel.png')

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
		print 'checked' , (mousePos[0] >= objRect.left and mousePos[0] <= objRect.right) and (mousePos[1] >= objRect.top and mousePos[1] <= objRect.bottom)
		return (mousePos[0] >= objRect.left and mousePos[0] <= objRect.right) and (mousePos[1] >= objRect.top and mousePos[1] <= objRect.bottom)

	
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
						clickagain = True
				if event.type ==  MOUSEMOTION:
					mouseMotPos = event.pos
					mousemox,mousemoy = mouseMotPos 
					print mousemox,mousemoy
				if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
					if self.jogando:
						self.jogando = False
					elif self.instrucoesbool:
						self.instrucoesbool = False
					else:
						sys.exit()
						pygame.quit()
						exit()
				
			if self.check_hover(mouseMotPos,self.sairObjRect):
				self.sair = pygame.image.load('sair2.png')
			else:
				self.sair = pygame.image.load('sair1.png')
			if self.check_hover(mouseClkPos,self.sairObjRect):
					if self.jogando:
						self.jogando = False
					elif self.instrucoesbool:
						self.instrucoesbool = False
					else:
						sys.exit()
						pygame.quit()
						exit()
			if self.jogando == False and self.instrucoesbool == False:
				if self.check_hover(mouseMotPos,self.menuObjRect):
					self.menu = pygame.image.load('menu2.png')
				else:
					self.menu = pygame.image.load('menu1.png')
				
				if self.check_hover(mouseMotPos,self.jogarObjRect):
					self.jogar = pygame.image.load('jogar2.png')
				else:
					self.jogar = pygame.image.load('jogar1.png')
				
				if self.check_hover(mouseMotPos,self.instrucoesObjRect):
					self.instrucoes = pygame.image.load('instrucoes2.png')
				else:
					self.instrucoes = pygame.image.load('instrucoes1.png')
					
				if self.clicked:
					if self.check_hover(mouseClkPos,self.jogarObjRect):
						self.jogando = True
						soundObj = pygame.mixer.Sound('asdf.ogg')
						soundObj.play()
						self.zerar()
					if self.check_hover(mouseClkPos,self.instrucoesObjRect):
						self.instrucoesbool = True	
						soundObj = pygame.mixer.Sound('asdf.ogg')
						soundObj.play()
						self.zerar()
				
				if self.check_hover(mouseClkPos,self.menuObjRect):
					self.click = True
					soundObj = pygame.mixer.Sound('asdf.ogg')
					soundObj.play()
					self.zerar()
					
				if self.jogary >= 90:
					self.click = False
					self.clicked = True 
				
				if self.click == True:
					self.jogary += 2
					self.instrucoesy += 4
					self.jogarObjRect.center = (self.jogarx,self.jogary)
					self.instrucoesObjRect.center = (self.instrucoesx,self.instrucoesy)
			
			elif self.instrucoesbool == True:
				instrucoescaixa = pygame.image.load('instrucoescaixa.png')
				instrucoescaixaObjRect = instrucoescaixa.get_rect()
				instrucoescaixaObjRect.center = (350,275)
				self.DISPLAYSURF.blit(self.menu,self.menuObjRect)
				self.DISPLAYSURF.blit(instrucoescaixa,instrucoescaixaObjRect)
				if self.check_hover(mouseClkPos,self.menuObjRect):
					self.instrucoesbool = False
					soundObj = pygame.mixer.Sound('asdf.ogg')
					soundObj.play()
					self.zerar()
				
				if self.check_hover(mouseClkPos,self.menuObjRect):
					self.menu = pygame.image.load('menu2.png')
				else:
					self.menu = pygame.image.load('menu1.png')
					
			elif self.jogando == True: #Eis o Real Jogo
				
				if self.plasticoclicked:
					if clickagain == True:
						if (mousex >= 4 and mousex <= 43) and (mousey >= 370 and mousey <= 430):
							self.acerto()
							plastico = False
							plasticoclicked = False
						else:
							self.erro()
							plastico = False
							plasticoclicked = False
						
				if self.organicoclicked:
					if clickagain == True:
						if (mousex >= 171 and mousex <= 210) and (mousey >= 370 and mousey <= 430):
							organico = False
							organicoclicked = False
							self.acerto()
						else:
							organico = False
							organicoclicked = False
							self.erro()
							
				if self.metalclicked:
					if clickagain == True:
						if (mousex >= 86 and mousex <= 126) and (mousey >= 370 and mousey <= 430):
							metal = False
							metalclicked = False
							self.acerto()
						else:
							metal = False
							metalclicked = False
							self.erro()
							
				if self.vidroclicked:
					if clickagain == True:
						if (mousex >= 45 and mousex <= 90) and (mousey >= 370 and mousey <= 430):
							vidro = False
							vidroclicked = False
							self.acerto()
						else:
							vidro = False
							vidroclicked = False
							self.erro()
				
				if self.organicoclicked:
					if clickagain == True:
						if (mousex >= 170 and mousex <= 210) and (mousey >= 370 and mousey <= 430):
							organico = False
							organicoclicked = False
							self.acerto()
						else:
							organico = False
							organicoclicked = False
							self.erro()
							
				if self.papelclicked:
					if clickagain == True:
						if (mousex >= 128 and mousex <= 170) and (mousey >= 370 and mousey <= 430):
							papel = False
							papelclicked = False
							self.acerto()
							
						else:
							papel = False
							papelclicked = False
							self.erro()
							
				
				if self.organico:
					self.DISPLAYSURF.blit(self.organicoimg,self.organicoimgObjRect)
					if self.check_hover(mouseClkPos,self.organicoimgObjRect):
						organicoclicked = True
						self.zerar()
				if plastico:
					self.DISPLAYSURF.blit(self.plasticoimg,self.plasticoimgObjRect)
					if self.check_hover(mouseClkPos,self.plasticoimgObjRect):
						plasticoclicked = True
						self.zerar()
				if metal:
					self.DISPLAYSURF.blit(self.metalimg,self.metalimgObjRect)
					if self.check_hover(mouseClkPos,self.metalimgObjRect):
						metalclicked = True
						self.zerar()
				if vidro:
					self.DISPLAYSURF.blit(self.vidroimg,self.vidroimgObjRect)
					if self.check_hover(mouseClkPos,self.vidroimgObjRect):
						vidroclicked = True
						self.zerar()
				if papel:
					self.DISPLAYSURF.blit(self.papelimg,self.papelimgObjRect)
					if self.check_hover(mouseClkPos,self.papelimgObjRect):
						papelclicked = True
						self.zerar()
				if organicoclicked:
					self.organicoimgObjRect.center = mouseMotPos
				if plasticoclicked:
					self.plasticoimgObjRect.center = mouseMotPos
				if metalclicked:
					self.metalimgObjRect.center = mouseMotPos
				if papelclicked:
					self.papelimgObjRect.center = mouseMotPos
				if vidroclicked:
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
					textSurfaceObj = self.fontObj.render("Parabens, voce venceu", True, red)
					textRectObj = textSurfaceObj.get_rect()
					mousex = 0
					mousey = 0
					self.restart()
					self.vidaponto()
					textRectObj.center = (350,275)
					textRectObj.top = 0
					self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
					pygame.display.update()
					time.sleep(3)
					
				if self.vidas == 0:
					soundObj = pygame.mixer.Sound('badswap.wav')
					soundObj.play()
					self.jogando = False
					textSurfaceObj = self.fontObj.render("Game Over", True, red)
					textRectObj = textSurfaceObj.get_rect()
					self.restart()
					self.vidaponto()
					textRectObj.center = (350,275)
					textRectObj.top = 0
					self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
					pygame.display.update()
					time.sleep(3)
				
				if organico == False and plastico == False and metal == False and vidro == False and papel == False:
					#jogando = False
					self.restart()
					self.nivel += 1
					nivelstr = "Nivel: "+str(self.nivel)
					textSurfaceObj = self.fontObj.render(nivelstr, True, self.RED)
					textRectObj = textSurfaceObj.get_rect()
					contsol = self.cont
					sol = True
					
				
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
			pygame.display.update()
			self.cont+= 1
			self.fpsClock.tick(self.fps)
				

	def zerar(self):
		self.mousemox = 0
		self.mousemoy = 0
		self.mousex = 0
		self.mousey = 0

	def vidaponto(self):
		self.vidas = 3
		self.ponto = 0

	def acerto(self):
		self.soundObj = pygame.mixer.Sound('match0.wav')
		self.soundObj.play()
		self.ponto +=1
		self.playing = pygame.image.load('playing.png')
		self.zerar()
		self.clickagain = False

	def erro(self):
		self.vidas = self.vidas - 1
		self.playing = pygame.image.load('playing2.png')
		self.zerar()
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