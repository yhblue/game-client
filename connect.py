'''
about socket
'''
import socket
ADDRESS, PORT = "localhost", 8000

class Socket(object):
	"""docstring for Socket"""
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		
	def socket_connect(self):
		self.sock.connect((ADDRESS,PORT));

	def get_socket(self):
		return self.sock
	
	def socket_close(slef):
		self.sock.close()

