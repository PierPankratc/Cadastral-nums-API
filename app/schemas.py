from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class Base(BaseModel):
    pass

class AddCadastralNumber(Base):
    cadastral_number: str = Field(max_length=20)
    latitude: float 
    longitude: float 

    model_config = ConfigDict(extra='forbid')

class ResponseCadastralNumber(Base):

    cadastral_number: str
    latitude: str
    longitude: str
    created_at: datetime
    server_response: bool

