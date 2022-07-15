from pydantic import BaseModel


class Article(BaseModel):
    id: int
    name: str
    link: str
    date: str
    labels: str
    content: str
    
    class Config:
        orm_mode = True