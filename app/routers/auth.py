from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, db, models, utils, oauth2
from sqlalchemy.orm import Session

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.TokenModel)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = oauth2.create_access_token(
        data={"user_id": str(user.id), "username": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}
