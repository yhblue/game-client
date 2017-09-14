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

HERO_MSG_REQ = 'H'
HERO_MSG_RSP = 'h'

LEAVE_REQ = 'V'
LEAVE_RSP = 'v'

START_RSP = 's'
START_REQ = 'S'

MOVE_REQ = 'M'
MOVE_RSP = 'm'

ENEMY_MSG = 'e'

NEW_ENEMY = 'n'  

LOGIN_END = 'i'

QUEUE_MAX_SIZE = 1024
QUEUE_GAME_THREAD = "queue_game_thread"
QUEUE_SEND_THREAD = "queue_send_thread"

PROTO_SIZE_INDEX = 1
PROTO_TYPE_INDEX = 2
PROTO_CONTENT_INDX = 3

class Hero_Play(object):
	"""docstring for player"""
	def __init__(self,screen):
		self.x = 0
		self.y = 0
		self.uid = 0
		self.name = "viki"
		self.screen = screen
		self.image = pygame.image.load(HERO_PIC_PATH);
		self.up = False
		self.left = False
		self.right = False
		self.down = False

	def set_uid(self,uid):
		self.uid = uid

	def set_position(x,y):
		self.x = x
		self.y = y

	def set_connect(flag):
		self.connect = flag

	def get_uid(self):
		return self.uid

	def get_position_x(self):
		return self.x

	def get_position_y(self):
		return self.y

	def get_name(self):
		return self.name	

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
		elif(self.down == True):
			self.move_down()
		elif(self.left == True):
			self.move_left()
		elif(self.right == True):
			self.move_right()	


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

	def hero_creat(hero):
		self.hero = hero

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


class Serialize(object):
	"""docstring for Serialize"""
	def __init__(self):
		pass

	def hero_msg_seria(hero,type):
		seria_data = message_pb2.hero_msg()
		seria_data.uid = hero.get_uid()
		seria_data.point_x = hero.get_position_x()
		seria_data.point_y = hero.get_position_y()

		list_ret =[]
		size = chr(seria_data.ByteSize()+len(type))  #get length
		list_ret.append(size)
		list_ret.append(type)
		list_ret.append(seria_data.SerializeToString()) 
		return list_ret		

	def login_require_seria(hero,type):
		seria_data = message_pb2.login_req()
		seria_data.name = hero.get_name()

		list_ret = []
		size = chr(seria_data.ByteSize()+len(type))
		list_ret.append(size)
		list_ret.append(type)
		list_ret.append(seria_data.SerializeToString()) 
		return list_ret

	def start_request_seria(start,type):
		seria_data = message_pb2.start_req()
		seria_data.start = start

		list_ret = []
		size = chr(seria_data.ByteSize()+len(type))
		list_ret.append(size)
		list_ret.append(type)
		list_ret.append(seria_data.SerializeToString()) 
		return list_ret				

	def move_request_seria(operation,type):
		seria_data = message_pb2.move_req()
		seria_data.move = operation

		list_ret = []
		size = chr(seria_data.ByteSize()+len(type))
		list_ret.append(size)
		list_ret.append(type)
		list_ret.append(seria_data.SerializeToString()) 
		return list_ret		


class Deserialize(object):
	"""docstring for Deserialize"""
	def __init__(self):
		pass

	def msg_data_deseria(self,data_list):
		assert(type(data_list) == list)

		rsp_list = []
		rsp = 0
		msg_type = data_list[PROTO_SIZE_INDEX]
		msg_size = data_list[PROTO_TYPE_INDEX] 
		content = data_list[PROTO_CONTENT_INDX]

		if msg_type == LOG_RSP:
			rsp = message_pb2.login_rsp()
			rsp.ParseFromString(content)

		elif msg_type == ENEMY_MSG:
			rsp = message_pb2.enemy_msg()
			rsp.ParseFromString(content)

		elif msg_type == NEW_ENEMY:
			rsp = message_pb2.new_enemy()
			rsp.ParseFromString(content)

		elif msg_type == START_RSP:
			rsp = message_pb2.start_rsp()
			rsp.ParseFromString(content)

		elif msg_type == LOGIN_END:
			rsp = message_pb2.login_end()
			rsp.ParseFromString(content)

		elif msg_type == MOVE_RSP:
			rsp = message_pb2.move_rsp()
			rsp.ParseFromString(content)

		elif msg_type == LEAVE_RSP:
			rsp = message_pb2.leave_rsp()
			rsp.ParseFromString(content)			

		rsp_list.append(msg_type)
		rsp_list.append(msg_size)
		rsp_list.append(rsp)

		return rsp_list

