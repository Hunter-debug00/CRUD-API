from passlib.context import CryptContext
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def post_with_votes(post: models.Post, votes_count: int) -> schemas.PostWithVotes:
    post_data = schemas.PostWithVotes.model_validate(post)
    post_data.votes = votes_count   
    return post_data