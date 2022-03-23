import logging
import os
import pathlib

import ffmpeg
import sqlalchemy as db
import sqlite3database
from sqlalchemy import select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from tqdm import tqdm

from config import *
from models import *

Base = automap_base()
maintain_engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files.sqlite3")
Base.prepare(maintain_engine, reflect=True)
maintain_session = Session(maintain_engine)
logging.basicConfig(filename='encoder.log', level=logging.INFO)

my_videos = maintain_session.execute(select(Video)).scalars().all()
for mov in tqdm(my_videos):
    maintain_session.expunge_all()
    if not os.path.isfile(mov.file_name):
        logging.info(f'{mov.file_name} is missing')
        maintain_session.delete(mov)
        maintain_session.commit()
    else:
        normal_name = os.path.join(all_files, Video.normalized_name(mov.file_name))
        if normal_name != mov.file_name:
            # logging.info(f'{file_name} is renamed to {normal_name}')
            if not os.path.isfile(normal_name):
                logging.info(f'{mov.file_name} is renamed to {normal_name}')
                os.rename(mov.file_name, normal_name)
            mov.file_name = normal_name

maintain_session.commit()


my_list = sorted(os.scandir(all_files), key=os.path.getctime)
for current_file in tqdm(my_list):
    if current_file.is_file() and os.path.splitext(current_file)[1].lower() == '.mp4':
        informer = ffmpeg.probe(current_file.path)
        video_stream = next((stream for stream in informer['streams'] if stream['codec_type'] == 'video'), None)
        width = int(video_stream['width'])
        height = int(video_stream['height'])

        select_statement = select(Video).where(Video.duration == float(video_stream['duration']))
        new_video = Video()
        old_video = maintain_session.execute(select_statement).first()
        if old_video:
            new_video = old_video[0]
        else:
            new_video = Video._init_from_file(current_file.path)
            maintain_session.add(new_video)
        maintain_session.commit()
        new_person = Person
        people = Person.get_people(current_file.path)
        for file_person in people:
            if file_person == '':
                continue
            person_select_statement = select(Person).where(Person.name == file_person)
            old_person = maintain_session.execute(person_select_statement).first()
            if old_person:
                new_person = old_person[0]
            else:
                new_person = Person(file_person, 1)
                maintain_session.add(new_person)
                new_person.get_net_data()
            maintain_session.commit()
            new_video.people.append(new_person)
            new_person.scene_count = new_person.video_count+1
            maintain_session.commit()
        else:
            new_person = None
        new_tag = Tag
        tags = Tag.get_file_tags(current_file.path)
        for file_tag in tags:
            if file_tag == '':
                continue
            tag_select_statement = select(Tag).where(Tag.name == file_tag)
            old_tag = maintain_session.execute(tag_select_statement).first()
            if old_tag:
                new_tag = old_tag[0]
            else:
                new_tag = Tag(file_tag)
                maintain_session.add(new_tag)
            maintain_session.commit()
            new_video.tags.append(new_tag)
            if new_person:
                new_tag.people.append(new_person)
            maintain_session.commit()

maintain_session.close()
maintain_engine.dispose()
