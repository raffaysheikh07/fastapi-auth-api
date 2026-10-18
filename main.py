from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from auth import verify_login, register_user

class data(BaseModel):
    choice: int
    identifier: str
    password: str

class registerdata(BaseModel):
    username: str
    email: str
    password: str

app = FastAPI()
@app.post("/login")
def login(request_body:data):
    
    result = verify_login(
        request_body.choice,
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
