from tqdm import tqdm
import sqlite3database
import sqlalchemy as db
import os
import ffmpeg
import logging
import pathlib

# from better_ffmpeg_progress import FfmpegProcess
from models import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import select
from config import *

Base = automap_base()
engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files.sqlite3")
Base.prepare(engine, reflect=True)
maintain_session = Session(engine)
logging.basicConfig(filename='encoder.log', level=logging.INFO)

currentDirectory = pathlib.Path(raw_files)
currentPattern = "*.mp4"
my_list = sorted(currentDirectory.glob(currentPattern), key=os.path.getsize, reverse=True)
logging.info(f'{len(my_list)} raw files found to encode. Starting encoding at {datetime.now()}')
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
