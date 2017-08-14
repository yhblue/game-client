# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='message.proto',
  package='',
  serialized_pb='\n\rmessage.proto\"9\n\x08Hero_msg\x12\x0b\n\x03uid\x18\x01 \x02(\x05\x12\x0f\n\x07point_x\x18\x02 \x02(\x05\x12\x0f\n\x07point_y\x18\x03 \x02(\x05\"\x0c\n\nHeart_beat\"\x19\n\tLogin_req\x12\x0c\n\x04name\x18\x01 \x02(\t\"^\n\tLogin_rsp\x12\x0f\n\x07success\x18\x01 \x02(\x08\x12\x0f\n\x07point_x\x18\x02 \x02(\x05\x12\x0f\n\x07point_y\x18\x03 \x02(\x05\x12\x11\n\tenemy_num\x18\x04 \x02(\x05\x12\x0b\n\x03uid\x18\x05 \x02(\x05\"\r\n\x0b\x43onnect_req\"\x1e\n\x0b\x43onnect_rsp\x12\x0f\n\x07success\x18\x01 \x02(\x08\";\n\tEnemy_msg\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0f\n\x07point_x\x18\x02 \x02(\x05\x12\x0f\n\x07point_y\x18\x03 \x02(\x05')




_HERO_MSG = _descriptor.Descriptor(
  name='Hero_msg',
  full_name='Hero_msg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='Hero_msg.uid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='point_x', full_name='Hero_msg.point_x', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='point_y', full_name='Hero_msg.point_y', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=17,
  serialized_end=74,
)


_HEART_BEAT = _descriptor.Descriptor(
  name='Heart_beat',
  full_name='Heart_beat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=76,
  serialized_end=88,
)


_LOGIN_REQ = _descriptor.Descriptor(
  name='Login_req',
  full_name='Login_req',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Login_req.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=90,
  serialized_end=115,
)


_LOGIN_RSP = _descriptor.Descriptor(
  name='Login_rsp',
  full_name='Login_rsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='Login_rsp.success', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='point_x', full_name='Login_rsp.point_x', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='point_y', full_name='Login_rsp.point_y', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='enemy_num', full_name='Login_rsp.enemy_num', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uid', full_name='Login_rsp.uid', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=117,
  serialized_end=211,
)


_CONNECT_REQ = _descriptor.Descriptor(
  name='Connect_req',
  full_name='Connect_req',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=213,
  serialized_end=226,
)


_CONNECT_RSP = _descriptor.Descriptor(
  name='Connect_rsp',
  full_name='Connect_rsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='Connect_rsp.success', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=228,
  serialized_end=258,
)


_ENEMY_MSG = _descriptor.Descriptor(
  name='Enemy_msg',
  full_name='Enemy_msg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Enemy_msg.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='point_x', full_name='Enemy_msg.point_x', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='point_y', full_name='Enemy_msg.point_y', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=260,
  serialized_end=319,
)

DESCRIPTOR.message_types_by_name['Hero_msg'] = _HERO_MSG
DESCRIPTOR.message_types_by_name['Heart_beat'] = _HEART_BEAT
DESCRIPTOR.message_types_by_name['Login_req'] = _LOGIN_REQ
DESCRIPTOR.message_types_by_name['Login_rsp'] = _LOGIN_RSP
DESCRIPTOR.message_types_by_name['Connect_req'] = _CONNECT_REQ
DESCRIPTOR.message_types_by_name['Connect_rsp'] = _CONNECT_RSP
DESCRIPTOR.message_types_by_name['Enemy_msg'] = _ENEMY_MSG

class Hero_msg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _HERO_MSG

  # @@protoc_insertion_point(class_scope:Hero_msg)

class Heart_beat(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _HEART_BEAT

  # @@protoc_insertion_point(class_scope:Heart_beat)

class Login_req(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LOGIN_REQ

  # @@protoc_insertion_point(class_scope:Login_req)

class Login_rsp(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LOGIN_RSP

  # @@protoc_insertion_point(class_scope:Login_rsp)

class Connect_req(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CONNECT_REQ

  # @@protoc_insertion_point(class_scope:Connect_req)

class Connect_rsp(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CONNECT_RSP

  # @@protoc_insertion_point(class_scope:Connect_rsp)

class Enemy_msg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ENEMY_MSG

  # @@protoc_insertion_point(class_scope:Enemy_msg)


# @@protoc_insertion_point(module_scope)
