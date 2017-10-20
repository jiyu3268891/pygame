# -*- coding: UTF-8 -*-
import pygame
import random
from pygame.locals import *
from sys import exit


########变量############
plane_img = 'C:\\09.python item\\pygame\\Airplane\\resources\\ui\\plane.png'
background_img = 'C:\\09.python item\\pygame\\Airplane\\resources\\background.png'
bullet_img = 'C:\\09.python item\\pygame\\Airplane\\resources\\ui\\bullet.png'
enemya_img = 'C:\\09.python item\\pygame\\Airplane\\resources\\ui\\enemya.png'
ship_img = 'C:\\09.python item\\pygame\\Airplane\\resources\\ui\\ship.png'
start_img = 'C:\\09.python item\\pygame\\Airplane\\resources\\ui\\game_start_up.png'
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600
interval_b = 0


########函数#############
class Bullet:
	def __init__(self):
		self.x = 0
		self.y = -1
		self.image = pygame.image.load(bullet_img).convert_alpha()
		self.active = False
	def move(self):
		if self.active:
			self.y = self.y - 3
		if self.y < 0:
			self.active = False
	def restart(self):
		mouseX, mouseY = pygame.mouse.get_pos()
		self.x = mouseX - self.image.get_width() / 2
		self.y = mouseY - self.image.get_height() / 2
		self.active = True

#####打一下的小飞机##############
class Enemya:
	def restart(self):
		self.x = random.randint(50, 400)
		self.y = random.randint(-400, -50)
		self.speed = random.uniform(0, 0.5) + 0.1
		self.blood = 1
	def __init__(self, blood):
		self.restart()
		self.image = pygame.image.load(enemya_img).convert_alpha()
		self.blood = blood
	def move(self):
		if self.y < 600:
			self.y += self.speed
		else:
			self.restart()

##########要打5下的大飞船#######
class Ship:
	def restart(self):
		self.x = random.randint(50, 400)
		self.y = random.randint(-400, -50)
		self.speed = random.uniform(0, 0.05) + 0.05
		self.blood = 5
	def __init__(self, blood):
		self.restart()
		self.image = pygame.image.load(ship_img).convert_alpha()
		self.blood = blood
	def move(self):
		if self.y < 1800:
			self.y += self.speed
		else:
			self.restart()
######自己的飞机##########
class Plane:
	def restart(self):
		self.x = 200
		self.y = 300
	def __init__(self):
		self.restart()
		self.image = pygame.image.load(plane_img).convert_alpha()

	def move(self):
		x, y = pygame.mouse.get_pos()
		x-= self.image.get_width() / 2
		y-= self.image.get_height() / 2
		self.x = x
		self.y = y



def checkHit(attack, bullet):
	if (bullet.x > attack.x and bullet.x < attack.x + attack.image.get_width()) and (
					bullet.y > attack.y and bullet.y < attack.y + attack.image.get_height()):
		if attack.blood > 1:
			attack.blood = attack.blood -1
			bullet.active = False
			return False
		else:
			bullet.active = False
			attack.restart()
			return True
	else:
		return False

def checkCrash(attack, plane):
	if (plane.x + 0.7 * plane.image.get_width() > attack.x) and (
		plane.x + 0.3 * plane.image.get_width() < attack.x + attack.image.get_width()) and (
		plane.y + 0.7 * plane.image.get_height() > attack.y) and (
		plane.y + 0.3 * plane.image.get_width() < attack.y + attack.image.get_height()):
		return True
	else:
		return False


########加载画面#########
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('一起打飞机')
background = pygame.image.load(background_img).convert()
start = pygame.image.load(start_img).convert()
plane = Plane()
bullets = []
for i in range(5):
	bullets.append(Bullet())
count_b = len(bullets)
enemyas = []
for i in range(3):
	enemyas.append(Enemya(1))

ship = []
for i in range(2):
	ship.append(Ship(5))


index_b = 0
interval_b = 0
score = 0
font = pygame.font.Font(None, 32)
#planebullet = Bullet()
#enemya = Enemya()


gameover = False
gamestart = False



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	if not gamestart:
		start_img_x= 80 + start.get_width()
		start_img_y= 280 + start.get_height()
		screen.blit(background, (0, 0))
		screen.blit(start, (80, 280))
#		for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = pygame.mouse.get_pos()
			if( x > 80 and x < start_img_x ) and ( y > 280 and y < start_img_y ):
				gamestart= True

	else:
		if gameover and event.type == pygame.MOUSEBUTTONUP:
			plane.restart()
			for e in enemyas:
				e.restart()
			for b in bullets:
				b.active = False
				score = 0
				gameover = False
		screen.blit(background, (0, 0))
		if not gameover:
			interval_b = interval_b - 0.5
			if interval_b < 0:
				bullets[index_b].restart()
				interval_b = 100
				index_b = (index_b + 1) % count_b
			for b in bullets:
				if b.active:
					b.move()
					screen.blit(b.image, (b.x, b.y))
			for e in enemyas:
				if checkCrash(e, plane):
					gameover = True
				e.move()
				screen.blit(e.image, (e.x, e.y))
			for s in ship:
				if checkCrash(s, plane):
					gameover = True
				s.move()
				screen.blit(s.image, (s.x, s.y))
			for b in bullets:
				if b.active:
					for e in enemyas:
						if checkHit(e, b):
							e.restart()
							score = score + 100
					for s in ship:
						if checkHit(s, b):
							s.restart()
							score = score + 200
					b.move()
					screen.blit(b.image, (b.x, b.y))
			plane.move()
			text = font.render("Score: %d" % score, 1, (0, 0, 0))
			screen.blit(text, (0, 0))
			screen.blit(plane.image, (plane.x, plane.y))
		else:
			text = font.render("Socre: %d" % score, 1, (0, 0, 0))
			screen.blit(text, (190, 300))
			text2 = font.render("GAME IS OVER",1, (0, 0, 0))
			screen.blit(text2, (160, 200))
	pygame.display.update()