#----------------------handle service rsp---------------------------------------------------
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

def handle_game_logic(type,data,hero,game,screen):
#------------------------------------------------------------------------

def game_prepare(game):

	while True:



class Game_Start(object):
 	"""docstring for Game_Start"""
 	def __init__(self):
 		pass


#-------------------------3 thread--------------------------------------
#read thread
def dispose_recv_message(sock,queue_dic):
	pack_size = 0 
	pack_type = 0
	msg_list = []
	unpack = Deserialize()
	queue = queue_dic[QUEUE_GAME_THREAD]

	while True:
		data = sock.recv(1) 
		if data:
			pack_size = ord(data) 			#get data len

		data = sock.recv(1)
		if data:
			pack_type = data     			#get proto type

		content_len = pack_size-len(data)	
		data = sock.recv(content_len)		#get content
		assert(content_len == len(data))

		msg_list[PROTO_SIZE_INDEX] = content_len
		msg_list[PROTO_TYPE_INDEX] = pack_type
		msg_list[PROTO_CONTENT_INDX] =  data

		unpack.msg_data_deseria(msg_list);  #unpack
		msg_list = queue.put(msg_list)	




def dispose_game_logic():


def dispose_send_message():

		if msg_type == LOG_RSP:
			rsp = message_pb2.login_rsp()
			rsp.ParseFromString(content)

		elif msg_type == ENEMY_MSG:
			rsp = message_pb2.enemy_msg()
			rsp.ParseFromString(content)

		elif msg_type == NEW_ENEMY:
			rsp = message_pb2.new_enemy()
			rsp.ParseFromString(content)

		elif msg_type == START_RSP:
			rsp = message_pb2.start_rsp()
			rsp.ParseFromString(content)

		elif msg_type == LOGIN_END:
			rsp = message_pb2.login_end()
			rsp.ParseFromString(content)

		elif msg_type == MOVE_RSP:
			rsp = message_pb2.move_rsp()
			rsp.ParseFromString(content)

		elif msg_type == LEAVE_RSP:


def socket_connect(addr,port)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((addr, port));
	return sock

def game_start_prepare(hero):
	while True:

		if queue.not_empty():
			qnode = queue.get()  #get a node
			if qnode:
				msg_type = qnode[PROTO_TYPE_INDEX]

				if msg_type == LOG_RSP:

				elif msg_type == ENEMY_MSG:

				elif msg_type == NEW_ENEMY:

				elif msg_type == START_RSP:

				elif msg_type == LOGIN_END:
			
			elif



def main():
	sock = socket_connect(ADDRESS,PORT)
	game = Game()
	game.();


def dispose_queue_game_event(queue):
	if queue.not_empty():
		qnode = queue.get()  #get a node
		msg_type = qnode[PROTO_TYPE_INDEX]	
		if msg_type == LOG_RSP:

		elif msg_type == ENEMY_MSG:

		elif msg_type == NEW_ENEMY:

		elif msg_type == START_RSP:

		elif msg_type == LOGIN_END:

		elif msg_type == MOVE_RSP:

		elif msg_type == LEAVE_RSP:


	else
		time.sleep(0.01)

def 


def msg_queue_creat(queue_name_list,queue_size):
	assert(type(queue_name_list) == list)

	for name in queue_name_list:
		queue_dic[name] = Queue.Queue(queue_size)
	return queue_dic		



def main():

	screen = pygame.display.set_mode((PIC_X,PIC_Y),0,32)
	background = pygame.image.load(BACK_PIC_PATH)
	queue_dic = msg_queue_creat([QUEUE_GAME_THREAD,QUEUE_SEND_THREAD],QUEUE_MAX_SIZE)

	hero = Hero_Play(screen)
	game = Game()
	game.hero_creat(hero)
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


