import sqlite3database
import sqlalchemy as db
import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session

Base = automap_base()

engine = db.create_engine("sqlite:///files.sqlite3")

Base.prepare(engine, reflect=True)
Video = Base.classes.videos
Person = Base.classes.people

session = Session(engine)

video1 = session.query(Video).first()

for video in session.query(Video).all():
    video.file_name = video.file_name.replace('P:/Diziler/', 'W:/Diziler/')
    video.file_name = video.file_name.replace('X:/Diziler/', 'W:/Diziler/')
    session.commit()
