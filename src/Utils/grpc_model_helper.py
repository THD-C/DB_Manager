from typing import Type, TypeVar
from google.protobuf.descriptor import FieldDescriptor

gRPC = TypeVar("gRPC")

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


def create_grpc_list_model(
    model_class: Type[gRPC], list_model_class: list[T], data_class: list[any]
) -> gRPC:
    grpc_fields: dict[str, type] = __get_grpc_model_fields_and_types(model_class)

    result = model_class()
    for f_name, f_type in grpc_fields.items():
        if f_type == list_model_class:
            r_list = []
            for data in data_class:
                r_list.append(create_grpc_model(f_type, data))
            getattr(result, f_name).extend(r_list)

    return result


def create_grpc_model(model_class: Type[gRPC], data_class) -> gRPC:

    if isinstance(data_class, dict):
        data = __create_grpc_based_on_dict(model_class, data_class)
    elif isinstance(data_class, type):
        data = __create_grpc_based_on_class(model_class, data_class)
    else:
        data = {}
    return model_class(**data)


def __get_grpc_model_fields_and_types(model_class: Type[gRPC]) -> dict[str, type]:
    fields_and_types = {}
    # create a map of fields and their types
    for field_name, field_descriptor in model_class.DESCRIPTOR.fields_by_name.items():
        if field_descriptor.type == FieldDescriptor.TYPE_MESSAGE:
            fields_and_types[field_name] = field_descriptor.message_type._concrete_class
        else:
            fields_and_types[field_name] = TYPE_MAP.get(field_descriptor.type)
    return fields_and_types


def __create_grpc_based_on_class(model_class: Type[gRPC], data_class) -> dict:
    grpc_fields: dict[str, type] = __get_grpc_model_fields_and_types(model_class)
    data = {}
    for f_name, f_type in grpc_fields.items():
        if not hasattr(data_class, f_name):
            continue
        if getattr(data_class, f_name) or getattr(data_class, f_name) == 0:
            data[f_name] = f_type(getattr(data_class, f_name))
        else:
            data[f_name] = None
    return data


def __create_grpc_based_on_dict(model_class: Type[gRPC], data_dict: dict) -> dict:
    grpc_fields: dict[str, type] = __get_grpc_model_fields_and_types(model_class)
    data = {}
    for f_name, f_type in grpc_fields.items():
        if not data_dict.get(f_name, None):
            continue
        if data_dict.get(f_name) or data_dict.get(f_name) == 0:
            data[f_name] = f_type(data_dict.get(f_name))
        else:
            data[f_name] = None
    return data
