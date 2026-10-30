from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator, EmailStr
from auth import verify_login, register_user
from database import init_db

class data(BaseModel):
    identifier: str
    password: str = Field(max_length=64)
    @field_validator("identifier")
    @classmethod
    def cleanIdentifier(cls, value: str) -> str:
        return value.strip().lower()

class registerdata(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)
    @field_validator("username")
    @classmethod
    def clean_username(cls, value: str) -> str:
        return value.lower()

    @field_validator("email")
    @classmethod
    def clean_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value:
            raise ValueError("Invalid email")
        return value

app = FastAPI()
init_db()
@app.post("/login")
def login(request_body:data):
    
    result = verify_login(
        request_body.identifier,
        request_body.password
    )
    
    if result:
        return {"message": "Welcome back!"}
        
    raise HTTPException(status_code=401, detail="Invalid details")

@app.post("/register", status_code = 201)
def register(request_body: registerdata):

    created = register_user(
        request_body.username,
        request_body.email,
        request_body.password,
    )

    if not created:
        raise HTTPException(status_code=409, detail = "User Already Exist!!. Please Login")

    return {"message": "Account created!!"}
