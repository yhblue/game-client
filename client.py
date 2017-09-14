import socket
import message_pb2

addr = "127.0.0.1"
port = 8000

def hero_msg_data_serlia(uid,x,y,type):
	seli_data = message_pb2.Hero_msg()
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


def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((addr, port)) 
	print "connect success"

	send_list = hero_msg_data_serlia(128,30,40,'H')

	for val in send_list:
		print send
		sock.sendall(val)


if __name__ == "__main__":
	main()



# send_list = ["hello","world","welcome","to","use","python"]
# for val in send_list:
# 	print val

# send_list = []
# size = 65
# send = chr(size)
# send_list.append(send)
# send_list.append(' ')
# send_list.append('L')
# send_list.append(' ')
# send_list.append("hello")