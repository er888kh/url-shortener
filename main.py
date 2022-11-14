import dotenv
import os
import re

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import constr


import crud, models, schemas, database
from database import SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.commit()
        db.close()


app = FastAPI(title="Shopino backend task")


@app.on_event("startup")
def startup_event():
    dotenv.load_dotenv()
    if "RUN_MIGRATIONS" in os.environ:
        if os.environ["RUN_MIGRATIONS"] == "true":
            database.run_migrations(engine)


@app.get("/@/{url_id}", response_model=schemas.ShortenerNoSecret)
def get_url(url_id: int, db: Session = Depends(get_db)):
    res = crud.get_url(db, url_id=url_id, add_visit=True)
    if res is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return res


@app.post("/@/create", response_model=schemas.Shortener)
def create_url(url: schemas.ShortenerCreate, db: Session = Depends(get_db)):
    return crud.create_url(db, url=url)


@app.get("/{short_url}")
def get_shortened_url(
    short_url: constr(to_lower=True, max_length=20, regex="^[a-z0-9]+$"),
    db: Session = Depends(get_db),
):
    res = crud.get_url_by_short(db, short_url, add_visit=True)
    if res is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(res.url)


@app.delete("/@/delete")
def delete_url(url: schemas.ShortenerDelete, db: Session = Depends(get_db)):
    res = crud.get_url_by_short(db, url.shortened, add_visit=False, keep_secret=True)
    if res is None:
        raise HTTPException(status_code=401, detail="No such URL")
    if res.token != url.token:
        raise HTTPException(status_code=403, detail="Invalid token")
    crud.delete_url(db, res)
    return {}

@app.patch("/@/update")
def update_url(url: schemas.ShortenerUpdate, db: Session = Depends(get_db)):
    res = crud.get_url_by_short(db, url.shortened, add_visit=False, keep_secret=True)
    if res is None:
        raise HTTPException(status_code=401, detail="No such URL")
    if res.token != url.token:
        raise HTTPException(status_code=403, detail="Invalid token")
    res.url = url.url
    res.expire_time = url.expire_time
    return res