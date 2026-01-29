from fastapi import FastAPI,Depends,Body, HTTPException,Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class User(BaseModel):
    username:str
    age:int

# @app.post("/register")
# def register(user:User):
#     return {
#         "username":user.username,
#         "age":user.age
#     }



# @app.post("/register_body")
# def register_body(user:dict=Body(...)):
#     return user


# @app.post("/register_json")
# async def register_json(user:Request):
#     body=await user.json()
#     return body

# def return_username(user:User):
#     return user


# def sendback_username(user=Depends(return_username)):
#     return {
#         "user":user.username,
#         "age":user.age,
#         "gender":"random"
#     }
@app.middleware("http")
async def my_middleware(request:Request,call_next):
    print("请求进来了")
    response=await call_next(request)
    print("请求出去了")

    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/sms")
def sms(body:dict=Body(...)):
    access=body.get("access")
    print(access)
    if access==0:
    # access=body.
        return {"sms":"123456"}
    if access==1:
        raise HTTPException(status_code=400,detail="access can't be 1")

# @app.post("/get_current_user")
# def get_current_user(username=Depends(sendback_username)):
#     return {"username":username}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012)