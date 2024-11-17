from typing import Type, TypeVar
from sqlalchemy.orm import Session


T = TypeVar("T")


class BaseDBOpsModel:

    @staticmethod
    def create_model(model_class: Type[T], proto_request) -> T:
        field_names = BaseDBOpsModel.__get_model_fields(model_class)
        data = {}
        for field in field_names:
            if not hasattr(proto_request, field):
                continue
            if getattr(proto_request, field):
                data[field] = BaseDBOpsModel.__get_type(model_class, field)(
                    getattr(proto_request, field)
                )
            else:
                data[field] = None
        return model_class(**data)

    @staticmethod
    def __get_model_fields(model_class: Type[T]) -> list[str]:
        return list(model_class.__dict__.get("model_fields").keys())

    @staticmethod
    def __get_type(model_class: Type[T], field_name: str) -> type:
        return model_class.__annotations__.get(field_name)

    def insert(self, session: Session):
        session.add(self)
        session.commit()
        session.refresh(self)
