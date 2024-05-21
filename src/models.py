import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    fullname = Column(String)
    posts = relationship('Post', back_populates='user')
    followers = relationship('Follower', back_populates='followed_user', foreign_keys='Follower.followed_user_id')
    following = relationship('Follower', back_populates='follower_user', foreign_keys='Follower.follower_user_id')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    caption = Column(String)
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    follower_user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    followed_user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    follower_user = relationship('User', foreign_keys=[follower_user_id], back_populates='following')
    followed_user = relationship('User', foreign_keys=[followed_user_id], back_populates='followers')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    type = Column(String)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship('Post', back_populates='media')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    comment_text = Column(String)
    user = relationship('User')
    post = relationship('Post', back_populates='comments')

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
