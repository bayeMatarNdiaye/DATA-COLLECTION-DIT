from fastapi import FastAPI
from libraries.database import Databases
import sqlalchemy
import _mysql_connector

app = FastAPI()


@app.get("/")
async def root():
    data = Databases.recupData()
    return data
