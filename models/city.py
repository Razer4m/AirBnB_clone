#!/usr/bin/python3
"""
It initiate one class, `City(),
"""


from models.base_model import BaseModel


class City(BaseModel):
    """City class that inherits from BaseModel"""
    state_id = ""
    name = ""
