import Queue

QUEUE_GAME_INDEX = 1
QUEUE_SEND_INDEX = 2
QUEUE_MAX_SIZE = 1024

class MsgQueue(object):
	"""docstring for MsgQueue"""
	def __init__(self):
		self.queue_dic = []
		self.queue_dic[QUEUE_GAME_INDEX] = Queue.Queue(QUEUE_MAX_SIZE)
		self.queue_dic[QUEUE_SEND_INDEX] = Queue.Queue(QUEUE_MAX_SIZE)

	def get_game_thread_que(self):
		return self.queue_dic[QUEUE_GAME_INDEX]

	def get_send_thread_que(self):
		return self.queue_dic[QUEUE_SEND_INDEX]