import json
import os

from pydantic import BaseModel
from typing import List


class Data(BaseModel):
    id: str
    predict: float


class Message(BaseModel):
    message: str


class Response(BaseModel):
    data: List[Data]


class Status(BaseModel):
    status: str


class Config(BaseModel):
    api_url: str
    file_path: str
    best_setup: dict
