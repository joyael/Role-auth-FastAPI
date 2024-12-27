from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role_id: int  # Role ID to assign during registration

class User(BaseModel):
    id: int
    username: str
    role_id: int

    class Config:
        from_attributes = True
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class Role(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        orm_mode = True