import sqlite3database
import sqlalchemy as db
import os
import ffmpeg

from datetime import datetime
from sys import platform
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Column, Table, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, Float, Text, Integer, String, DateTime, Boolean, Numeric

engine = db.create_engine("sqlite:///files.sqlite3")
meta = MetaData()
Base = declarative_base()
session = session = Session(engine)


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
    scene_count = Column(BigInteger, default=1)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    videos = relationship('Video', secondary=people_videos_association, backref='people')
#    tags = relationship('Tag', secondary=tags_people_association, backref='people')

    def __str__(self) -> str:
        return f"{self.name} "

    def __init__(self, name, count=1) -> None:
        self.name = name
        self.scene_count = count

    def get_people(file_name: str) -> tuple:
        if file_name.find('_') >= 0:  # movie
            return ''
        else:
            return file_name.strip().split(', ')

    @property
    def video_count(self):
        return session.query(Video).with_parent(self).count()


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name_linux = Column(Text, nullable=True, index=True)
    file_name_windows = Column(Text, nullable=True, index=True)
    file_size = Column(BigInteger, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    extension = Column(String(20), nullable=False, default='.mp4')
    duration = Column(Float, nullable=False)
    is_movie = Column(Boolean, nullable=False, default=False)
    file_count = Column(Integer, nullable=True, default=1)
    file_date = Column(DateTime, nullable=False)
    width = Column(Integer, nullable=True, default=854)
    height = Column(Integer, nullable=True, default=480)
    frame_rate = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    def __str__(self) -> str:
        if self.is_movie:
            t = 'M'
        else:
            t = 'S'
        return f"{t}: {self.name} ({self.file_count})"

    @classmethod
    def get_video_name(cls, file_name: str) -> str:
        file_name.replace(',', ', ').replace('  ', ' ')
        if file_name.find('_') >= 0:  # movie
            return file_name[1:(file_name[1:].find('_')+1)].strip()
        else:  # scene
            if file_name.find('#') >= 0:  # tag
                return file_name[0:(file_name.find('#')-1)].strip()
            elif file_name.find('('):  # number
                return file_name[0:(file_name.find('(')-1)].strip()

    @classmethod
    def get_video_count(cls, file_name: str) -> str:
        if file_name.find('_') >= 0:  # movie
            if file_name.find('Sc') >= 0:
                return file_name[(file_name.find('Sc')):]
            elif file_name.find('#') >= 0:
                return -1
        else:  # scene
            return file_name[(file_name.find('(')+1):(file_name.find(')'))]

    @classmethod
    def get_video_info(cls, file_name: str) -> str:
        file_name = os.path.basename(file_name)
        name = cls.get_video_name(file_name)
        count = cls.get_video_count(file_name)
        return name, count

    @classmethod
    def _init_from_file(cls, file_name: str):
        informer = ffmpeg.probe(file_name)
        stream_number = 0
        for stream in informer['streams']:
            if stream['codec_type'] == 'video':
                stream_number = stream['index']
        new_name, new_file_count = Video.get_video_info(file_name)
        n = Video()
        n.name = new_name
        n.file_count = new_file_count
        n.ext = os.path.splitext(file_name)
        if platform == 'linux':
            n.file_name_linux = file_name
        else:  # scene
            n.file_name_windows = file_name
        n.file_size = os.path.getsize(file_name)
        n.file_date = datetime.fromtimestamp(os.path.getctime(file_name))
        n.duration = float(informer['streams'][stream_number]['duration'])
        n.is_movie = file_name.find('_') >= 0
        n.width = int(informer['streams'][stream_number]['width'])
        n.height = int(informer['streams'][stream_number]['height'])
        n.frame_rate = int(informer['streams'][stream_number]['bit_rate'])
        return n


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), index=True)
    description = Column(String(50), index=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    people = relationship(Person, secondary=tags_people_association, backref='tags')
    videos = relationship(Video, secondary=tags_videos_association, backref='tags')

    def __str__(self) -> str:
        return f"{self.description} (\#{self.name})"

    @classmethod
    def get_file_tags(cls, file_name: str) -> str:
        if file_name.find('#') >= 0:
            file_name.replace(',', ', ').replace('  ', ' ')
            return file_name[(file_name.find('#')+2):(file_name.find(']'))].replace(', ', ',').split(',')
        else:
            return ''

    def __init__(self, name, description='To edit') -> None:
        name = name
        description = description
