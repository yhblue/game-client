from proto import Deserialize
from connect import Socket
from queue import MsgQueue
from game import Game

import threading
import time
import sys

#-------------------------3 thread--------------------------------------#
''' socket recieve thread '''
def dispose_recv_message(sock,queue_dic):
	pack_size = 0 
	pack_type = 0
	unpack = Deserialize()
	queue = queue_dic[QUEUE_GAME_THREAD]
	msg_format = ProtoFormat()

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

		msg_list = []
		msg_list[msg_format.PROTO_SIZE_INDEX] = content_len
		msg_list[msg_format.PROTO_TYPE_INDEX] = pack_type
		msg_list[msg_format.PROTO_CONTENT_INDEX] = data

		unpack.msg_data_deseria(msg_list);   #unpack
		msg_list = queue.put(msg_list)		 #push to queue

''' socket send thread '''
def dispose_send_message():
	while True:
		time.sleep(1)
		print "send thread running"
'''
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
'''		

''' game thread '''
def dispose_game_logic():
	game_play = Game()
	game_play.game_run()


''' main function '''
def main():

	sock = Socket()
	sock.socket_connect()
	socket = sock.get_socket()
	msg_queue = msg_queue_creat([QUEUE_GAME_THREAD,QUEUE_SEND_THREAD],QUEUE_MAX_SIZE)

	thread_read = threading.Thread(target=dispose_recv_message,args=(socket,msg_queue))
	thread_write = threading.Thread(target=dispose_send_message,args=(socket,msg_queue))
	thread_game = threading.Thread(target=dispose_game_logic,arg=(msg_queue))

	thread_read.start()
	thread_write.start()	
	thread_game.start()

	thread_read.join()
	thread_write.join()
	thread_game.join()

	sock.socket_close()
	sys.exit()


if __name__ == "__main__":
	main()


#----------------------handle service rsp---------------------------------------------------

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
	pass
'''
	









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









'''
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




'''