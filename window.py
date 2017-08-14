import pygame
from pygame.locals import *
import time
import socket
import threading
import message_pb2

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

LOG_REQ='L'
LOG_RSP='l'

HERO_MSG_REQ="H"
HERO_MSG_RSP='h'

CONNECT_REQ='C'
CONNECT_RSP='c'

HEART_REQ='R'
HEART_REQ='r'

ENEMY_MSG='e'

class HERO_PLAYER(object):
	"""docstring for player"""
	def __init__(self, screen,lock):
		self.x = 0
		self.y = 0
		self.uid = 0
		self.screen = screen
		self.image = pygame.image.load(HERO_PIC_PATH);
		self.up = False
		self.left = False
		self.right = False
		self.down = False
		self.lock = lock

	def display(self):
		self.lock.acquire()
		try:
			self.screen.blit(self.image, (self.x,self.y))
		finally:
			self.lock.release()

	def move_left(self):
		self.lock.acquire()
		try:
			if self.x >= STEP:
				self.x -= STEP
		finally:
			self.lock.release()

	def move_right(self):	
		self.lock.acquire()
		try:		
			if self.x <= X_MAX - STEP:
				self.x += STEP
		finally:
			self.lock.release()

	def move_up(self):
		self.lock.acquire()
		try:
			if self.y >= STEP:
				self.y -= STEP
		finally:
			self.lock.release()

	def move_down(self):
		self.lock.acquire()
		try:
			if self.y <= Y_MAX - STEP:
				self.y += STEP
		finally:
			self.lock.release()

	def position_update(self):
		if(self.up == True):
			self.move_up()
		elif(self.down == True):
			self.move_down()
		elif(self.left == True):
			self.move_left()
		elif(self.right == True):
			self.move_right()	

	def set_uid(self,uid):
		self.uid = uid

	def set_position(x,y)
		self.x = x
		self.y = y

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

class GAME(object):
	"""docstring for game"""
	def __init__(self, arg):
		self.enemy_list = []
		self.enemy_num = 0

	def append_enemy(self,enemy):
		self.enemy_list.append(enemy)
	
	def set_enemy_num(self,num)
		self.enemy_num = num

#put to anthor .py file
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


def login_data_serlia(hero):
	seli_data = message_pb2.Login_req()
	seli_data.name = hero.name
	seli_data.point_x = hero.x
	seli_data.point_y = hero.y
	list_ret =[]
	size = chr(seli_data.ByteSize())
	list_ret.append(size)
	list_ret.append(seli_data.SerializeToString()) 
	return list_ret

def hero_msg_data_serlia(hero):
	seli_data = message_pb2.Hero_msg()
	seli_data.uid = hero.uid
	seli_data.point_x = hero.x
	seli_data.point_y = hero.y

	list_ret =[]
	length = seli_data.ByteSize()
	#print("hero_msg_data_serlia:length=%d"%length)
	size = chr(seli_data.ByteSize())
	#print("hero_msg_data_serlia:size=%s"%size)
	list_ret.append(size)
	list_ret.append(seli_data.SerializeToString()) 
	return list_ret

def connect_data_serlia(hero):
	seli_data = message_pb2.Connect_req()

	list_ret =[]
	size = chr(seli_data.ByteSize())
	list_ret.append(size)
	list_ret.append(seli_data.SerializeToString()) 
	return list_ret


def serialize_data(hero,type):
	if(type == LOG_REQ):
		return login_data_serlia(hero)

	elif (type == HERO_MSG_REQ):
		return hero_msg_data_serlia(hero)

	elif (type == CONNECT_REQ):
		return connect_data_serlia(hero)
	

def package_data_send(seria_list,type):
	type_s = type
	pack_data = seria_list[0] + type_s + seria_list[1] 
	#print("len = %s"%pack_data)
	return pack_data


def data_send(sock,pack_data):
	print pack_data
	sock.sendall(pack_data)

def client_send(sock,hero,lock):
	while True:
		time.sleep(0.1)
		#sock.sendall("hellow tcp server")
		lock.acquire()  #get lock

		try:
			seli_data = serialize_data(hero,HERO_MSG_REQ)
		finally:
			lock.release()

		pack_data = package_data_send(seli_data,HERO_MSG_REQ)
		data_send(sock,pack_data)



def client_recv(sock,buff_recv):
	while True:
		data = sock.recv(1)
		if data:
			size = ord(data)

		data = sock.recv(1)
		if data:
			type = data

		data = sock.recv(size)
		if(data != size)
			print("recv err! exit")
			exit()

		Parse_data(type,data)
		print(data)


	

def connect_data_parse(data):
	connect_rsp = message_pb2.Connect_rsp()
	connect_rsp.ParseFromString(data)
	return connect_rsp

def enemy_msg_data_parse(data):
	enemy_msg = message_pb2.Enemy_msg()
	enemy_msg.ParseFromString(data)
	return enemy_msg

def login_data_parse(data):
	login_rsp = message_pb2.Login_rsp()
	login_rsp.ParseFromString(data)
	return login_rsp


def Parse_data(type,data,buff_recv):
	if(type == LOG_RSP):
		return login_data_parse(data)

	elif (type == ENEMY_MSG):
		return enemy_msg_data_parse(data)

	elif (type == CONNECT_RSP):
		return connect_data_parse(data)

def log_in(login_rsp,hero,game):
	if(login_rsp.success == True):
		hero.set_position(login_rsp.x,login_rsp.y)
		game.set_enemy_num(login_rsp.enemy_num)
		hero.set_uid(login_rsp.uid)
	else:
		print("log_in err")
		exit()

def scene_load(hero,game):
	


def handle_game_logic(type,data,hero,game):
	if(type == LOG_RSP):
		login_rsp = login_data_parse(data)
		log_in(login_rsp,hero,game)

	elif (type == ENEMY_MSG):
		enemy_msg = enemy_msg_data_parse(data)

	elif (type == CONNECT_RSP):
		connect_rsp = connect_data_parse(data)	

def main():

	buff_recv = []
	enemy_list = []
	screen = pygame.display.set_mode((PIC_X,PIC_Y),0,32)
	background = pygame.image.load(BACK_PIC_PATH)
	lock = threading.Lock()
	hero = HERO_PLAYER(screen,lock)
	enemy = ENEMY_PLAYER(screen)
	game = GAME()
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ADDRESS, PORT)) 
	
	print('thread %s is running...' %threading.current_thread().name)
	thread_read = threading.Thread(target=client_send,args=(sock,hero,lock))
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