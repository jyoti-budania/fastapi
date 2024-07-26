from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
   # id: int
    # created_at: str

    class Config:
        from_attributes = True