import pygame
from pygame.locals import *
from proto import Serialize,ProtoType,ProtoFormat
from operation import Move
from connect import Socket
import time
import sys
import os


MAP_X, MAP_Y = 1000, 600
HERO_SIZE_X, HERO_SIZE_Y= 40, 40
ENEMY_SIZE_X, ENEMY_SIZE_Y = 40, 40

X_MAX = MAP_X - HERO_SIZE_X   
Y_MAX = MAP_Y - HERO_SIZE_Y

START_POSITION = (0,0)

HERO_PIC_PATH = "./pic/hero.png"
ENEMY_PIC_PATH = "./pic/enemy.png"
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
		self.move = Move.STOP

	def msg_load(self,uid,x,y):
		self.uid = uid
		self.x = x
		self.y = y

	def msg_update(self,x,y):
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

	def player_move(self,operation):
		self.move = operation

	def get_operation(self):
		return self.move

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
		self.screen.blit(self.image,(self.x,self.y))

	def msg_update(self,x,y):
		self.x = x
		self.y = y

	def set_position(self,x,y):
		self.x = x
		self.y = y		


class Game(object):
	def __init__(self,socket,msg_queue):
		self.screen = pygame.display.set_mode((MAP_X,MAP_Y),0,32)
		self.background = pygame.image.load(BACK_PIC_PATH)
		self.enemy_list = {}
		self.enemy_num = 0
		self.msg_queue = msg_queue
		self.queue_send = self.msg_queue.get_send_thread_que()
		self.queue_game = self.msg_queue.get_game_thread_que()
		self.pack = Serialize()
		self.hero = HeroPlayer(self.screen)
		self.log_in = False
		self.start = False
		self.sock = socket
		self.count_hero = 0
		self.cont_enemy = 0		

	def hero_creat(self):
		return HeroPlayer(self.screen)

	def enemy_creat(self):
		'''append a new enemy to dic'''
		return EnemyPlayer(self.screen)

	def enemy_append(self,enemy):
		uid = enemy.get_uid()
		self.enemy_list[uid] = enemy
		self.enemy_num += 1 

	def remove_enemy(self,uid):
		del self.enemy_list[uid]
		self.enemy_num -= 1

	def update_enemy_msg(self,uid,x,y):
		self.enemy_list[uid].msg_update(x,y)
		#self.enemy_list[uid].update_display()    #draw
		#pygame.display.update()			      #update

	def game_update_display(self):
		self.screen.blit(self.background,START_POSITION)
		self.hero.update_display()
		for uid,enemy in self.enemy_list.items(): #dict type
			if enemy:
				enemy.update_display()
		pygame.display.update()   				  #necessary

	def send_request(self,req_list):
		self.queue_send.put(req_list)

	def login_request(self):
		name = self.hero.get_name()
		req_list = self.pack.login_request_seria(name,ProtoType.LOG_REQ)   
		self.send_request(req_list)
		print "login request send"

	def leave_request(self):
		uid = self.hero.get_uid()
		req_list = self.pack.leave_request_seria(uid,ProtoType.LEAVE_REQ)
		self.send_request(req_list)
		print "leave request send"

	def start_request(self,start):
		req_list = self.pack.start_request_seria(start,ProtoType.START_REQ)
		self.send_request(req_list)

	def move_request(self,operation):
		req_list = self.pack.move_request_seria(operation,ProtoType.MOVE_REQ)
		self.send_request(req_list)
		#print "move request"

	def dispose_game_login(self,qnode):
		msg_type = qnode[ProtoFormat.PROTO_TYPE_INDEX]
		rsp = qnode[ProtoFormat.PROTO_CONTENT_INDEX]
		
		if msg_type == ProtoType.LOG_RSP:
			if rsp.success == True:
				self.hero.msg_load(rsp.uid,rsp.point_x,rsp.point_y)
				self.enemy_num = rsp.enemy_num
				# print "***LOG_RSP***"
				# print ("rsp.success = %d"%rsp.success)
				# print ("rsp.point_x = %d"%rsp.point_x)
				# print ("rsp.point_y = %d"%rsp.point_y)
				# print ("rsp.enemy_num = %d"%rsp.enemy_num)
				# print ("rsp.uid = %d"%rsp.uid)

		elif msg_type == ProtoType.HERO_MSG_RSP:
			self.hero.msg_load(rsp.uid,rsp.point_x,rsp.point_y)

		elif msg_type == ProtoType.ENEMY_MSG:#existed player
			enemy = self.enemy_creat()
			print "existed enemy"
			enemy.msg_load(rsp.uid,rsp.point_x,rsp.point_y)
			self.enemy_append(enemy)

		elif msg_type == ProtoType.START_RSP:
			if self.log_in == True:
				self.start = rsp.start
			else:
				print "login error"
				sys.exit()

		elif msg_type == ProtoType.LOGIN_END:		#break	
			if rsp.success == True:
				self.log_in = True
				print "login success"	
				self.start_request(True)	

	def dispose_move_rsp(self,msg_rsp):
		rsp = msg_rsp
		if rsp.success == True:
			if rsp.uid == self.hero.get_uid():
				# print("suc=%d"%rsp.success)
				# print("uid=%d"%rsp.uid)
				# print("x=%d"%rsp.pos_x)
				# print("y=%d,"%rsp.pos_y)
				self.hero.msg_update(rsp.pos_x,rsp.pos_y)
		else:
			print "can not move"

	def dispose_new_enemy_msg(self,msg_rsp): #ENEMY_MSG
		rsp = msg_rsp
		enemy = self.enemy_creat()
		enemy.msg_load(rsp.uid,rsp.point_x,rsp.point_y)
		self.enemy_append(enemy)	

	def dispose_enemy_msg(self,msg_rsp):
		rsp = msg_rsp
		uid = rsp.uid
		if uid != self.hero.get_uid():
			self.update_enemy_msg(rsp.uid,rsp.point_x,rsp.point_y)
			self.cont_enemy += 1
			print("enemy:%d"%self.cont_enemy)
		else:
			self.hero.msg_update(rsp.point_x,rsp.point_y)
			self.count_hero += 1
			print("hero:%d"%self.count_hero)

	def dispose_enemy_leave_msg(self,msg_rsp):
		rsp = msg_rsp
		uid = rsp.uid
		print type(msg_rsp)
		if uid != self.hero.get_uid():
			self.remove_enemy(uid)
		else:
			pass

	def dispose_leave_rsp(self,msg_rsp):
		rsp = msg_rsp
		if rsp.leave == True:			#what shuould i do? exit
			#self.sock.socket_close()
			self.sock.close()
			print "close socket"
			os._exit(0)
		else:							#if false,again
			self.leave_request()
			

	def dispose_game_logic(self,qnode):
		msg_type = qnode[ProtoFormat.PROTO_TYPE_INDEX]
		rsp = qnode[ProtoFormat.PROTO_CONTENT_INDEX]
		print("msg_type = %c"%msg_type)
		if msg_type == ProtoType.MOVE_RSP:
			#print "dispose move rsp"
			#self.dispose_move_rsp(rsp)
			pass

		elif msg_type == ProtoType.NEW_ENEMY:
			print "new enemy"
			self.dispose_new_enemy_msg(rsp)

		elif msg_type == ProtoType.ENEMY_MSG:
			#print "enemy msg"
			self.dispose_enemy_msg(rsp)

		elif msg_type == ProtoType.ENEMY_LEAVE:
			print "enemy leave"
			self.dispose_enemy_leave_msg(rsp)

		elif msg_type == ProtoType.LEAVE_RSP:
			print "leave rsp"
			self.dispose_leave_rsp(rsp)

	def key_control(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				print "QUIT"

			elif event.type ==  KEYDOWN:
				if event.key == K_LEFT:
					print "left"
					self.hero.player_move(Move.LEFT)

				elif event.key == K_RIGHT:
					print "right"
					self.hero.player_move(Move.RIGHT)

				elif event.key == K_UP:
					print "up"
					self.hero.player_move(Move.UP)

				elif event.key == K_DOWN:
					print "down"
					self.hero.player_move(Move.DOWN)

				elif event.key == K_ESCAPE:
					self.leave_request() #leave request -> wait to leave 	
					#os._exit(0)		

			elif event.type == KEYUP:
				self.hero.player_move(Move.STOP)
				pass

		move = self.hero.get_operation()
		if move == Move.STOP:
			pass
		else:
			self.move_request(move)
			#time.sleep(0.05);

	def game_start_prepare(self):
		self.login_request()
		while not self.start:
			if not self.queue_game.empty():
				qnode = self.queue_game.get()
				if qnode:
					self.dispose_game_login(qnode)
					print "queue game get msg"
			else:
				pass
				#time.sleep(0.05)
				#print "wait for login success"			

	def game_start_run(self):
		self.game_start_prepare()
		if self.start == True:
			self.game_update_display()
			print "----start the game-----"

			while True:
				if not self.queue_game.empty():
					qnode = self.queue_game.get()
					if qnode:
						self.dispose_game_logic(qnode)
						
				self.key_control()
				self.game_update_display()
				time.sleep(0.05);
		else:
			print "start error"
			sys.exit()

