from fastapi import FastAPI, HTTPException, Depends
import serializers
import models
from db import get_db, create_table
from contextlib import asynccontextmanager
from router import router



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)
