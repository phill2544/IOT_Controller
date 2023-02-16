from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

# class Item(BaseModel):
#     name: str | None = None
#     price: float

app = FastAPI()

def get_conn():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="iot"
    )
    return conn

@app.on_event("startup")
async def startup():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.close()
    conn.close()

@app.on_event("shutdown")
async def shutdown():
    conn = get_conn()
    conn.close()

@app.get("/")
async def root():
    print('come from Django')
    return {"message": "Hello World"}


@app.get("/hello")
async def test(temp,humid,adc):
    print(temp)
    print(humid)
    print(adc)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""update iot set temp = {}, humid = {}, adc = {} where id = 1""".format(temp,humid,adc))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "{},{}".format(temp,humid)}


@app.get("/change_state_fan")
async def haha():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""update iot set status_fan = not status_fan where id = 1""")
    conn.commit()
    cursor.execute("SELECT status_fan FROM iot where id = 1")
    a = cursor.fetchall()
    print(a[0][0])
    cursor.close()
    conn.close()
    return a

@app.get("/change_state_lamp")
async def haha():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""update iot set status_lamp = not status_lamp where id = 1""")
    conn.commit()
    cursor.execute("SELECT status_lamp FROM iot where id = 1")
    a = cursor.fetchall()
    print(a[0][0])
    cursor.close()
    conn.close()
    return a

@app.get("/change_state_water")
async def haha():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""update iot set status_water = not status_water where id = 1""")
    conn.commit()
    cursor.execute("SELECT status_water FROM iot where id = 1")
    a = cursor.fetchall()
    print(a[0][0])
    cursor.close()
    conn.close()
    return a

@app.get("/get_status")
async def get_status():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT status_fan,status_lamp,status_water FROM iot where id = 1")
    a = cursor.fetchall()
    print(a[0])
    cursor.close()
    conn.close()
    return a