from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate


def get_article(db: Session, article_id: int) -> Optional[Article]:
    return db.query(Article).filter(Article.id == article_id).first()


def get_articles(db: Session, skip: int = 0, limit: int = 100) -> List[Article]:
    return db.query(Article).offset(skip).limit(limit).all()


def create_article(db: Session, article_in: ArticleCreate) -> Article:
    db_article = Article(**article_in.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(db: Session, db_article: Article, article_in: ArticleUpdate) -> Article:
    data = article_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_article, field, value)
    db.commit()
    db.refresh(db_article)
    return db_article


def delete_article(db: Session, db_article: Article) -> None:
    db.delete(db_article)
    db.commit()

