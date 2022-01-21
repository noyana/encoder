from posixpath import splitext
from xml.etree.ElementInclude import include
import sqlite3database
import sqlalchemy as db
import os
import ffmpeg

from better_ffmpeg_progress import FfmpegProcess
from models import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import select
from config import *

Base = automap_base()
engine = db.create_engine("sqlite:///files.sqlite3")
Base.prepare(engine, reflect=True)
session = Session(engine)

for current_path in video_paths:
    for current_file in sorted(os.scandir(current_path), key=os.path.getctime):
        if current_file.is_file() and os.path.splitext(current_file)[1].lower() == '.mp4':
            # print(current_file.name)
            informer = ffmpeg.probe(current_file.path)
            stream_number = 0
            for stream in informer['streams']:
                if stream['codec_type'] == 'video':
                    stream_number = stream['index']
            select_statement = select(Video).where(Video.duration == float(
                informer['streams'][stream_number]['duration']))
            new_video = Video()
            old_video = session.execute(select_statement).first()
            if old_video:
                new_video = old_video[0]
            else:
                new_video = Video._init_from_file(current_file.path)
                session.add(new_video)
            session.commit()
            new_person = Person
            people = Person.get_people(new_video.name)
            for file_person in people:
                if file_person == '':
                    continue
                person_select_statement = select(Person).where(Person.name == file_person)
                old_person = session.execute(person_select_statement).first()
                if old_person:
                    new_person = old_person[0]
                else:
                    new_person = Person(file_person, 1)
                    session.add(new_person)
                session.commit()
                new_video.people.append(new_person)
                new_person.scene_count = new_person.video_count
                session.commit()
            new_tag = Tag
            tags = Tag.get_file_tags(current_file.path)
            for file_tag in tags:
                if file_tag == '':
                    continue
                tag_select_statement = select(Tag).where(Tag.name == file_tag)
                old_tag = session.execute(tag_select_statement).first()
                if old_tag:
                    new_tag = old_tag[0]
                else:
                    new_tag = Tag(file_tag, '')
                    session.add(new_tag)
                session.commit()
                new_video.tags.append(new_tag)
                new_tag.people.append(new_person)
                session.commit()


for raw_file in sorted(os.scandir(raw_files), key=os.path.getsize, reverse=True):
    if raw_file.is_file():
        print(raw_file.name)
        if "_" in raw_file.name:
            is_movie = True
            name, file_count = Video.get_video_info(raw_file.name)
            tags = Tag.get_file_tags(raw_file.name)
            print(f"\t {name} ({file_count}) ")
        else:
            is_movie = False
            name, file_count = Video.get_video_info(raw_file.name)
            tags = Tag.get_file_tags(raw_file.name)
            people = Person.get_people(name)
            print("\t", name, file_count, people)
        converter = ffmpeg()
