from tqdm import tqdm
import sqlite3database
import sqlalchemy as db
import os
import ffmpeg
import logging
import pathlib

#from better_ffmpeg_progress import FfmpegProcess
from models import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import select
from config import *

Base = automap_base()
engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files.sqlite3")
Base.prepare(engine, reflect=True)
session = Session(engine)
logging.basicConfig(filename='encoder.log', level=logging.INFO)

currentDirectory = pathlib.Path(raw_files)
currentPattern = "*.mp4"
my_list = sorted(currentDirectory.glob(currentPattern), key=os.path.getsize, reverse=True)
logging.info(f'{len(my_list)} raw files found to encode. Starting encoding at {datetime.now()}')
# for raw_file in my_list:
for raw_file in tqdm(my_list):
    if raw_file.is_file():
        options = {'codec:v': 'h264_amf', 's': '854x480', 'b:v': '768k', 'r': '23.976', 'codec:a': 'aac', 'b:a': '128k',
                   'ar': 44100, 'tune': 'film', 'preset': 'superfast', 'threads': 'auto'}
        (new_name, new_tags, new_file_count, new_people, new_is_movie) = Video.get_video_info(raw_file._str)
        normal_name = Video.normalized_name(raw_file._str)
        in_file = raw_file._str
        out_file = f"{all_files}{os.path.sep}{normal_name}"
        logging.info(f'{raw_file._str} is being encoded to {out_file} @ {datetime.now()}')
        start = datetime.now()
        ffmpeg.input(raw_file._str).output(out_file, **options).run(quiet=True)
        logging.info(f"{raw_file._str} has been encoded to {out_file} @ {datetime.now()}, lasted {datetime.now() - start}")
        if os.path.getsize(out_file) > 50*1024*1024:
            logging.info(f'{out_file} is being deleted')
            os.remove(raw_file._str)
        else:
            logging.info(f'{out_file} is being kept')

exit()
my_list = sorted(os.scandir(all_files), key=os.path.getctime)
for current_file in tqdm(my_list):
    if current_file.is_file() and os.path.splitext(current_file)[1].lower() == '.mp4':
        # if re.search("Friends", current_file.name):
        #    print(current_file.name)

        informer = ffmpeg.probe(current_file.path)
        video_stream = next((stream for stream in informer['streams'] if stream['codec_type'] == 'video'), None)
        width = int(video_stream['width'])
        height = int(video_stream['height'])

        select_statement = select(Video).where(Video.duration == float(
            video_stream['duration']))
        new_video = Video()
        old_video = session.execute(select_statement).first()
        if old_video:
            new_video = old_video[0]
        else:
            new_video = Video._init_from_file(current_file.path)
            session.add(new_video)
        session.commit()
        new_person = Person
        people = Person.get_people(current_file.path)
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
            new_person.scene_count = new_person.video_count+1
            session.commit()
        else:
            new_person = None
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
                new_tag = Tag(file_tag)
                session.add(new_tag)
            session.commit()
            new_video.tags.append(new_tag)
            if new_person:
                new_tag.people.append(new_person)
            session.commit()
