# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: objetos.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\robjetos.proto\"y\n\x06Planta\x12\x0c\n\x04\x61gua\x18\x01 \x01(\x05\x12\x10\n\x08\x61gua_min\x18\x02 \x01(\x05\x12\x0f\n\x07luz_min\x18\x03 \x01(\x05\x12\x10\n\x08temp_min\x18\x04 \x01(\x05\x12\x10\n\x08temp_max\x18\x05 \x01(\x05\x12\x0c\n\x04name\x18\x06 \x01(\t\x12\x0c\n\x04vida\x18\x07 \x01(\x05\"$\n\x07Lampada\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0b\n\x03luz\x18\x02 \x01(\x05\"\x16\n\x06Sensor\x12\x0c\n\x04temp\x18\x01 \x01(\x05\"W\n\x07Objetos\x12\x18\n\x07plantas\x18\x01 \x03(\x0b\x32\x07.Planta\x12\x19\n\x07lampada\x18\x02 \x01(\x0b\x32\x08.Lampada\x12\x17\n\x06sensor\x18\x03 \x01(\x0b\x32\x07.Sensor\"Y\n\x07Request\x12\x17\n\x06objeto\x18\x01 \x01(\x0e\x32\x07.Objeto\x12\x11\n\tmodificar\x18\x02 \x01(\x08\x12\r\n\x05value\x18\x03 \x01(\x05\x12\x13\n\x04tipo\x18\x04 \x01(\x0e\x32\x05.Tipo\"@\n\x08Response\x12\x0b\n\x03msg\x18\x01 \x01(\t\x12\x0c\n\x04\x65rro\x18\x02 \x01(\x08\x12\x19\n\x07objetos\x18\x03 \x01(\x0b\x32\x08.Objetos*2\n\x04Tipo\x12\x08\n\x04NADA\x10\x00\x12\n\n\x06OBJETO\x10\x03\x12\t\n\x05REGAR\x10\x01\x12\t\n\x05\x42USCA\x10\x02*F\n\x06Objeto\x12\x08\n\x04NOTH\x10\x00\x12\n\n\x06PLANTA\x10\x04\x12\n\n\x06SENSOR\x10\x01\x12\r\n\tAQUECEDOR\x10\x02\x12\x0b\n\x07LAMPADA\x10\x03\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'objetos_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TIPO._serialized_start=448
  _TIPO._serialized_end=498
  _OBJETO._serialized_start=500
  _OBJETO._serialized_end=570
  _PLANTA._serialized_start=17
  _PLANTA._serialized_end=138
  _LAMPADA._serialized_start=140
  _LAMPADA._serialized_end=176
  _SENSOR._serialized_start=178
  _SENSOR._serialized_end=200
  _OBJETOS._serialized_start=202
  _OBJETOS._serialized_end=289
  _REQUEST._serialized_start=291
  _REQUEST._serialized_end=380
  _RESPONSE._serialized_start=382
  _RESPONSE._serialized_end=446
# @@protoc_insertion_point(module_scope)
