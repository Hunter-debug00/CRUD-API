from fastapi import Depends, HTTPException, status, APIRouter
from ..db import get_db
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List
from .. import models, schemas, utils, oauth2


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostWithVotes])
def get_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    query = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .where(models.Post.title.ilike(f"%{search}%"))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
    )

    results = db.execute(query).all()

    return [utils.post_with_votes(post, votes) for post, votes in results]


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostWithVotes)
def get_post(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    query = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .where(models.Post.id == id)
        .group_by(models.Post.id)
    )

    result = db.execute(query).first()

    if not result:
        raise HTTPException(status_code=404, detail="Post not found")

    post, votes = result
    return utils.post_with_votes(post, votes)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.get(models.Post, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action",
        )
    db.delete(post)
    db.commit()


@router.patch("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: UUID,
    data: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.get(models.Post, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action",
        )

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post
