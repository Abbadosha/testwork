from fastapi import FastAPI, status, Depends
from rest_models import User, Article, Video, Comments
import DB_models
import database_cfg
from sqlalchemy.orm import Session
import math
from typing import TypeVar, Generic




app = FastAPI()



def get_db_session():
    """getting and mantaining DB session"""
    db=database_cfg.Session_local
    try:
        yield db
    finally:
        db.close()

def get_slice(seq, offset):
    """making slise for pagination"""
    for start in range(0, len(seq), offset):
        yield seq[start:start+offset]



@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(user:User, db: Session= Depends(get_db_session)):
    """Creating user in table user"""
    new_user = DB_models.User_tbl(
        email=user.email,
        usr_password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/articles',  status_code=status.HTTP_201_CREATED)
def create_article(article:Article, db: Session= Depends(get_db_session)):
    """Creating article"""
    new_article= DB_models.Article_tbl(
        user_id=article.user_id,
        article_name=article.article_name,
        article=article.article
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@app.post('/videos',  status_code=status.HTTP_201_CREATED)
def create_video(video:Video, db: Session= Depends(get_db_session)):
    """Creating video"""
    new_video= DB_models.Video_tbl(
        user_id=video.user_id,
        video_name=video.video_name,
        video_url=video.video_url
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video

@app.post('/comments',  status_code=status.HTTP_201_CREATED)
def create_comments(comments:Comments, db: Session= Depends(get_db_session)):
    """Creating video"""
    new_comments= DB_models.Comments(
        user_id=comments.user_id,
        article_id=comments.article_id,
        video_id=comments.video_id,
        comments_txt=comments.comments_txt
    )
    db.add(new_comments)
    db.commit()
    db.refresh(new_comments)
    return new_comments



@app.get('/users/{user_id}', status_code=status.HTTP_200_OK)
def get_one_user(user_id:int, db: Session= Depends(get_db_session)):
    """Getting user data"""
    resp = db.query(DB_models.User_tbl).filter(DB_models.User_tbl.user_id==user_id).first()
    return resp

@app.get('/articles/{article_id}', status_code=status.HTTP_200_OK)
def get_one_article(article_id:int, db: Session= Depends(get_db_session)):
    """Getting articles data"""
    resp = db.query(DB_models.Article_tbl).filter(DB_models.Article_tbl.article_id==article_id).first()
    return resp

@app.get('/videos/{video_id}', status_code=status.HTTP_200_OK)
def get_one_video(video_id:int, db: Session= Depends(get_db_session)):
    """Getting videos data"""
    resp = db.query(DB_models.Video_tbl).filter(DB_models.Video_tbl.video_id==video_id).first()
    return resp

@app.get('/comments/{comment_id}', status_code=status.HTTP_200_OK)
def get_one_comment(comment_id:int, db: Session= Depends(get_db_session)):
    """Getting comments data"""
    resp = db.query(DB_models.Comments).filter(DB_models.Comments.comment_id==comment_id).first()
    return resp



@app.put('/users/{user_id}', status_code=status.HTTP_200_OK)
def update_one_user(user_id:int, user:User, db: Session= Depends(get_db_session)):
    """Updating users data"""
    user_to_upd = db.query(DB_models.User_tbl).filter(DB_models.User_tbl.user_id==user_id).first()
    user_to_upd.email=user.email
    user_to_upd.usr_password=user.password
    db.commit()
    db.refresh(user_to_upd)
    return user_to_upd

@app.put('/articles/{article_id}', status_code=status.HTTP_200_OK)
def update_one_article(article_id:int, article:Article, db: Session= Depends(get_db_session)):
    """Updating articles data"""
    article_to_upd = db.query(DB_models.Article_tbl).filter(DB_models.Article_tbl.article_id==article_id).first()
    article_to_upd.user_id=article.user_id
    article_to_upd.article_name=article.article_name
    article_to_upd.article=article.article
    db.commit()
    db.refresh(article_to_upd)
    return article_to_upd

@app.put('/videos/{video_id}', status_code=status.HTTP_200_OK)
def update_one_video(video_id:int, video:Video, db: Session= Depends(get_db_session)):
    """Updating videos data"""
    video_to_upd = db.query(DB_models.Video_tbl).filter(DB_models.Video_tbl.video_id==video_id).first()
    video_to_upd.user_id=video.user_id
    video_to_upd.video_name=video.video_name
    video_to_upd.video_url=video.video_url
    db.commit()
    db.refresh(video_to_upd)
    return video_to_upd

@app.put('/comments/{comment_id}', status_code=status.HTTP_200_OK)
def update_one_comment(comment_id:int, comment:Comments, db: Session= Depends(get_db_session)):
    """Updating comments data"""
    comment_to_upd = db.query(DB_models.Comments).filter(DB_models.Comments.comment_id==comment_id).first()
    comment_to_upd.user_id=comment.user_id
    comment_to_upd.article_id =comment.article_id
    comment_to_upd.video_id =comment.video_id
    comment_to_upd.comments_txt =comment.comments_txt
    db.commit()
    db.refresh(comment_to_upd)
    return comment_to_upd



@app.delete('/users/{user_id}', status_code=status.HTTP_200_OK)
def del_user(user_id:int, db: Session= Depends(get_db_session)):
    """Deleteng users data"""
    db.query(DB_models.User_tbl).filter(DB_models.User_tbl.user_id == user_id).delete(synchronize_session=False)  # documentation of sqlalchemy
    db.commit()
    return {'done': f'User {user_id} deleted!'}


@app.delete('/articles/{article_id}', status_code=status.HTTP_200_OK)
def del_article(article_id:int,  db: Session= Depends(get_db_session)):
    """Deleteng articles data"""
    db.query(DB_models.Article_tbl).filter(DB_models.Article_tbl.article_id == article_id).delete(synchronize_session=False)  # documentation of sqlalchemy
    db.commit()
    return {'done': f'Article {article_id} deleted!'}

@app.delete('/videos/{video_id}', status_code=status.HTTP_200_OK)
def del_video(video_id:int,  db: Session= Depends(get_db_session)):
    """Deleteng videos data"""
    db.query(DB_models.Video_tbl).filter(DB_models.Video_tbl.video_id == video_id).delete(synchronize_session=False)  # documentation of sqlalchemy
    db.commit()
    return {'done': f'Video {video_id} deleted!'}

@app.delete('/comments/{comment_id}', status_code=status.HTTP_200_OK)
def del_comment(comment_id:int, db: Session= Depends(get_db_session)):
    """Deleteng comments data"""
    db.query(DB_models.Comments).filter(DB_models.Comments.comment_id == comment_id).delete(synchronize_session=False)  # documentation of sqlalchemy
    db.commit()
    return {'done': f'Comment {comment_id} deleted!'}



@app.get('/users')
def get_all_users(page_num: int = 1, page_size: int = 2, db: Session= Depends(get_db_session)):
    """Getting paginated users data"""
    db_array = db.query(DB_models.User_tbl).all()
    data_array = [i for i in db_array]
    resp_arr = list(get_slice(data_array, page_size))[page_num-1]
    len_data = len(data_array)
    total_pages = math.ceil(len_data/page_size)
    return{"data": resp_arr, "meta": {"current": page_num, "last_page": total_pages, "per_page": page_size, "total": len_data}}

@app.get('/articles')
def get_all_articles(page_num: int = 1, page_size: int = 2, db: Session= Depends(get_db_session)):
    """Getting articles users data"""
    db_array = db.query(DB_models.Article_tbl).all()
    data_array = [i for i in db_array]
    resp_arr = list(get_slice(data_array, page_size))[page_num-1]
    len_data = len(data_array)
    total_pages = math.ceil(len_data/page_size)
    return{"data": resp_arr, "meta": {"current": page_num, "last_page": total_pages, "per_page": page_size, "total": len_data}}

@app.get('/videos')
def get_all_videos(page_num: int = 1, page_size: int = 2, db: Session= Depends(get_db_session)):
    """Getting videos users data"""
    db_array = db.query(DB_models.Video_tbl).all()
    data_array = [i for i in db_array]
    resp_arr = list(get_slice(data_array, page_size))[page_num-1]
    len_data = len(data_array)
    total_pages = math.ceil(len_data/page_size)
    return{"data": resp_arr, "meta": {"current": page_num, "last_page": total_pages, "per_page": page_size, "total": len_data}}

@app.get('/comments')
def get_all_comments(page_num: int = 1, page_size: int = 2, db: Session= Depends(get_db_session)):
    """Getting comments users data"""
    db_array = db.query(DB_models.Comments).all()
    data_array = [i for i in db_array]
    resp_arr = list(get_slice(data_array, page_size))[page_num-1]
    len_data = len(data_array)
    total_pages = math.ceil(len_data/page_size)
    return{"data": resp_arr, "meta": {"current": page_num, "last_page": total_pages, "per_page": page_size, "total": len_data}}








