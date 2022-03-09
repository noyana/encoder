import sqlite3database
import sqlalchemy as db

from datetime import datetime

from sqlalchemy.orm import Session, relationship
from sqlalchemy import Column, Table, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, Float, Text, Integer, String, DateTime, Boolean, Numeric

engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files.sqlite3")
meta = MetaData()

Base = declarative_base()

people_videos_association = Table(
    'people_videos', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('video_id', Integer, ForeignKey('videos.id')),
    Column('person_id', Integer, ForeignKey('people.id')),
)

tags_videos_association = Table(
    'tags_videos', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('video_id', Integer, ForeignKey('videos.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)

tags_people_association = Table(
    'tags_people', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('people_id', Integer, ForeignKey('people.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), index=True)
    count = Column(BigInteger, default=1)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    videos = relationship('Video', secondary=people_videos_association, backref='people')
#    tags = relationship('Tag', secondary=tags_people_association, backref='people')


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(Text, index=True)
    file_size = Column(BigInteger, index=True)
    name = Column(String, index=True)
    extension = Column(String(20), default='.mp4')
    duration = Column(Float)
    is_movie = Column(Boolean, default=False)
    file_count = Column(Integer, default=1)
    file_date = Column(DateTime)
    width = Column(Integer, default=854)
    height = Column(Integer, default=480)
    frame_rate = Column(Float)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
#    people = relationship('People', secondary=people_videos_association, backref='videos')
#    tags = relationship('Tag', secondary=tags_videos_association, backref='videos')

    def __repr__(self) -> str:
        if self.is_movie:
            t = 'M'
        else:
            t = 'S'
        return f"{t}:{self.name} ({self.file_count})"


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), index=True)
    description = Column(String(50), index=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    people = relationship('Person', secondary=tags_people_association, backref='tags')
    videos = relationship('Video', secondary=tags_videos_association, backref='tags')


Base.metadata.create_all(engine)
