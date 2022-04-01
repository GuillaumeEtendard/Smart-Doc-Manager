import os
from dotenv import load_dotenv
from fastapi.applications import FastAPI
from fastapi.datastructures import UploadFile
from fastapi.exceptions import HTTPException
from fastapi.param_functions import File, Body
from s3_events.s3_utils import S3_SERVICE
from dotenv import load_dotenv

from typing import List
from fastapi.middleware.cors import CORSMiddleware
from utils import *

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine
from utils import *
import json

load_dotenv()
project_name = "FastAPI"

# TODO(developer): Uncomment these variables before running the sample.
project_id = "smart-doc-manager"
location = "eu"  # Format is 'us' or 'eu'
processor_id = "e03ac7695ea2d081"  # Create processor in Cloud Console
file_path = "./invoice-template-us-band-blue-750px.png"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION")
S3_Bucket = os.environ.get("S3_Bucket")
S3_Key = os.environ.get("S3_Key")

app = FastAPI(title="FastAPI")

# Object of S3_SERVICE Class
s3_client = S3_SERVICE(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(type: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, type, skip=skip, limit=limit)
    return items


@app.get("/items/{id}", response_model=schemas.Item)
def read_item(id: int, db: Session = Depends(get_db)):
    items = crud.get_item(db, id)
    return items


@app.get("/ping", status_code=200, description="***** Liveliness Check *****")
async def ping():
    return {"ping": "pong"}


import calendar
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR')


@app.get("/dashboard", status_code=200, description="***** Liveliness Check *****")
async def dashboard(db: Session = Depends(get_db)):
    total_cv = crud.get_total(db=db, type='CV')
    total_invoice = crud.get_total(db=db, type='invoice')
    items = crud.get_all_items(db)
    months_names = list(calendar.month_abbr)
    months_values = [0] * 12
    for _ in items:
        months_values[items[0].date.month] += 1

    return {"totalCV": total_cv, "totalInvoice": total_invoice, "months_values": months_values,
            "months_names": months_names}


@app.post("/upload", status_code=200, description="***** Upload png asset to S3 *****")
async def upload(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    uploaded = []
    for file in files:
        print(file.filename)
        content, file_type = await processFile(file)
        if content and file_type:
            item = {'name': file.filename, 'data': json.dumps(content), 'type': file_type}
            crud.create_user_item_dict(db=db, item=item, user_id=1)
            uploaded.append(f'{file.filename} : {file_type}')

    return {"status": "success", "uploaded": ', '.join(uploaded)}
