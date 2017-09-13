import socket

addr = "127.0.0.1"
port = 8000

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((addr, port)) 
	print "connect success"

	# send_list = ["hello","world","welcome","to","use","python"]
	# for val in send_list:
	# 	print val

	send_list = []
	size = 65
	send = chr(size)
	send_list.append(send)
	send_list.append(' ')
	send_list.append('L')
	send_list.append(' ')
	send_list.append("hello")

	for val in send_list:
		print send
		sock.sendall(val)


if __name__ == "__main__":
	main()