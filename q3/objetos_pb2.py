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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\robjetos.proto\"]\n\x06Planta\x12\x0c\n\x04\x61gua\x18\x01 \x01(\x05\x12\x10\n\x08\x61gua_min\x18\x02 \x01(\x05\x12\x0f\n\x07luz_min\x18\x03 \x01(\x05\x12\x10\n\x08temp_min\x18\x04 \x01(\x05\x12\x10\n\x08temp_max\x18\x05 \x01(\x05\"$\n\x07Lampada\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0b\n\x03luz\x18\x02 \x01(\x05\"\x15\n\x06Sensor\x12\x0b\n\x03ler\x18\x01 \x01(\x08\"\x19\n\tAquecedor\x12\x0c\n\x04temp\x18\x01 \x01(\x05\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'objetos_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PLANTA._serialized_start=17
  _PLANTA._serialized_end=110
  _LAMPADA._serialized_start=112
  _LAMPADA._serialized_end=148
  _SENSOR._serialized_start=150
  _SENSOR._serialized_end=171
  _AQUECEDOR._serialized_start=173
  _AQUECEDOR._serialized_end=198
# @@protoc_insertion_point(module_scope)
