from datetime import datetime
from enum import Enum
from pydantic import BaseModel, field_validator, PlainValidator, WrapSerializer, Field, EmailStr
from bson import ObjectId
from typing import Annotated
from utils import DbDumper

RequiredId = Annotated[
    str,
    PlainValidator(lambda value: str(value)),
    WrapSerializer(lambda value, handler, info: ObjectId(value) if info.context == "objectid" and value else value),
    Field(min_length=24, max_length=24)
]

OptionalId = Annotated[
    RequiredId | None,
    Field(default=None)
]

class User(DbDumper):
    id: OptionalId
    username: str
    email: EmailStr

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Post(DbDumper):
    id: OptionalId
    title: str
    content: str
    author_id: RequiredId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
