from fastapi import FastAPI, HTTPException, UploadFile
import json
from datetime import date
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import shutil
app = FastAPI()

class Coffee(BaseModel):
    bean_name: str
    description: str
    roasted_on: date

def get_db():
    with open("db.json") as f:
        coffee_db = json.load(f)
    return coffee_db

def save_db(db):
    with open("db.json", "w") as f:
        json.dump(jsonable_encoder(db), f)

@app.get("/coffee/")
def read_coffee():
    return get_db()

@app.post("/coffee/")
def add_coffee(input_coffee: Coffee):
    coffee_db = get_db()
    if coffee_db == {} or len(coffee_db['coffee']) == 0:
        coffee_db['coffee'] = [jsonable_encoder(input_coffee)]
    else:
        coffee_db['coffee'].append(jsonable_encoder(input_coffee))
    save_db(coffee_db)
    return {"status": "Created"}
    
@app.post("/coffee/upload/{bean_name}")
def upload_img(upload_file: UploadFile, bean_name: str):
    with open(f"./{bean_name}.png", "wb") as buff:
        shutil.copyfileobj(upload_file.file, buff)
    return {"status": "Uploaded"}
