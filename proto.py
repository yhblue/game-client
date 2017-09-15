'''
about protobuf pack and unpack
'''


class ProtoType(object):
	"""docstring for ProtoType"""
	def __init__(self, arg):
		self.LOG_REQ = 'L'
		self.LOG_RSP = 'l'
		self.HERO_MSG_REQ = 'H' 
		self.HERO_MSG_RSP = 'h'
		self.LEAVE_REQ = 'V'
		self.LEAVE_RSP = 'v'
		self.START_REQ = 'S'
		self.START_RSP = 's'
		self.MOVE_REQ = 'M'
		self.MOVE_RSP = 'm'
		self.ENEMY_MSG = 'e'
		self.NEW_ENEMY = 'n'  
		self.LOGIN_END = 'i'	


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
		self.proto_type = ProtoType()
		pass

	def msg_data_deseria(self,data_list):
		assert(type(data_list) == list)

		rsp_list = []
		rsp = 0
		msg_type = data_list[PROTO_SIZE_INDEX]
		msg_size = data_list[PROTO_TYPE_INDEX] 
		content = data_list[PROTO_CONTENT_INDX]

		if msg_type == self.proto_type.LOG_RSP:
			rsp = message_pb2.login_rsp()
			rsp.ParseFromString(content)

		elif msg_type == self.proto_type.ENEMY_MSG:
			rsp = message_pb2.enemy_msg()
			rsp.ParseFromString(content)

		elif msg_type == self.proto_type.NEW_ENEMY:
			rsp = message_pb2.new_enemy()
			rsp.ParseFromString(content)

		elif msg_type == self.proto_type.START_RSP:
			rsp = message_pb2.start_rsp()
			rsp.ParseFromString(content)

		elif msg_type == self.proto_type.LOGIN_END:
			rsp = message_pb2.login_end()
			rsp.ParseFromString(content)

		elif msg_type == self.proto_type.MOVE_RSP:
			rsp = message_pb2.move_rsp()
			rsp.ParseFromString(content)

		elif msg_type == self.proto_type.LEAVE_RSP:
			rsp = message_pb2.leave_rsp()
			rsp.ParseFromString(content)			

		rsp_list.append(msg_type)
		rsp_list.append(msg_size)
		rsp_list.append(rsp)

		return rsp_list