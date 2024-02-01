from pydantic import BaseModel, EmailStr

from datetime import datetime


class User(BaseModel):

    first_name: str
    last_name: str
    email: EmailStr
    


class UserIn(User):

    password: str


class UserOut(User):

    member_since: datetime
    
    class Config:
        from_attributes = True