import socket
import message_pb2
import time
addr = "127.0.0.1"
port = 8000

def hero_msg_data_serlia(uid,x,y,type):
	seli_data = message_pb2.hero_msg()
	seli_data.uid = uid
	seli_data.point_x = x
	seli_data.point_y = y

	list_ret =[]
	length = seli_data.ByteSize()
	size = chr(length+len(type))
	list_ret.append(size)
	list_ret.append(type)
	list_ret.append(seli_data.SerializeToString()) 
	return list_ret


def recv_data(sock):
	data = sock.recv(1) 
	pack_size = 0 
	pack_type = 0

	if data:
		pack_size = ord(data) 			#get data len

	data = sock.recv(1)
	if data:
		pack_type = data     			#get proto type

	content_len = pack_size-len(data)	
	data = sock.recv(content_len)	#get content
	assert(content_len == len(data))

	list_ret = []
	list_ret.append(pack_type)
	list_ret.append(content_len)

	if(pack_type == 'l'):
		rsp = message_pb2.login_rsp()
		rsp.ParseFromString(data)
		print ("rsp.success = %d"%rsp.success)
		print ("rsp.point_x = %d"%rsp.point_x)
		print ("rsp.point_y = %d"%rsp.point_y)
		print ("rsp.enemy_num = %d"%rsp.enemy_num)
		print ("rsp.uid = %d"%rsp.uid)
		list_ret.append(rsp)
	
	return list_ret
	

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((addr,port)) 
	print "connect success"

	send_list = hero_msg_data_serlia(32*1024,380,840,'H')

	for val in send_list:
		print val
		sock.sendall(val)
		time.sleep(0.1)

	while True:
		recv_data(sock);



if __name__ == "__main__":
	main()


