from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import aiomysql
import asyncio

app = FastAPI()


async def connect_to_database():
    connection = await aiomysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        db='test',
        charset='utf8mb4',
        loop=asyncio.get_event_loop()
    )
    return connection


class User(BaseModel):
    name : str



@app.get("/{item}/{name}")
async def root(item,name):
    return {"message": [item,name]}

    
@app.get("/")
async def read_root(name : str):
    connection = await connect_to_database()
    cursor = await connection.cursor()
    print(cursor)
    await cursor.execute("INSERT INTO begin(name) VALUES ('{}');".format(name))
    await connection.commit()
    await cursor.execute("SELECT * FROM begin")
    result = await cursor.fetchall()
    print(result)
    return result

@app.post("/item")
async def test(User:User):
    return User


@app.post("/user")
async def create_user(name: User):
    async with connect_to_database().get() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"INSERT INTO begin (name) VALUES ('{name}')")
    return {"message": "User created"}

