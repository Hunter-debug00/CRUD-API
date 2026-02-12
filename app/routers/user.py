from fastapi import Depends, HTTPException, status, APIRouter
from app.db import get_db
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .. import models, schemas, utils

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    new_user = models.User(
        **user.model_dump(exclude={"password"}), password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: UUID, db: Session = Depends(get_db)):
    user = db.get(models.User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
