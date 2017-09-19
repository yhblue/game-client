'''
about protobuf pack and unpack
'''
import message_pb2

class ProtoType(object):
	LOG_REQ = 'L'
	LOG_RSP = 'l'
	HERO_MSG_REQ = 'H' 
	HERO_MSG_RSP = 'h'
	LEAVE_REQ = 'V'
	LEAVE_RSP = 'v'
	START_REQ = 'S'
	START_RSP = 's'
	MOVE_REQ = 'M'
	MOVE_RSP = 'm'
	ENEMY_MSG = 'e'
	NEW_ENEMY = 'n'  
	LOGIN_END = 'i'		
	ENEMY_LEAVE = 'y'

	def __init__(self):
		pass

class ProtoFormat(object):
	PROTO_SIZE_INDEX = 0
	PROTO_TYPE_INDEX = 1
	PROTO_CONTENT_INDEX = 2

	def __init__(self):
		pass

class Serialize(object):
	def __init__(self):
		pass

	def hero_msg_seria(self,hero,type):
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

	def login_require_seria(self,hero,type):
		seria_data = message_pb2.login_req()
		seria_data.name = hero.get_name()

		list_ret = []
		size = chr(seria_data.ByteSize()+len(type))
		list_ret.append(size)
		list_ret.append(type)
		list_ret.append(seria_data.SerializeToString()) 
		return list_ret

	def start_request_seria(self,start,type):
		seria_data = message_pb2.start_req()
		seria_data.start = start

		list_ret = []
		size = chr(seria_data.ByteSize()+len(type))
		list_ret.append(size)
		list_ret.append(type)
		list_ret.append(seria_data.SerializeToString()) 
		return list_ret				

	def move_request_seria(self,operation,type):
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
		pass
		#self.proto_type = ProtoType()
		#self.msg_format = ProtoFormat()

	def msg_data_deseria(self,data_list):
		assert(type(data_list) == dict)

		rsp_list = [] 
		rsp = 0
		msg_type = data_list[ProtoFormat.PROTO_SIZE_INDEX]
		msg_size = data_list[ProtoFormat.PROTO_TYPE_INDEX] 
		content = data_list[ProtoFormat.PROTO_CONTENT_INDEX]

		if msg_type == ProtoType.LOG_RSP:
			rsp = message_pb2.login_rsp()
			rsp.ParseFromString(content)

		elif msg_type == ProtoType.ENEMY_MSG:
			rsp = message_pb2.enemy_msg()
			rsp.ParseFromString(content)

		elif msg_type == ProtoType.NEW_ENEMY:
			rsp = message_pb2.new_enemy()
			rsp.ParseFromString(content)

		elif msg_type == ProtoType.START_RSP:
			rsp = message_pb2.start_rsp()
			rsp.ParseFromString(content)

		elif msg_type == ProtoType.LOGIN_END:
			rsp = message_pb2.login_end()
			rsp.ParseFromString(content)

		elif msg_type == ProtoType.MOVE_RSP:
			rsp = message_pb2.move_rsp()
			rsp.ParseFromString(content)

		elif msg_type == ProtoType.LEAVE_RSP:
			rsp = message_pb2.leave_rsp()
			rsp.ParseFromString(content)			

		rsp_list.append(msg_size)
		rsp_list.append(msg_type)
		rsp_list.append(rsp)

		return rsp_list