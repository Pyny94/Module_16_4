from http.client import HTTPException
from mailbox import Message

from fastapi import FastAPI,Path
from typing import Annotated

from pydantic.v1 import BaseModel

app = FastAPI()

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get("/users")
async def main():
    return users

@app.post("/user/{username}/{age}")
async def create_user(username: str, age: int):
    last_id = users[-1].id if users else 0
    new_id = last_id + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            users[i].username = username
            users[i].age = age
            return users[i]
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(i)
            return deleted_user
    raise HTTPException(status_code=404, detail="User was not found")