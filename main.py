from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models as models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Datas(BaseModel):
    rover_number: str = Field(min_length=1)
    rover_name: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=100)
    status: str = Field(min_length=1)
    fuel_lev: str = Field(min_length=1)
    feed_lev: str = Field(min_length=1)
    input_comm: str = Field(min_length=1)



BOOKS = []


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return {"message":"Hello River"}

#    return db.query(models.Control).all()


@app.post("/")
def create_book(data: Datas, db: Session = Depends(get_db)):

    rover_model = models.Control()
    rover_model.rover_number = data.rover_number
    rover_model.rover_name = data.rover_name
    rover_model.location = data.location
    rover_model.status = data.status
    rover_model.fuel_lev = data.fuel_lev
    rover_model.feed_lev = data.feed_lev
    rover_model.input_comm = data.input_comm

    db.add(rover_model)
    db.commit()

    return data


@app.put("/{book_id}")
def update_book(rover_id: int, data: Datas, db: Session = Depends(get_db)):

    rover_model = db.query(models.Control).filter(models.Control.id == rover_id).first()

    if rover_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {rover_id} : Does not exist"
        )

    rover_model.rover_number = data.rover_number
    rover_model.rover_name = data.rover_name
    rover_model.location = data.location
    rover_model.status = data.status
    rover_model.fuel_lev = data.fuel_lev
    rover_model.feed_lev = data.feed_lev
    rover_model.input_comm = data.input_comm

    db.add(rover_model)
    db.commit()

    return data


@app.delete("/{book_id}")
def delete_book(rover_id: int, db: Session = Depends(get_db)):

    rover_model = db.query(models.Control).filter(models.Control.id == rover_id).first()

    if rover_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {rover_id} : Does not exist"
        )

    db.query(models.Control).filter(models.Control.id == rover_id).delete()

    db.commit()