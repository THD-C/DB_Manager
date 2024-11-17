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

    def insert(self, session: Session):
        session.add(self)
        session.commit()
        session.refresh(self)

    def update(self, session: Session, values_to_update: Type[T]):
        self.__update_model_fields(values_to_update)
        session.add(self)
        session.commit()
        session.refresh(self)
        
        
    def delete(self, session: Session):
        session.delete(self)
        session.commit()

    def __update_model_fields(self, values_to_update: Type[T]):
        fields = self.__get_model_fields(self.__class__)
        for f in fields:
            value = getattr(values_to_update, f)
            # if value is None, then we want to keep the existing value
            if value and f != "id":
                setattr(self, f, value)

    @staticmethod
    def __get_model_fields(model_class: Type[T]) -> list[str]:
        return list(model_class.__dict__.get("model_fields").keys())

    @staticmethod
    def __get_type(model_class: Type[T], field_name: str) -> type:
        return model_class.__annotations__.get(field_name)
