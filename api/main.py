from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/item/{item_id}", response_model=schemas.Article)
def get_article(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_article(db, article_id=item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return db_item

@app.get("/items", response_model=dict[str, dict[str, str]])
def get_all_articles(db: Session = Depends(get_db)):
    articles = crud.get_all_articles(db)
    return articles

@app.delete("/item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_article(db, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")