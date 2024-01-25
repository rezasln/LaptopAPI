from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from DataBase.db import get_db, LaptopDB, delete_laptop_by_model 

class Laptop(BaseModel):
    brand: str
    model: str
    price: float
    battery_capacity: int

app = FastAPI()

@app.get("/laptops/", response_model=List[Laptop])
def get_laptops(db: Session = Depends(get_db)):
    return db.query(LaptopDB).all()

@app.post("/laptops/")
def add_laptop(laptop: Laptop, db: Session = Depends(get_db)):
    db_laptop = LaptopDB(**laptop.dict())
    db.add(db_laptop)
    db.commit()
    db.refresh(db_laptop)
    return db_laptop

@app.put("/laptops/{model}")
def update_laptop(model: str, laptop: Laptop, db: Session = Depends(get_db)):
    db_laptop = db.query(LaptopDB).filter(LaptopDB.model == model).first()
    if not db_laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    for key, value in laptop.dict().items():
        setattr(db_laptop, key, value)
    db.commit()
    return db_laptop

@app.delete("/laptops/{model}")
def delete_laptop(model: str, db: Session = Depends(get_db)):
    if not delete_laptop_by_model(db, model):  
        raise HTTPException(status_code=404, detail="Laptop not found")
    return {"message": "Laptop deleted successfully"}

@app.get("/laptops/brand/{brand_name}/count")
def get_laptop_count_by_brand(brand_name: str, db: Session = Depends(get_db)):
    count = db.query(LaptopDB).filter(LaptopDB.brand == brand_name).count()
    return {"brand": brand_name, "count": count}
