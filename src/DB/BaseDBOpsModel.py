from typing import Type, TypeVar
from sqlalchemy.orm import Session
import src.Utils as Utils


T = TypeVar('T')

class BaseDBOpsModel:
    
    @staticmethod
    def create_model(model_class: Type[T], proto_request) -> T:
        field_names = Utils.get_class_fields(model_class)
        data = {}
        for field in field_names:
            if hasattr(proto_request, field):
                data[field] = getattr(proto_request, field)
        return model_class(**data)
    
    def insert(self, session: Session):
        session.add(self)
        session.commit()
        session.refresh(self)