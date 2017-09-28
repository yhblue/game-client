from proto import Deserialize,ProtoType,ProtoFormat
from connect import Socket
from queue import MsgQueue
from game import Game

import threading
import time
import sys

#-------------------------3 thread--------------------------------------#
''' socket recieve thread '''
def dispose_recv_message(socket,msg_que):
	sock = socket
	pack_size = 0 
	pack_type = 0
	content = 0
	unpack = Deserialize()
	queue = msg_que.get_game_thread_que()
	print "---recieve thread running---"
	while True:
		data = sock.recv(ProtoFormat.DATA_LEN_SIZE)    #one size
		if data:
			pack_size = ord(data) 					   #get data len

		data = sock.recv(pack_size)
		if data:
			pack_type = data[ProtoFormat.PROTO_TYPE_INDEX]
			content = data[ProtoFormat.PROTO_CONTENT_INDEX:]

		assert(pack_size == len(data))

		msg_list = {}
		msg_list[ProtoFormat.PROTO_TYPE_INDEX] = pack_type
		msg_list[ProtoFormat.PROTO_CONTENT_INDEX] = content

		msg_list = unpack.msg_data_deseria(msg_list);  #unpack
		queue.put(msg_list)		 					   #push to queue
		del msg_list



''' socket send thread '''
def dispose_send_message(socket,msg_que):
	sock = socket
	queue = msg_que.get_send_thread_que()
	print "---send thread running---"
	while True:
		if not queue.empty():
			qnode = queue.get()	
			if qnode:
				sock.sendall(qnode)
		else:
			#pass
			time.sleep(0.05)



''' game thread '''
def dispose_game_logic(socket,msg_que):
	print "...game thread run..."
	
	game_play = Game(socket,msg_que)
	game_play.game_start_run()


''' main function '''
def main():

	sock = Socket()
	sock.socket_connect()
	socket = sock.get_socket()
	msg_queue = MsgQueue()

	thread_read = threading.Thread(target=dispose_recv_message,args=(socket,msg_queue,))
	thread_write = threading.Thread(target=dispose_send_message,args=(socket,msg_queue,))
	thread_game = threading.Thread(target=dispose_game_logic,args=(socket,msg_queue,))

	thread_read.start()
	thread_write.start()	
	thread_game.start()

	thread_read.join()
	thread_write.join()
	thread_game.join()

	# print "close socket"
	# sock.socket_close()
	# sys.exit()


if __name__ == "__main__":
	main()


#-------------------------------------------------------------------------#