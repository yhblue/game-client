import pygame
from pygame.locals import *
import time
import socket
import threading

PIC_X = 1000
PIC_Y = 600

START_X = 0
START_Y = 0

HERO_X = 40
HERO_Y = 40

ENEMY_X = 40
ENEMY_Y = 40

X_MAX = PIC_X - HERO_X   
Y_MAX = PIC_Y - HERO_Y

STEP = 2

HERO_PIC_PATH = "./pic/hero.jpg"
ENEMY_PIC_PATH = "./pic/enemy.jpg"
BACK_PIC_PATH = "./pic/background.jpg"

ADDRESS = "localhost"
PORT = 3080

class HERO_PLAYER(object):
	"""docstring for player"""
	def __init__(self, screen):
		self.x = 0
		self.y = 0
		self.screen = screen
		self.image = pygame.image.load(HERO_PIC_PATH);
		self.up = False
		self.left = False
		self.right = False
		self.down = False

	def display(self):
		self.screen.blit(self.image, (self.x,self.y))

	def move_left(self):
		if self.x >= STEP:
			self.x -= STEP

	def move_right(self):			
		if self.x <= X_MAX - STEP:
			self.x += STEP

	def move_up(self):
		if self.y >= STEP:
			self.y -= STEP

	def move_down(self):
		if self.y <= Y_MAX - STEP:
			self.y += STEP

	def position_update(self):
		if(self.up == True):
			self.move_up()
		if(self.down == True):
			self.move_down()
		if(self.left == True):
			self.move_left()
		if(self.right == True):
			self.move_right()	


class ENEMY_PLAYER(object):
	"""docstring for enemy"""
	def __init__(self, screen):
		self.x = 0
		self.y = 0
		self.screen = screen
		self.image = pygame.image.load(ENEMY_PIC_PATH);

	def display(self):
		self.screen.blit(self.image, (self.x,self.y))

	def move_left(self):
		if self.x >= STEP:
			self.x -= STEP

	def move_right(self):			
		if self.x <= X_MAX - STEP:
			self.x += STEP

	def move_up(self):
		if self.y >= STEP:
			self.y -= STEP

	def move_down(self):
		if self.y <= Y_MAX - STEP:
			self.y += STEP


def key_control(hero):
	for event in pygame.event.get():
		if event.type == QUIT:
			print("exit")
			exit()

		elif event.type ==  KEYDOWN:

			if event.key == K_LEFT:
				hero.left = True

			elif event.key == K_RIGHT:
				hero.right = True

			elif event.key == K_UP:
				hero.up = True

			elif event.key == K_DOWN:
				hero.down = True

		elif event.type ==  KEYUP:
			hero.down = False
			hero.left = False			
			hero.right = False
			hero.up = False


def client_send(sock,hero,enemy_list):
	while True:
		time.sleep(0.1)
		sock.sendall("hellow tcp server")
		pass



def client_recv(sock,buff_recv):
	while True:
		data = sock.recv(128)
		if data:
			buff_recv.append(data)
			print(data)


def scene_load():
	pass
	

def main():

	buff_recv = []
	enemy_list = []
	screen = pygame.display.set_mode((PIC_X,PIC_Y),0,32)
	background = pygame.image.load(BACK_PIC_PATH)
	hero = HERO_PLAYER(screen)
	enemy = ENEMY_PLAYER(screen)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ADDRESS, PORT)) 

	print('thread %s is running...' % threading.current_thread().name)
	thread_read = threading.Thread(target=client_send,args=(sock,hero,enemy_list))
	thread_write = threading.Thread(target=client_recv,args=(sock,buff_recv))
	thread_read.start()
	thread_write.start()

	while True:
		screen.blit(background, (START_X,START_Y))
		hero.display()
		enemy.display()
		pygame.display.update()

		key_control(hero)
		hero.position_update()
		time.sleep(0.01)

	sock.close()
	thread_read.join()
	thread_write.join()

if __name__ == "__main__":
	main()


#http://www.cnblogs.com/lewiskyo/p/6240854.html