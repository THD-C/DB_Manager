from typing import Type, TypeVar
from sqlalchemy.orm import Session
import datetime

from src.DB.Tables import TABLE_NAME_USER, TABLE_NAME_USER_DETAIL, PK_PAYMENT

T = TypeVar("T")

NULL_DATE = datetime.datetime(1970, 1, 1, 0, 0)

TABLES_WITHOUT_UPPERCASE = [
    TABLE_NAME_USER,
    TABLE_NAME_USER_DETAIL,
]


class BaseDBOpsModel:

    @staticmethod
    def create_model(model_class: Type[T], proto_request) -> T:
        field_names = BaseDBOpsModel.__get_model_fields(model_class)
        data = {}
        for field in field_names:
            if not hasattr(proto_request, field):
                continue

            if getattr(proto_request, field) or getattr(proto_request, field) == 0:
                data_type = BaseDBOpsModel.__get_type(model_class, field)

                if data_type == datetime.datetime:
                    data[field] = getattr(proto_request, field).ToDatetime()
                    if data[field] == NULL_DATE:
                        data[field] = None

                elif (
                    data_type is str
                    and field != PK_PAYMENT
                    and model_class.__tablename__ not in TABLES_WITHOUT_UPPERCASE
                ):
                    data[field] = str(getattr(proto_request, field)).upper()
                else:
                    data[field] = data_type(getattr(proto_request, field))
            else:
                data[field] = None
        return model_class(**data)

    def check_all_attributes_are_none(self):
        fields: list[str] = self.__get_model_fields(self.__class__)
        field_values = [getattr(self, f) for f in fields]
        return all(attribute is None for attribute in field_values)

    def insert(self, session: Session, skip_commit=False):
        session.add(self)
        if not skip_commit:
            session.commit()
        session.refresh(self)

    def update(self, session: Session, values_to_update: Type[T], skip_commit=False):
        self.__update_model_fields(values_to_update)
        session.add(self)
        if not skip_commit:
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
