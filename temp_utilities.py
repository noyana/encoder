from datetime import datetime
from config import *
from models import *
from tqdm import tqdm
from sqlalchemy.orm import Session, session
from sqlalchemy.ext.automap import automap_base
import sqlalchemy as db
import sqlite3database
import os
import re
import json
import requests
import slugify


Base = automap_base()
engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files.sqlite3")
Base.prepare(engine, reflect=True)
maintain_session = Session(engine)

""
for raw_file in tqdm(sorted(os.scandir(all_files), key=os.path.getmtime, reverse=False)):
    # print(raw_file.path)
    (new_name, new_tags, new_file_count, new_people, new_is_movie) = Video.get_video_info(raw_file.path)
    org_name = new_name
    org_tags = new_tags.copy()
    org_people = new_people.copy()

    if (not 'a' in new_tags) and (not 'na' in new_tags):
        new_tags.append('a')

    for fv in new_people:
        for my_key, my_list in tags_distro.items():
            if fv in my_list and not my_key in new_tags:
                new_tags.append(my_key)
    new_tags = list(set(new_tags))
    new_tags.sort()
    newest_name = Video.name_sort(new_name, new_tags, new_file_count, new_people, new_is_movie)
    os.rename(raw_file.path, f"{all_files}{os.path.sep}{newest_name}")

# if person.name in my_list and not my_key in person.default_tags.split(','):
##        person.default_tags += ',' + my_key
# maintain_session.commit()

"""
fn_bare = "No Ay.mp4"
fn_num = "No Ay,(10).mp4"
fn_numw = "No Ay (11).mp4"
fn_tag = "No Ay,#(a).mp4"
fn_tags = "No Ay,#(a,s).mp4"
fn_tagw = "No Ay #(w).mp4"
fn_tagsw = "No Ay #(w,s).mp4"
fn_full = "No Ay,#(f),(12).mp4"
fn_fuls = "No Ay,#(f,s),(13).mp4"

mn_num = "Bu Ay,No Ay,(10).mp4"
mn_numw = "Bu Ay,No Ay (11).mp4"
mn_tag = "Bu Ay,No Ay,#(a).mp4"
mn_tags = "Bu Ay,No Ay,#(a,s).mp4"
mn_tagw = "Bu Ay,No Ay #(w).mp4"
mn_tagsw = "Bu Ay,No Ay #(w,s).mp4"
mn_full = "Bu Ay,No Ay,#(f),(12).mp4"
mn_fuls = "Bu Ay,No Ay,#(f,s),(13).mp4"


def gc(fn):
    name = ""
    tags = []
    count = 1
    is_movie = None
    people = []
    name = fn.split('#')
    if len(name) > 1:
        cstr = re.search("\((\d+)\).mp4", fn)
        if cstr:
            count = int(cstr[1])
        else:
            count = 1
        tag_str = name[1].replace('.mp4', '')
        for tag in re.findall("(?:([a-z]{1,3}),*)", tag_str):
            tags += tag
        name = name[0]
    else:
        cstr = re.search("\((\d+)\).mp4", fn)
        if cstr:
            count = int(cstr[1])
            name = fn.replace(cstr[0], '').strip().rstrip(',')
        else:
            count = 1
            name = name[0].strip()
    if re.search(".mp4", name):
        name = name.replace('.mp4', '').strip()
    if not 'm' in tags:
        people = name.split(',')
        is_movie = False
    else:
        is_movie = True
    return (name, tags, count, people, is_movie)

print(f"{fn_bare} -> {gc(fn_bare)}")
print(f"{fn_num} -> {gc(fn_num)}")
print(f"{fn_numw} -> {gc(fn_numw)}")
print(f"{fn_tag} -> {gc(fn_tag)}")
print(f"{fn_tags} -> {gc(fn_tags)}")
print(f"{fn_tagsw} -> {gc(fn_tagsw)}")
print(f"{fn_full} -> {gc(fn_full)}")
print(f"{fn_fuls} -> {gc(fn_fuls)}")

print(f"{mn_num} -> {gc(mn_num)}")
print(f"{mn_numw} -> {gc(mn_numw)}")
print(f"{mn_tag} -> {gc(mn_tag)}")
print(f"{mn_tags} -> {gc(mn_tags)}")
print(f"{mn_tagsw} -> {gc(mn_tagsw)}")
print(f"{mn_full} -> {gc(mn_full)}")
print(f"{mn_fuls} -> {gc(mn_fuls)}")
"""
