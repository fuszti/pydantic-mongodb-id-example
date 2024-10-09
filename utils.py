from pydantic import BaseModel
from bson import ObjectId

class DbDumper(BaseModel):
    @staticmethod
    def from_db(doc: dict) -> dict:
        model_dump = doc.copy()
        for key, value in model_dump.items():
            if isinstance(value, ObjectId):
                model_dump[key] = str(value)
        if "_id" in model_dump:
            model_dump["id"] = str(model_dump["_id"])
            del model_dump["_id"]
        return model_dump

    @staticmethod
    def to_db(model: BaseModel, include_id: bool = False) -> dict:
        dump = model.model_dump(context="objectid")
        if "id" in dump:
            if include_id:
                dump["_id"] = dump["id"]
            del dump["id"]
        return dump
