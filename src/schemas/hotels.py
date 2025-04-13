from pydantic import BaseModel, Field, field_validator, model_validator
from src.exceptions.exceptions import TooShortLocationHTTPException, TooShortTitleHTTPException, EmptyDataHTTPException

class HotelAdd(BaseModel):
    title: str
    location: str

    @field_validator("title")
    @classmethod
    def title_is_not_empty(cls, value) :
        if len(value.strip()) <= 1 :
            raise TooShortTitleHTTPException
        return value
    
    @field_validator("location")
    @classmethod
    def location_is_not_empty(cls, value) :
        if len(value.strip()) <= 1 :
            raise TooShortLocationHTTPException
        return value

class Hotel(HotelAdd):
    id: int

class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)

    @model_validator(mode="after")
    def is_not_empty(self) :
        if not (self.title or self.location) : 
            raise EmptyDataHTTPException

class HotelPUT(BaseModel):
    title: str
    location: str
