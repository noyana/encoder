import os
import re
from datetime import datetime
from sys import platform
from tkinter import Label

from numpy import delete
from config import *

import ffmpeg
import sqlalchemy as db
import sqlite3database
from sqlalchemy import Column, ForeignKey, MetaData, Table, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, DateTime, Date, Float, Integer, String, Text

#engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files_new.sqlite3")
#model_session = Session(engine)
#meta = MetaData()
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
    videos = relationship('Video', secondary=people_videos_association, backref='people', lazy='subquery')
    default_tags = Column(String(120), index=True)
    birthplace = Column(String(3), index=True, nullable=True, default=None)
    birthdate = Column(DateTime, nullable=True, default=None)
    ethnicity = Column(String(15), index=True, nullable=True, default=None)
    hair_color = Column(String(10), index=True, nullable=True, default=None)
    nationality = Column(String(20), index=True, nullable=True, default=None)
    cupsize = Column(String(10), index=True, nullable=True, default=None)

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
        rc = session.query(Video).with_parent(self).count()
        session.close()
        return rc

    @property
    def personal_tags(self):
        return self.default_tags

    @personal_tags.setter
    def personal_tags(self, tags):
        if self.default_tags:
            dt = self.default_tags + " " + tags
        else:
            dt = tags
        dt = dt.split(',')
        dt = list(set(dt))
        dt.sort()
        self.default_tags = ','.join(dt)

    def get_net_data(self):
        model_engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files.sqlite3")
        model_session = Session(model_engine)
        code_encoder = {'gb': 'uk', 'us': None, 'gr': 'grk', 'br': 'brz', 'co': 'col'}
        ethn_encoder = {'black': 'b', 'asian': 'as', 'caucasian': None}
        hair_encoder = {'blonde': 'bl', 'black': 'br', 'brown': 'br', 'red': 'rh'}
        info = get_person_info(self.name)
        if info:
            if info.get('data').get('extras').get('birthplace_code'):
                self.birthplace = info.get('data').get('extras').get('birthplace_code').lower()
            if self.birthplace in code_encoder.keys():
                self.birthplace = code_encoder.get(self.birthplace)
            self.nationality = info.get('data').get('extras').get('nationality')
            if info.get('data').get('extras').get('birthday'):
                self.birthdate = datetime.strptime(info.get('data').get('extras').get('birthday'), "%Y-%m-%d")
                now = datetime.now()
                if self.birthdate < datetime(now.year-35, now.month, now.day):
                    self.personal_tags = ',' + 'mi'
                elif self.birthdate > datetime(now.year-20, now.month, now.day):
                    self.personal_tags = ',' + 'y'
            self.ethnicity = info.get('data').get('extras').get('ethnicity')
            if self.ethnicity in ethn_encoder.keys():
                self.personal_tags = ',' + ethn_encoder.get(self.ethnicity.lower())
            self.hair_color = info.get('data').get('extras').get('hair_colour')
            if self.hair_color in hair_encoder.keys():
                self.personal_tags = ',' + hair_encoder.get(self.hair_color.lower())
            self.cupsize = info.get('data').get('extras').get('cupsize')
            if self.birthplace:
                if self.birthplace != 'us':
                    self.personal_tags = ',' + self.birthplace.lower()
            model_session.commit()
        model_session.close()
        model_engine.dispose()


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

    @property
    def file_name(self) -> str:
        if platform == 'win32' or platform == 'win64':
            return self.file_name_windows
        elif platform == 'linux':
            return self.file_name_linux

    @file_name.setter
    def file_name(self, file_name: str) -> None:
        if platform == 'win32' or platform == 'win64':
            self.file_name_windows = file_name
        elif platform == 'linux':
            self.file_name_linux = file_name

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
                tag_str = name[1].replace(cstr[0], '').replace('(', '').replace(')', '')
            else:
                count = 1
                tag_str = name[1].replace('.mp4', '').replace('(', '').replace(')', '')
            # tags = tag_str.split(',')
            # name = name[0]
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
        n.name = new_name.strip(',')
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
        model_engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files.sqlite3")
        model_session = Session(model_engine)
        new_file_count = 1
        sorted_name = ''
        if new_people:
            people_select_str = select(Person.name, Person.scene_count, Person.default_tags).where(
                Person.name.in_(new_people)).order_by(Person.scene_count.desc())
            sorted_people = model_session.execute(people_select_str).fetchall()
            all_list = []
            for person in [(x, z) for x, y, z in sorted_people]:
                all_list += [person[0].strip()]
                if person[1]:
                    new_tags += person[1].split(',')
                if person[0] in all_list:
                    new_people.remove(person[0])
            all_list += new_people
            new_tags = list(dict.fromkeys(new_tags))
            new_tags.sort()
            if new_is_movie:
                sorted_name = new_name + ',#(' + ','.join(new_tags) + '),(1).mp4'
            else:
                sorted_name = ','.join(all_list) + ',#(' + ','.join(new_tags) + '),(1).mp4'
            while os.path.isfile(all_files + os.path.sep + sorted_name):
                new_file_count += 1
                if new_is_movie:
                    sorted_name = new_name + ',#(' + ','.join(new_tags) + '),('+str(new_file_count) + ').mp4'
                else:
                    sorted_name = ','.join(all_list) + ',#(' + ','.join(new_tags) + '),('+str(new_file_count) + ').mp4'
        else:
            sorted_name = new_name + ',#(' + ','.join(new_tags) + '),('+str(new_file_count) + ').mp4'
            while os.path.isfile(all_files + os.path.sep + sorted_name):
                new_file_count += 1
                if new_is_movie:
                    sorted_name = new_name + ',#(' + ','.join(new_tags) + '),('+str(new_file_count) + ').mp4'
        model_session.close_all()
        model_engine.dispose()
        return sorted_name

    @ classmethod
    def normalized_name(cls, file_name: str) -> str:

        if os.path.isfile(file_name):
            (new_name, new_tags, new_file_count, new_people, new_is_movie) = Video.get_video_info(file_name)
        sorted_name = Video.name_sort(new_name.strip(','), new_tags, new_file_count, new_people, new_is_movie)
        return sorted_name


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False, index=True)
    description = Column(String(50), index=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    people = relationship(Person, secondary=tags_people_association, backref='tags', lazy='subquery')
    videos = relationship(Video, secondary=tags_videos_association, backref='tags', lazy='subquery')

    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"{self.description} (\#{self.name})"

    @ classmethod
    def get_file_tags_old(cls, file_name: str) -> str:
        if file_name.find('#') >= 0:
            file_name.replace(',', ', ').replace('  ', ' ')
            return file_name[(file_name.find('#')+2): (file_name.find(']'))].replace(', ', ',').split(',')
        else:
            return ''

    @ classmethod
    def get_file_tags(cls, file_name: str):
        (new_name, new_tags, new_file_count, new_people, new_is_movie) = Video.get_video_info(file_name)
        return new_tags
