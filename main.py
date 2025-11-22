from fastapi import FastAPI, HTTPException, Depends
import serializers
import models
from db import get_db, create_table
from contextlib import asynccontextmanager
from router import router

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield

app.include_router(router)
