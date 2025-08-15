from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP,text
from app.database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key= True, nullable = False)
    title = Column(String, nullable = False)
    caption = Column (String,nullable = False)
    content = Column (String,nullable = False)
    published = Column (Boolean, server_default = 'True',nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False,server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key = False, nullable = False)
    owner = relationship("Users")


class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key= True, nullable = False)
    email = Column(String,nullable= False, unique=True)
    password = Column (String,nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False,server_default = text('now()'))


class votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key= True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"),primary_key= True)

Base = Base

