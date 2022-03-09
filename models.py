import os
import re
from datetime import datetime
from sys import platform
from config import *

import ffmpeg
import sqlalchemy as db
import sqlite3database
from sqlalchemy import Column, ForeignKey, MetaData, Table, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql.sqltypes import (BigInteger, Boolean, DateTime, Float,
                                     Integer, Numeric, String, Text)


engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files_new.sqlite3")
session = Session(engine)

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
    Column('person_id', Integer, ForeignKey('people.id')),
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
    default_tags = Column(String(120), index=True)

    def __str__(self) -> str:
        return f"{self.name} "

    def __init__(self, name, count=1) -> None:
        self.name = name
        self.scene_count = count

    def get_people(file_name: str) -> tuple:
        (new_name, new_tags, new_file_count, new_people, new_is_movie) = Video.get_video_info(file_name)
        return new_people

    @property
    def video_count(self):
        engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files.sqlite3")
        session = Session(engine)
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
        pass

    @classmethod
    def get_video_count(cls, file_name: str) -> str:
        try:
            count = int(re.search("\((\d+)\).mp4", file_name))
            return count
        except ValueError:
            return None

    @classmethod
    def get_video_info(cls, file_name: str) -> tuple:
        file_name = os.path.basename(file_name)
        name = ""
        tags = []
        count = 1
        is_movie = None
        people = []
        name = file_name.split('#')
        if len(name) > 1:
            cstr = re.search("\((\d+)\).mp4", file_name)
            if cstr:
                count = int(cstr[1])
            else:
                count = 1
            tag_str = name[1].replace(cstr[0], '').replace('(', '').replace(')', '')
            #tags = tag_str.split(',')
            #name = name[0]
            tags = [t for t in tag_str.split(',') if t.isalpha()]
            if (not 'm' in tags) and (not 's' in tags):
                tags.append('s')
            name = name[0]
        else:
            tags.append('s')
            cstr = re.search("\((\d+)\).mp4", file_name)
            if cstr:
                count = int(cstr[1])
                name = file_name.replace(cstr[0], '').strip().rstrip(',')
            else:
                count = 1
                name = name[0].strip()
        if re.search(".mp4", name):
            name = name.replace('.mp4', '').strip()
        if not 'm' in tags:
            people = name.rstrip(',').split(',')
            for p in people:
                people.remove(p)
                people.append(p.strip())
            is_movie = False
        else:
            name = name.rstrip(',')
            is_movie = True
        tags = list(dict.fromkeys(tags))
        tags.sort()
        people = list(dict.fromkeys(people))
        people.sort()
        return (name, tags, count, people, is_movie)

    @ classmethod
    def _init_from_file(cls, file_name: str):
        informer = ffmpeg.probe(file_name)
        stream_number = 0
        for stream in informer['streams']:
            if stream['codec_type'] == 'video':
                stream_number = stream['index']
        (new_name, new_tags, new_file_count, new_people, new_is_movie) = Video.get_video_info(file_name)
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
        n.is_movie = new_is_movie
        n.width = int(informer['streams'][stream_number]['width'])
        n.height = int(informer['streams'][stream_number]['height'])
        n.frame_rate = int(informer['streams'][stream_number]['bit_rate'])
        return n

    @classmethod
    def name_sort(cls, new_name: str, new_tags, new_file_count: int, new_people, new_is_movie) -> str:
        engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files.sqlite3")
        session = Session(engine)

        sorted_name = ''
        if new_people:
            people_select_str = select(Person.name, Person.scene_count).where(
                Person.name.in_(new_people)).order_by(Person.scene_count.desc())
            sorted_people = session.execute(people_select_str).fetchall()
            all_list = []
            for person in [x for x, y in sorted_people]:
                all_list += [person.strip()]
                if person in all_list:
                    new_people.remove(person)
            all_list += new_people
            if new_is_movie:
                sorted_name = new_name + ',#(' + ','.join(new_tags) + '),('+str(new_file_count) + ').mp4'
            else:
                sorted_name = ','.join(all_list) + ',#(' + ','.join(new_tags) + '),('+str(new_file_count) + ').mp4'
            while os.path.isfile(all_files + os.path.sep + sorted_name):
                new_file_count += 1
                if new_is_movie:
                    sorted_name = new_name + ',#(' + ','.join(new_tags) + '),('+str(new_file_count) + ').mp4'
                else:
                    sorted_name = ','.join(all_list) + ',#(' + ','.join(new_tags) + \
                        '),('+str(new_file_count) + ').mp4'
        else:
            sorted_name = new_name + ',#(' + ','.join(new_tags) + '),('+str(new_file_count) + ').mp4'
            while os.path.isfile(all_files + os.path.sep + sorted_name):
                new_file_count += 1
                if new_is_movie:
                    sorted_name = new_name + ',#(' + ','.join(new_tags) + '),('+str(new_file_count) + ').mp4'
        session.close_all()
        engine.dispose()
        return sorted_name

    @classmethod
    def normalized_name(cls, file_name: str) -> str:

        if os.path.isfile(file_name):
            (new_name, new_tags, new_file_count, new_people, new_is_movie) = Video.get_video_info(file_name)
        sorted_name = Video.name_sort(new_name, new_tags, new_file_count, new_people, new_is_movie)
        return sorted_name


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False, index=True)
    description = Column(String(50), index=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    people = relationship(Person, secondary=tags_people_association, backref='tags')
    videos = relationship(Video, secondary=tags_videos_association, backref='tags')

    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"{self.description} (\#{self.name})"

    @ classmethod
    def get_file_tags_old(cls, file_name: str) -> str:
        if file_name.find('#') >= 0:
            file_name.replace(',', ', ').replace('  ', ' ')
            return file_name[(file_name.find('#')+2):(file_name.find(']'))].replace(', ', ',').split(',')
        else:
            return ''

    @ classmethod
    def get_file_tags(cls, file_name: str):
        (new_name, new_tags, new_file_count, new_people, new_is_movie) = Video.get_video_info(file_name)
        return new_tags
