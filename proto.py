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
#	PROTO_SIZE_INDEX = 0
	PROTO_TYPE_INDEX = 0
	PROTO_CONTENT_INDEX = 1
	DATA_LEN_SIZE = 1
	
	def __init__(self):
		pass

class Serialize(object):
	def __init__(self):
		pass

	def msg_data_pack(self,seria_data,msg_type):
		list_ret = []
		size = chr(seria_data.ByteSize() + len(msg_type))  #get length
		data = seria_data.SerializeToString()
		send_data = size + msg_type + data
		# list_ret.append(size)
		# list_ret.append(msg_type)
		# list_ret.append(seria_data.SerializeToString())
		return send_data

	def hero_msg_seria(self,uid,pos_x,pos_y,msg_type):
		seria_data = message_pb2.hero_msg()
		seria_data.uid = uid
		seria_data.point_x = pos_x
		seria_data.point_y = pos_y
		return self.msg_data_pack(seria_data,msg_type)		

	def login_request_seria(self,name,msg_type):
		seria_data = message_pb2.login_req()
		seria_data.name = name
		return self.msg_data_pack(seria_data,msg_type)

	def start_request_seria(self,start,msg_type):
		seria_data = message_pb2.start_req()
		seria_data.start = start
		return self.msg_data_pack(seria_data,msg_type)			

	def move_request_seria(self,operation,msg_type):
		seria_data = message_pb2.move_req()
		seria_data.move = operation
		return self.msg_data_pack(seria_data,msg_type)

	def leave_request_seria(self,uid,msg_type):
		seria_data = message_pb2.leave_req()
		seria_data.uid = uid
		return self.msg_data_pack(seria_data,msg_type)		

class Deserialize(object):
	def __init__(self):
		pass

	def msg_data_deseria(self,data_list):
		assert(type(data_list) == dict)

		rsp_list = [] 
		rsp = 0
		#msg_size = data_list[ProtoFormat.PROTO_SIZE_INDEX] 
		msg_type = data_list[ProtoFormat.PROTO_TYPE_INDEX]
		content = data_list[ProtoFormat.PROTO_CONTENT_INDEX]

		if msg_type == ProtoType.LOG_RSP:
			print "---LOG_RSP---"
			rsp = message_pb2.login_rsp()
			rsp.ParseFromString(content)			
			print ("rsp.success = %d"%rsp.success)
			print ("rsp.point_x = %d"%rsp.point_x)
			print ("rsp.point_y = %d"%rsp.point_y)
			print ("rsp.enemy_num = %d"%rsp.enemy_num)
			print ("rsp.uid = %d"%rsp.uid)


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
			print "MOVE RSP"

		elif msg_type == ProtoType.LEAVE_RSP:
			rsp = message_pb2.leave_rsp()
			rsp.ParseFromString(content)			

		#rsp_list.append(msg_size)
		rsp_list.append(msg_type)
		rsp_list.append(rsp)

		return rsp_list