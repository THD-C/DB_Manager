def get_class_fields(cls):
    return [ name for name in
        cls.__dict__.get("model_fields").keys() if not "ID" in name
        ]