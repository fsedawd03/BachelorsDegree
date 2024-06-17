from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    email: str
    test: int


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/hello")
async def say_hello(item: Item):
    return {"message": "hello World"}
