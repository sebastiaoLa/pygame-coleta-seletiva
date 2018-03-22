import random
import sys
import time

import pygame
from pygame.locals import *


class Game():
	def __init__(self, *args, **kwargs):
		self.organicolist = []
		self.metallist = []
		self.plasticolist = []
		self.papellist = []
		self.vidrolist = []
		self.ponto = 0

		self.cont = 0
		self.sol = False
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
	
	def main_loop(self):
		while True: #main game loop
			self.DISPLAYSURF.blit(self.playing,self.playingObjRect)
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
					pygame.quit()
					exit()
				if event.type == MOUSEBUTTONUP:
					mousex, mousey = event.pos
					print mousex,mousey
					if self.jogando and True in [self.plasticoclicked,self.metalclicked,self.papelclicked,self.organicoclicked,self.vidroclicked]:
						clickagain = True
				if event.type ==  MOUSEMOTION:
					mousemox,mousemoy = event.pos
					#print mousemox,mousemoy
				if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
					if self.jogando:
						self.jogando = False
					elif self.instrucoesbool:
						self.instrucoesbool = False
					else:
						sys.exit()
						pygame.quit()
						exit()
				
			if (mousemox >= self.sairObjRect.left and mousemox <=self.sairObjRect.right) and (mousemoy >= self.sairObjRect.top and mousemoy <= self.sairObjRect.bottom):
				sair = pygame.image.load('sair2.png')
			else:
				sair = pygame.image.load('sair1.png')
			if (mousex >= self.sairObjRect.left and mousex <= self.sairObjRect.right) and (mousey >= self.sairObjRect.top and mousey <= self.sairObjRect.bottom):
					if self.jogando:
						self.jogando = False
					elif self.instrucoesbool:
						self.instrucoesbool = False
					else:
						sys.exit()
						pygame.quit()
						exit()
			if self.jogando == False and self.instrucoesbool == False:
				if (mousemox >=self. menuObjRect.left and mousemox <= self.menuObjRect.right) and (mousemoy >= self.menuObjRect.top and mousemoy <= self.menuObjRect.bottom):
					menu = pygame.image.load('menu2.png')
				else:
					menu = pygame.image.load('menu1.png')
				
				if (mousemox >= self.jogarObjRect.left and mousemox <= self.jogarObjRect.right) and (mousemoy >= self.jogarObjRect.top and mousemoy <= self.jogarObjRect.bottom):
					jogar = pygame.image.load('jogar2.png')
				else:
					jogar = pygame.image.load('jogar1.png')
				
				if (mousemox >= instrucoesObjRect.left and mousemox <= instrucoesObjRect.right) and (mousemoy >= instrucoesObjRect.top and mousemoy <= instrucoesObjRect.bottom):
					instrucoes = pygame.image.load('instrucoes2.png')
				else:
					instrucoes = pygame.image.load('instrucoes1.png')
					
				if clicked:
					if (mousex >= jogarObjRect.left and mousex <= jogarObjRect.right) and (mousey >= jogarObjRect.top and mousey <= jogarObjRect.bottom):
						jogando = True
						soundObj = pygame.mixer.Sound('asdf.ogg')
						soundObj.play()
						zerar()
					if (mousex >= instrucoesObjRect.left and mousex <= instrucoesObjRect.right) and (mousey >= instrucoesObjRect.top and mousey <= instrucoesObjRect.bottom):
						instrucoesbool = True	
						soundObj = pygame.mixer.Sound('asdf.ogg')
						soundObj.play()
						zerar()	
				
				if (mousex >= menuObjRect.left and mousex <= menuObjRect.right) and (mousey >= menuObjRect.top and mousey <= menuObjRect.bottom):
					click = True
					soundObj = pygame.mixer.Sound('asdf.ogg')
					soundObj.play()
					zerar()
					
				if jogary >= 90:
					click = False
					clicked = True 
				
				if click == True:
					jogary += 2
					instrucoesy += 4
					jogarObjRect.center = (jogarx,jogary)
					instrucoesObjRect.center = (instrucoesx,instrucoesy)
			
			elif instrucoesbool == True:
				instrucoescaixa = pygame.image.load('instrucoescaixa.png')
				instrucoescaixaObjRect = instrucoescaixa.get_rect()
				instrucoescaixaObjRect.center = (350,275)
				DISPLAYSURF.blit(menu,menuObjRect)
				DISPLAYSURF.blit(instrucoescaixa,instrucoescaixaObjRect)
				if (mousex >= menuObjRect.left and mousex <= menuObjRect.right) and (mousey >= menuObjRect.top and mousey <= menuObjRect.bottom):
					instrucoesbool = False
					soundObj = pygame.mixer.Sound('asdf.ogg')
					soundObj.play()
					zerar()
				
				if (mousemox >= menuObjRect.left and mousemox <= menuObjRect.right) and (mousemoy >= menuObjRect.top and mousemoy <= menuObjRect.bottom):
					menu = pygame.image.load('menu2.png')
				else:
					menu = pygame.image.load('menu1.png')
					
			elif jogando == True: #Eis o Real Jogo
				
				if plasticoclicked:
					if clickagain == True:
						if (mousex >= 4 and mousex <= 43) and (mousey >= 370 and mousey <= 430):
							acerto()
							plastico = False
							plasticoclicked = False
						else:
							erro()
							plastico = False
							plasticoclicked = False
						
				if organicoclicked:
					if clickagain == True:
						if (mousex >= 171 and mousex <= 210) and (mousey >= 370 and mousey <= 430):
							organico = False
							organicoclicked = False
							acerto()
						else:
							organico = False
							organicoclicked = False
							erro()
							
				if metalclicked:
					if clickagain == True:
						if (mousex >= 86 and mousex <= 126) and (mousey >= 370 and mousey <= 430):
							metal = False
							metalclicked = False
							acerto()
						else:
							metal = False
							metalclicked = False
							erro()
							
				if vidroclicked:
					if clickagain == True:
						if (mousex >= 45 and mousex <= 90) and (mousey >= 370 and mousey <= 430):
							vidro = False
							vidroclicked = False
							acerto()
						else:
							vidro = False
							vidroclicked = False
							erro()
				
				if organicoclicked:
					if clickagain == True:
						if (mousex >= 170 and mousex <= 210) and (mousey >= 370 and mousey <= 430):
							organico = False
							organicoclicked = False
							acerto()
						else:
							organico = False
							organicoclicked = False
							erro()
							
				if papelclicked:
					if clickagain == True:
						if (mousex >= 128 and mousex <= 170) and (mousey >= 370 and mousey <= 430):
							papel = False
							papelclicked = False
							acerto()
							
						else:
							papel = False
							papelclicked = False
							erro()
							
				
				if organico:
					DISPLAYSURF.blit(organicoimg,organicoimgObjRect)
					if (mousex >= organicolist[2] and mousex <= organicolist[3]) and (mousey >= organicolist[4] and mousey <= organicolist[5]):
						organicoclicked = True
						zerar()
				if plastico:
					DISPLAYSURF.blit(plasticoimg,plasticoimgObjRect)
					if (mousex >= plasticolist[2] and mousex <= plasticolist[3]) and (mousey >= plasticolist[4] and mousey <= plasticolist[5]):
						plasticoclicked = True
						zerar()
				if metal:
					DISPLAYSURF.blit(metalimg,metalimgObjRect)
					if (mousex >= metallist[2] and mousex <= metallist[3]) and (mousey >= metallist[4] and mousey <= metallist[5]):
						metalclicked = True
						zerar()
				if vidro:
					DISPLAYSURF.blit(vidroimg,vidroimgObjRect)
					if (mousex >= vidrolist[2] and mousex <= vidrolist[3]) and (mousey >= vidrolist[4] and mousey <= vidrolist[5]):
						vidroclicked = True
						zerar()
				if papel:
					DISPLAYSURF.blit(papelimg,papelimgObjRect)
					if (mousex >= papellist[2] and mousex <= papellist[3]) and (mousey >= papellist[4] and mousey <= papellist[5]):
						papelclicked = True
						zerar()
				if organicoclicked:
					organicoimgObjRect.center = (mousemox,mousemoy)
				if plasticoclicked:
					plasticoimgObjRect.center = (mousemox,mousemoy)
				if metalclicked:
					metalimgObjRect.center = (mousemox,mousemoy)
				if papelclicked:
					papelimgObjRect.center = (mousemox,mousemoy)
				if vidroclicked:
					vidroimgObjRect.center = (mousemox,mousemoy)
				
				pontosObj = fontObj.render(str(ponto), True, red)
				vidasObj = fontObj.render(str(vidas), True, red)
				pontosObjRect = pontosObj.get_rect()
				vidasObjRect = vidasObj.get_rect()
				pontosObjRect.topright = (700,0)
				vidasObjRect.topleft = (0,0)
				DISPLAYSURF.blit(pontosObj,pontosObjRect)
				DISPLAYSURF.blit(vidasObj,vidasObjRect)
				
				if ponto == 15:
					jogando = False
					textSurfaceObj = fontObj.render("Parabens, voce venceu", True, red)
					textRectObj = textSurfaceObj.get_rect()
					mousex = 0
					mousey = 0
					restart()
					vidaponto()
					vidaponto()
					textRectObj.center = (350,275)
					textRectObj.top = 0
					DISPLAYSURF.blit(textSurfaceObj, textRectObj)
					pygame.display.update()
					time.sleep(3)
					
				if vidas == 0:
					soundObj = pygame.mixer.Sound('badswap.wav')
					soundObj.play()
					jogando = False
					textSurfaceObj = fontObj.render("Game Over", True, red)
					textRectObj = textSurfaceObj.get_rect()
					mousex = 0
					mousey = 0
					restart()
					vidaponto()
					textRectObj.center = (350,275)
					textRectObj.top = 0
					DISPLAYSURF.blit(textSurfaceObj, textRectObj)
					pygame.display.update()
					time.sleep(3)
				
				if organico == False and plastico == False and metal == False and vidro == False and papel == False:
					#jogando = False
					restart()
					nivel += 1
					nivelstr = "Nivel: "+str(nivel)
					textSurfaceObj = fontObj.render(nivelstr, True, red)
					textRectObj = textSurfaceObj.get_rect()
					contsol = cont
					sol = True
					
				
			if (mousex >= 68 and mousex<=140) and (mousey>=80 and mousey<= 130):
					textSurfaceObj = fontObj.render("CUIDADO, O SOL QUEIMA!!!", True, red)
					textRectObj = textSurfaceObj.get_rect()
					mousex = 0
					mousey = 0
					contsol = cont
					sol = True
			if sol==True:
				if cont != contsol+3*fps:
					textRectObj = textSurfaceObj.get_rect()
					textRectObj.center = (350,275)
					textRectObj.top = 0
					DISPLAYSURF.blit(textSurfaceObj, textRectObj)
				else:
					sol = False
			if jogando == False and instrucoesbool == False:
				DISPLAYSURF.blit(jogar,jogarObjRect)
				DISPLAYSURF.blit(instrucoes,instrucoesObjRect)
				DISPLAYSURF.blit(menu,menuObjRect)
			
			DISPLAYSURF.blit(sair,sairObjRect)
			pygame.display.update()
			cont+= 1
			fpsClock.tick(fps)
				

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
		self.organicolist.insert(0,random.randint(40,600))
		self.organicolist.insert(1,random.randint(450,500))
		organicoimgObjRect = self.organicoimg.get_rect()
		organicoimgObjRect.center = (self.organicolist[0],self.organicolist[1])
		self.metallist.insert(0,random.randint(40,600))
		self.metallist.insert(1,random.randint(450,500))
		metalimgObjRect = self.metalimg.get_rect()
		metalimgObjRect.center = (self.metallist[0],self.metallist[1])
		self.vidrolist.insert(0,random.randint(40,600))
		self.vidrolist.insert(1,random.randint(450,500))
		vidroimgObjRect = self.vidroimg.get_rect()
		vidroimgObjRect.center = (self.vidrolist[0],self.vidrolist[1])
		self.plasticolist.insert(0,random.randint(40,600))
		self.plasticolist.insert(1,random.randint(450,500))
		plasticoimgObjRect = self.plasticoimg.get_rect()
		plasticoimgObjRect.center = (self.plasticolist[0],self.plasticolist[1])
		self.papellist.insert(0,random.randint(40,600))
		self.papellist.insert(1,random.randint(450,500))
		papelimgObjRect = self.papelimg.get_rect()
		papelimgObjRect.center = (self.papellist[0],self.papellist[1])
		self.organicolist.insert(2,organicoimgObjRect.left)
		self.organicolist.insert(3,organicoimgObjRect.right)
		self.organicolist.insert(4,organicoimgObjRect.top)
		self.organicolist.insert(5,organicoimgObjRect.bottom)
		self.metallist.insert(2,metalimgObjRect.left)
		self.metallist.insert(3,metalimgObjRect.right)
		self.metallist.insert(4,metalimgObjRect.top)
		self.metallist.insert(5,metalimgObjRect.bottom)
		self.vidrolist.insert(2,vidroimgObjRect.left)
		self.vidrolist.insert(3,vidroimgObjRect.right)
		self.vidrolist.insert(4,vidroimgObjRect.top)
		self.vidrolist.insert(5,vidroimgObjRect.bottom)
		self.plasticolist.insert(2,plasticoimgObjRect.left)
		self.plasticolist.insert(3,plasticoimgObjRect.right)
		self.plasticolist.insert(4,plasticoimgObjRect.top)
		self.plasticolist.insert(5,plasticoimgObjRect.bottom)
		self.papellist.insert(2,papelimgObjRect.left)
		self.papellist.insert(3,papelimgObjRect.right)
		self.papellist.insert(4,papelimgObjRect.top)
		self.papellist.insert(5,papelimgObjRect.bottom)
		
		
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