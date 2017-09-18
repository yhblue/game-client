import pygame
from pygame.locals import *
from proto import Serialize
import time
import sys

MAP_X, MAP_Y = 1000, 600
HERO_SIZE_X, HERO_SIZE_Y= 40, 40
ENEMY_SIZE_X, ENEMY_SIZE_Y = 40, 40

X_MAX = MAP_X - HERO_SIZE_X   
Y_MAX = MAP_Y - HERO_SIZE_Y

START_POSITION = (0,0)

HERO_PIC_PATH = "./pic/hero.jpg"
ENEMY_PIC_PATH = "./pic/enemy.jpg"
BACK_PIC_PATH = "./pic/background.jpg"

class HeroPlayer(object):
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

	def msg_load(self,uid,x,y):
		self.uid = uid
		self.x = x
		self.y = y

	def msg_update(x,y):
		self.x = x
		self.y = y

	def get_uid(self):
		return self.uid

	def get_position_x(self):
		return self.x

	def get_position_y(self):
		return self.y

	def get_name(self):
		return self.name	

	def update_display(self):
		self.screen.blit(self.image, (self.x,self.y))

class EnemyPlayer(object):
	"""docstring for enemy"""
	def __init__(self, screen):
		self.uid = 0
		self.x = 0
		self.y = 0
		self.screen = screen
		self.image = pygame.image.load(ENEMY_PIC_PATH)

	def msg_load(self,uid,x,y):
		self.uid = uid
		self.x = x
		self.y = y

	def get_uid(self):
		return self.uid

	def update_display(self):
		self.screen.blit(self.image, (self.x,self.y))

	def msg_update(x,y):
		self.x = x
		self.y = y

	def set_position(self,x,y):
		self.x = x
		self.y = y		

class Game(object):
	def __init__(self,msg_queue):
		self.screen = pygame.display.set_mode((MAP_X,MAP_Y),0,32)
		self.background = pygame.image.load(BACK_PIC_PATH)
		self.enemy_list = {}
		self.enemy_num = 0
		self.msg_queue = msg_queue
		self.queue_send = self.msg_queue.get_send_thread_que()
		self.queue_game = self.msg_queue.get_game_thread_que()
		self.pack = Serialize()
		self.proto_type = ProtoType()
		self.msg_format = ProtoFormat()
		self.log_in = False
		self.start = False

	def hero_creat(self):
		return HeroPlayer(slef.screen)

	def enemy_creat(self,uid):
		'''append a new enemy to dic'''
		return EnemyPlayer(slef.screen)

	def enemy_append(self,enemy):
		uid = enemy.get_uid()
		self.enemy_list[uid] = enemy
		self.enemy_num += 1 

	def remove_enemy(self,uid):
		del enemy_list[uid]
		self.enemy_num -= 1

	def update_enemy_msg(self,uid,x,y):
		self.enemy_list[key_uid].update_msg(x,y)
		self.enemy_list[key_uid].update_display()  	#draw
		pygame.display.update()					    #update

	def game_update_display(self):
		self.screen.blit(background,START_POSITION)
		self.hero.update_display()
		for enemy in self.enemy_list:
			enemy.update_display()
		pygame.display.update()   #necessary

	def login_require(self):
		req_list = []
		req_list = self.pack.login_require_seria(self.hero,self.proto_type.LOG_REQ)   
		queue_game.put(self.req_list)

	def dispose_game_login(self,qnode):
		msg_type = qnode[self.msg_format.PROTO_TYPE_INDEX]
		rsp = qnode[self.msg_format.PROTO_CONTENT_INDEX]

		if msg_type == self.proto_type.LOG_RSP:
			if rsp.success == True:
				self.hero = self.hero_creat()
				self.msg_load(rsp.uid,rsp.point_x,rsp.point_y)
				self.enemy_num = rsp.enemy_num

		elif msg_type == self.proto_type.HERO_MSG_RSP:
			if hasattr(self,"hero") == False:
				self.hero = self.hero_creat()
			self.msg_load(rsp.uid,rsp.point_x,rsp.point_y)

		elif msg_type == self.proto_type.NEW_ENEMY:
			enemy = self.enemy_creat()
			enemy.msg_load(rsp.uid,rsp.point_x,rsp.point_y)
			self.enemy_append(enemy)

		elif msg_type == self.proto_type.START_RSP:
			if rsp.log_in == True:
				self.start = rsp.start
			else:
				print "login error"
				sys.exit()

		elif msg_type == self.proto_type.LOGIN_END:		#break	
			if rsp.success == True:
				self.log_in = True
				print "login success"		

		def dispose_move_rsp(self,msg_rsp):
			rsp = msg_rsp
			if rsp.success == True:
				if rsp.uid == self.hero.get_uid():
					self.hero.msg_update(rsp.pos_x,rsp.pos_y)
					print "hero move"


	def dispose_game_logic(self,qnode):
		msg_type = qnode[self.msg_format.PROTO_TYPE_INDEX]
		rsp = qnode[self.msg_format.PROTO_CONTENT_INDEX]

		if msg_type == self.proto_type.MOVE_RSP:
			self.dispose_move_rsp(rsp)

		elif msg_type == self.proto_type.NEW_ENEMY:
			pass

		elif msg_type == self.proto_type.ENEMY_MSG:
			pass

		elif msg_type == self.proto_type.ENEMY_LEAVE:
			pass

		elif msg_type == self.proto_type.LEAVE_RSP:
			pass

	def game_start_prepare(self):
		self.login_require()
		while True:
			if not self.queue_game.empty():
				self.qnode = self.queue_game.get()
				if self.qnode:
					self.dispose_game_login(qnode)
			else:
				time.sleep(1)
				print "wait for login success"			

	def game_run(self):
		self.game_start_prepare()
		if self.start == True:
			print "start the game"
			while True:
				if not self.queue_game.empty():
					self.qnode = self.queue_game.get()
					if self.qnode:
						self.dispose_game_logic(qnode)
				else:	#key control
					time.sleep(0.01)
		else:
			print "start error"
			sys.exit()

	
'''

		while True:

			if self.queue_game.empty():
				time.sleep(0.01)

			else:
				self.qnode = self.queue_game.get()
				if self.qnode:
					self.msg_type = qnode[PROTO_TYPE_INDEX]
					if self.msg_type == self.proto_type.HERO_MSG_RSP:

					elif self.msg_type == self.proto_type.LEAVE_RSP:

					elif self.msg_type == self.proto_type.MOVE_RSP:

					elif self.msg_type == self.proto_type.NEW_ENEMY:

					elif self.msg_type == self.proto_type.ENEMY_MSG:

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
'''

'''
class Game(object):
	"""docstring for game"""
	def __init__(self,msg_queue):
		self.screen = pygame.display.set_mode((MAP_X,MAP_Y),0,32)
		self.background = pygame.image.load(BACK_PIC_PATH)
		self.uid2enemy_dic = {}
		self.enemy_num = 0
		self.log_in = False
		self.msg_queue = msg_queue

	def hero_creat(slef):
		self.hero = HeroPlayer(slef.screen)

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

	def remove_enemy(self,key_uid):
		del self.uid2enemy_dic[key_uid]
		
	def update_enemy_msg(self,key_uid,x,y):
		self.uid2enemy_dic[key_uid].update_msg(x,y)

	def enemy_display(self,key_uid):
		self.uid2enemy_dic[key_uid].display()

	def game_update_display(self):
		self.screen.blit(background,START_POSITION)
		self.hero.update_display()
		pygame.display.update()

	def game_run(self):



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

'''