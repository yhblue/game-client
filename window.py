import pygame
from pygame.locals import *
import time
import socket
import threading
import message_pb2
import sys
import Queue

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
PORT = 8000

LOG_REQ = 'L'
LOG_RSP = 'l'

HERO_MSG_REQ = "H"
HERO_MSG_RSP = 'h'

CONNECT_REQ = 'C'
CONNECT_RSP = 'c'

HEART_REQ = 'R'
HEART_REQ = 'r'

ENEMY_MSG = 'e'

NEW_ENEMY = 'n'

GAME_START = 's'

QUEUE_MAX_SIZE = 1024
QUEUE_GAME_THREAD = "queue_game_thread"
QUEUE_SEND_THREAD = "queue_send_thread"

PROTO_TYPE_INDEX = 0
PROTO_SIZE_INDEX = 1

class Hero_Play(object):
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

	def set_position(x,y):
		self.x = x
		self.y = y

	def set_connect(flag):
		self.connect = flag

class Enemy_Player(object):
	"""docstring for enemy"""
	def __init__(self, screen):
		self.uid = 0
		self.x = 0
		self.y = 0
		self.screen = screen
		self.image = pygame.image.load(ENEMY_PIC_PATH);

	def display(self):
		self.screen.blit(self.image, (self.x,self.y))

	def update_msg(x,y):
		self.x = x
		self.y = y

class Game(object):
	"""docstring for game"""
	def __init__(self):
		self.uid2enemy_dic = {}
		self.enemy_num = 0
		self.connect = False
		self.log_in = False

	def append_enemy(self,key_uid,val_enemy):
		self.uid2enemy_dic(self,key_uid,val_enemy)

	def set_enemy_num(self,num):
		self.enemy_num = num

	def enemy_num_increase(self):
		self.enemy_num += 1

	def get_enemy_num(self):
		if(len(self.uid2enemy_dic) == self.enemy_num):
			return self.enemy_num
		else:
			print("get_enemy_num err")
			exit()

	def remv_enemy(self,key_uid):
		del self.uid2enemy_dic[key_uid]
		
	def update_enemy_msg(self,key_uid,x,y):
		self.uid2enemy_dic[key_uid].update_msg(x,y)

	def enemy_display(self,key_uid):
		self.uid2enemy_dic[key_uid].display()


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

			elif event.key == K_ESCAPE:
				sys.exit()

		elif event.type ==  KEYUP:
			hero.down = False
			hero.left = False			
			hero.right = False
			hero.up = False


def login_data_serlia(hero,type):
	seli_data = message_pb2.Login_req()
	seli_data.name = hero.name
	seli_data.point_x = hero.x
	seli_data.point_y = hero.y
	list_ret = []
	size = chr(seli_data.ByteSize()+len(type))
	list_ret.append(size)
	list_ret.append(type)
	list_ret.append(seli_data.SerializeToString()) 
	return list_ret

def hero_msg_data_serlia(hero,type):
	seli_data = message_pb2.Hero_msg()
	seli_data.uid = hero.uid
	seli_data.point_x = hero.x
	seli_data.point_y = hero.y

	list_ret =[]
	length = seli_data.ByteSize()
	size = chr(seli_data.ByteSize()+len(type))
	list_ret.append(size)
	list_ret.append(type)
	list_ret.append(seli_data.SerializeToString()) 
	return list_ret

def connect_data_serlia(hero,type):
	seli_data = message_pb2.Connect_req()

	list_ret =[]
	size = chr(seli_data.ByteSize()+len(type))
	list_ret.append(size)
	list_ret.append(type)
	list_ret.append(seli_data.SerializeToString()) 
	return list_ret


def serialize_data(hero,type):
	if(type == LOG_REQ):
		return login_data_serlia(hero,type)

	elif (type == HERO_MSG_REQ):
		return hero_msg_data_serlia(hero,type)

	elif (type == CONNECT_REQ):
		return connect_data_serlia(hero,type)
	

def package_data_send(seria_list,type):
	type_s = type
	pack_data = seria_list[0] + type_s + seria_list[1] 
	return pack_data


def data_send(sock,pack_data):
	print pack_data
	sock.sendall(pack_data)


def client_send(sock,hero,lock,queue_dic):
	while True:
		time.sleep(0.1)
		lock.acquire()  #get lock

		try:
			seli_data = serialize_data(hero,HERO_MSG_REQ)
		finally:
			lock.release()

		pack_data = package_data_send(seli_data,HERO_MSG_REQ)
		data_send(sock,pack_data)

#------------------------------------------------------------------------
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

def new_enemy_data_parse(data):
	new_enemy = message_pb2.New_enemy()
	new_enemy.ParseFromString(data)
	return new_enemy

