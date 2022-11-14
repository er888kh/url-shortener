import datetime
import random

import sqlalchemy as sqlal
from sqlalchemy.orm import Session

import models, schemas


ALPHABET = "abcdefghijklmnopqrstuvwxyz123456"


def check_url_age(db: Session, res: models.Shortener) -> models.Shortener | None:
    if res is None:
        return None

    if res.expire_time < datetime.datetime.now():
        db.execute(sqlal.delete(models.Shortener).where(models.Shortener.id == res.id))
        db.commit()
        res = None

    return res


def maybe_commit(db: Session) -> bool:
    if random.randint(1, 10) == 1:
        db.commit()
        return True

    return False


def add_url_visit(db: Session, visits: int, url_id: int) -> bool:
    db.execute(
        sqlal.update(models.Shortener)
        .where(models.Shortener.id == url_id)
        .values(visits=visits)
    )
    return maybe_commit(db)


def create_token(len: int) -> str:
    return "".join(random.choice(ALPHABET) for _ in range(len))


def get_url(
    db: Session, url_id: int, add_visit: bool = False, keep_secret: bool = False
) -> models.Shortener | None:
    res = db.query(models.Shortener).filter(models.Shortener.id == url_id).first()
    res = check_url_age(db, res)
    if res is None:
        return None

    if add_visit:
        res.visits += 1

    return res


def get_url_by_short(
    db: Session, key: str, add_visit: bool = False, keep_secret: bool = False
) -> models.Shortener | None:
    res = db.query(models.Shortener).filter(models.Shortener.shortened == key).first()
    res = check_url_age(db, res)
    if res is None:
        return None

    if add_visit:
        res.visits += 1

    return res


def create_url(db: Session, url: schemas.ShortenerCreate) -> models.Shortener:
    token = create_token(30)
    short = create_token(20)

    if url.url[:4] != "http":
        url.url = "http://" + url.url
 
    db_url = models.Shortener(**url.dict(), token=token, shortened=short, visits=0)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def delete_url(db: Session, url: models.Shortener) -> None:
    db.execute(sqlal.delete(models.Shortener).where(models.Shortener.id == url.id))
    db.commit()
