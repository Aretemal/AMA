from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import article as article_crud
from app.db.session import get_db
from app.schemas.article import ArticleCreate, ArticleRead, ArticleUpdate

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=list[ArticleRead])
def list_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return article_crud.get_articles(db, skip=skip, limit=limit)


@router.post("/", response_model=ArticleRead, status_code=status.HTTP_201_CREATED)
def create_article(article_in: ArticleCreate, db: Session = Depends(get_db)):
    return article_crud.create_article(db, article_in)


@router.get("/{article_id}", response_model=ArticleRead)
def get_article(article_id: int, db: Session = Depends(get_db)):
    db_article = article_crud.get_article(db, article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return db_article


@router.put("/{article_id}", response_model=ArticleRead)
def update_article(article_id: int, article_in: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = article_crud.get_article(db, article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return article_crud.update_article(db, db_article, article_in)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = article_crud.get_article(db, article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    article_crud.delete_article(db, db_article)