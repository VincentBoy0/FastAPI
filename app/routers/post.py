from .. import models, schemas, oauth2
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/", response_model=List[schemas.PostOut])
# def get_post(db: Session = Depends(get_db),
#              current_user: int = Depends(oauth2.get_current_user),
#              limit: int = 10,
#              skip: int = 0,
#              search: Optional[str] = ""):

#     posts = db.query(models.Post).filter(
#         models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
#     results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
#         models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
#     # results = db.query(
#     #     models.Post, 
#     #     func.count(models.Vote.post_id).label("votes"),
#     #     models.User  # Include User (owner)
#     # ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
#     # .join(models.User, models.User.id == models.Post.owner_id, isouter=True) \
#     # .group_by(models.Post.id, models.User.id) \
#     # .all()

#     formatted_results = [
#         {"post": {key: getattr(post, key) for key in post.__dict__ if key != "_sa_instance_state"}, "votes": votes}
#         for post, votes in results
#     ]
#     print(formatted_results)
#     return results

@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user),
             limit: int = 10,
             skip: int = 0,
             search: Optional[str] = ""):

    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(
        models.Post, 
        func.count(models.Vote.post_id).label("votes"),
        models.User  # Include User (owner)
    ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
    .join(models.User, models.User.id == models.Post.owner_id, isouter=True) \
    .group_by(models.Post.id, models.User.id) \
    .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    formatted_results = [
        {
            "post": {
                **schemas.Post.model_validate(post).model_dump(),  # Convert Post object to dict
                "owner": schemas.UserOut.model_validate(owner).model_dump() if owner else None  # Add owner inside post
            },
            "votes": votes
        }
        for post, votes, owner in results
    ]
    
    # print(formatted_results)  # Debugging
    return formatted_results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(
        **post.dict()
    )
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, 
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(
        models.Post, 
        func.count(models.Vote.post_id).label("votes"),
        models.User  # Include User (owner)
    ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
    .join(models.User, models.User.id == models.Post.owner_id, isouter=True) \
    .group_by(models.Post.id, models.User.id) \
    .filter(models.Post.id == id).first()

    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id = {id} was not found")

    post_obj, votes, owner = post
    formatted_result = {
        "post": {
            **schemas.Post.model_validate(post_obj).model_dump(),  # Convert Post object to dict
            "owner": schemas.UserOut.model_validate(owner).model_dump() if owner else None  # Add owner inside post
        },
        "votes": votes
    }

    return formatted_result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(f"DELETE FROM posts WHERE id = {id} RETURNING *;")
    # deleted_post = cursor.fetchone()
    # conn.commit()


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f"post with {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='No authorzied to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, 
                updated_post: schemas.PostCreate, 
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
    #                 (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='No authorzied to perform requested action')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
