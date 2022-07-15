from sqlalchemy.orm import Session
import models


def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def get_all_articles(db: Session):
    items = db.query(models.Article).all()
    return {
        str(item.id): {
            "name": item.name,
            "link": item.link,
            "date": item.date,
            "labels": item.labels,
            "content": item.content
            } for item in items
    }

def delete_article(db: Session, article_id: int):
    article = get_article(db, article_id)
    if article:
        db.delete(article)
        db.commit()
    return article