def hero_msg_data_parse(data):
	hero_rsp = message_pb2.Hero_rsp()
	hero_rsp.ParseFromString(data)
	return hero_rsp
#-------------------------------------------------------------------------
def handle_log_in(login_rsp,hero,game):
	if(login_rsp.success == True):
		hero.set_position(login_rsp.x,login_rsp.y)
		game.set_enemy_num(login_rsp.enemy_num)
		hero.set_uid(login_rsp.uid)
	else:
		print("log_in err")
		exit()

def handle_enemy_msg(enemy_msg,game):
	key_uid = enemy_msg.uid
	x = enemy_msg.point_x
	y = enemy_msg.point_y
	game.update_enemy_msg(key_uid,x,y)


def handle_new_enemy(new_enemy,game,screen):
	key_uid = new_enemy.uid
	x = new_enemy.point_x
	y = new_enemy.point_y

	enemy = ENEMY_PLAYER(screen)
	enemy.update_msg(x,y)
	
	val_enemy = enemy
	game.append_enemy(key_uid,val_enemy)
	game.enemy_num_increase()

# def handle_hero_msg(hero_msg,hero):
# 	uid = hero_msg.uid
# 	x = hero_msg.point_x
# 	y = hero_msg.point_y


def handle_connect(connect_rsp,hero):
	success = connect_rsp.success
	if(success == True):
		hero.set_connect(True)

#------------------------------------------------------------------------
def handle_game_logic(type,data,hero,game,screen):
	if (type == LOG_RSP):      #if success -> in -> loader 	
		login_rsp_data = login_data_parse(data)
		handle_log_in(login_rsp_data,hero,game)

	elif (type == ENEMY_MSG):
		enemy_msg_data = enemy_msg_data_parse(data)
		handle_enemy_msg(enemy_msg_data,game)

	elif (type == CONNECT_RSP):
		connect_rsp_data = connect_data_parse(data) 
		handle_connect(connect_rsp_data)

	elif (type == NEW_ENEMY):
		new_enemy_data = new_enemy_data_parse(data)
		handle_new_enemy(new_enemy_data,game,screen)


def client_recv(sock,hero,game,screen,queue_dic):
	while True:
		pack_list = recv_data(sock)
		handle_game_logic(pack_list[0],pack_list[1],hero,game,screen)



def game_prepare(game):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ADDRESS, PORT)) 

	while True:
		pack_list = recv_data(sock)
		type = pack_list[0]
		if(type == GAME_START):
			break  #start game
		handle_game_logic(pack_list[0],pack_list[1],hero,game,screen)


def recv_data(sock):
	data = sock.recv(1)  
	if data:
		size = ord(data) 			#get data len

	data = sock.recv(1)
	if data:
		type = data     			#get proto type

	content_len = size-len(data)
	data = sock.recv(content_len)	#get content

	assert(content_len == len(data))

	list_ret = []
	list_ret.append(type)
	list_ret.append(content_len)
	list_ret.append(data)

	return list_ret


class Game_Start(object):
 	"""docstring for Game_Start"""
 	def __init__(self):
 		pass

 	def socket_connect(self,addr,port)
 		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 		self.sock.connect((addr, port));
 		return self.sock

 	def login_require(self,hero)
		data_list = serialize_data(hero,LOG_REQ)
		assert(type(data_list) == list)

		for data in data_list:
			self.sock.sendall(data)   # send 


def dispose_queue_game_event(queue):
	if queue.not_empty():
		qnode = queue.get()  #get a node
		proto_type = qnode[]
	
	else
		time.sleep(0.01)



def msg_queue_creat(queue_name_list,queue_size):
	assert(type(queue_name_list) == list)

	for name in queue_name_list:
		queue_dic[name] = Queue.Queue(queue_size)
	return queue_dic		



def main():

	screen = pygame.display.set_mode((PIC_X,PIC_Y),0,32)
	background = pygame.image.load(BACK_PIC_PATH)
	queue_dic = msg_queue_creat([QUEUE_GAME_THREAD,QUEUE_SEND_THREAD],QUEUE_MAX_SIZE)
	lock = threading.Lock()
	hero = Hero_Play(screen,lock)
	game = Game()

	game_prepare(game) 

	print('thread %s is running...' %threading.current_thread().name)
	thread_read = threading.Thread(target=client_send,args=(sock,hero,lock,queue_dic))
	thread_write = threading.Thread(target=client_recv,args=(sock,buff_recv,queue_dic))
	thread_read.start()
	thread_write.start()

	while True:
		screen.blit(background,(START_X,START_Y))
		hero.display()
		pygame.display.update()

		key_control(hero)
		hero.position_update()
		time.sleep(0.01)

	sock.close()
	thread_read.join()
	thread_write.join()
	sys.exit()

if __name__ == "__main__":
	main()


