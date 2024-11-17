
from typing import Type, TypeVar
from google.protobuf.descriptor import FieldDescriptor

T = TypeVar("T")

TYPE_MAP = {
    FieldDescriptor.TYPE_DOUBLE: float,
    FieldDescriptor.TYPE_FLOAT: float,
    FieldDescriptor.TYPE_INT64: int,
    FieldDescriptor.TYPE_UINT64: int,
    FieldDescriptor.TYPE_INT32: int,
    FieldDescriptor.TYPE_FIXED64: int,
    FieldDescriptor.TYPE_FIXED32: int,
    FieldDescriptor.TYPE_BOOL: bool,
    FieldDescriptor.TYPE_STRING: str,
    FieldDescriptor.TYPE_GROUP: None,  # Deprecated, no direct mapping
    FieldDescriptor.TYPE_MESSAGE: lambda: None,  # Special case, needs the message class
    FieldDescriptor.TYPE_BYTES: bytes,
    FieldDescriptor.TYPE_UINT32: int,
    FieldDescriptor.TYPE_ENUM: int,  # Typically enums map to integers
    FieldDescriptor.TYPE_SFIXED32: int,
    FieldDescriptor.TYPE_SFIXED64: int,
    FieldDescriptor.TYPE_SINT32: int,
    FieldDescriptor.TYPE_SINT64: int,
}

def create_grpc_model(model_class: Type[T], data_class) -> T:
    grpc_fields: dict[str, type] = __get_grpc_model_fields_and_types(model_class)
    data = {}
    for f_name, f_type in grpc_fields.items():
        if not hasattr(data_class, f_name):
            continue
        if getattr(data_class, f_name):
            data[f_name] = f_type(
                getattr(data_class, f_name)
            )
        else:
            data[f_name] = None
    
    return model_class(**data)

def __get_grpc_model_fields_and_types(model_class: Type[T]) -> dict[str, type]:
    fields_and_types = {}
    # create a map of fields and their types
    for field_name, field_descriptor in model_class.DESCRIPTOR.fields_by_name.items():
        fields_and_types[field_name] = TYPE_MAP.get(field_descriptor.type)
    return fields_and_types