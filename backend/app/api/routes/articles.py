from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_user_from_request, verify_auth_global
from app.crud import article as article_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.article import ArticleCreate, ArticleRead, ArticleUpdate

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    dependencies=[Depends(verify_auth_global)],
)


@router.get("/", response_model=list[ArticleRead])
def list_articles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    """Получить список статей текущего пользователя"""
    return article_crud.get_articles_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@router.post("/", response_model=ArticleRead, status_code=status.HTTP_201_CREATED)
def create_article(
    article_in: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    """Создать новую статью"""
    return article_crud.create_article(db, article_in, user_id=current_user.id)


@router.get("/{article_id}", response_model=ArticleRead)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    """Получить статью по ID"""
    db_article = article_crud.get_article(db, article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    if db_article.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return db_article


@router.put("/{article_id}", response_model=ArticleRead)
def update_article(
    article_id: int,
    article_in: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    """Обновить статью"""
    db_article = article_crud.get_article(db, article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    if db_article.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return article_crud.update_article(db, db_article, article_in)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    """Удалить статью"""
    db_article = article_crud.get_article(db, article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    if db_article.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    article_crud.delete_article(db, db_article)