import os
import re

import sqlite3database
import sqlalchemy as db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from tqdm import tqdm
from models import *
from config import *

Base = automap_base()
engine = db.create_engine("sqlite:///C:\\Users\\noyana\\source\\repos\\encoder\\files.sqlite3")
Base.prepare(engine, reflect=True)
session = Session(engine)

my_list = sorted(os.scandir(all_files), key=os.path.getmtime, reverse=False)
for raw_file in tqdm(my_list):
    # print(raw_file.path)
    (new_name, new_tags, new_file_count, new_people, new_is_movie) = Video.get_video_info(raw_file.path)
    org_name = new_name
    org_tags = new_tags.copy()
    org_people = new_people.copy()

    if (not 'a' in new_tags) and (not 'na' in new_tags):
        new_tags.append('a')

    if re.search('Muslim', new_name) and not 'mu' in new_tags:
        new_tags.append('mu')
    elif (re.search('Dredd', new_name) or re.search('Ana Foxxx', new_name) or re.search('Zaawaadi', new_name) or re.search('Kira Noir', new_name)) and not 'b' in new_tags:
        new_tags.append('b')
    elif (re.search('Dredd', new_name)) and not 'bbc' in new_tags:
        new_tags.append('bbc')
    elif (re.search('Thai', new_name) or re.search('Alexis Tae', new_name)) and not 'as' in new_tags:
        new_tags.append('as')
    elif (re.search('Dellai', new_name) or re.search('Twin', new_name) or re.search(' Zee', new_name) or re.search('Joey White', new_name) or re.search('Sami White', new_name)) and not ('tw' in new_tags or 'ss' in new_tags):
        new_tags.append('tw')
        new_tags.append('ss')
    elif (not re.search('Dredd', new_name)) and len(new_people) == 2 and not 'ffm' in new_tags:
        new_tags.append('ffm')
    elif (not re.search('Dredd', new_name)) and len(new_people) == 3 and not 'gr' in new_tags:
        new_tags.append('gr')
    elif re.search('TS ', new_name) and not 'ts' in new_tags:
        new_tags.append('ts')
        new_name.replace('TS ', '')
    elif re.search('Bi ', new_name) and not 'bi' in new_tags:
        new_tags.append('bi')
    for fv in new_people:
        if fv in populars and not 'fv' in new_tags:
            new_tags.append('fv')
        if fv in ['Angela White', 'Angel Wicky', 'Lena Paul', 'Gabbie Carter', 'Savannah Bond', 'Joanna Angel', 'Kitana Lure', 'Phoenix Marie', 'Alison Tyler', 'Anissa Kate', 'Blanche Bradburry', 'Bridgette B', 'Ivy Lebelle', 'Jasmine Jae', 'Jolee Love', 'Lasirena69', 'Stella Cox', 'Taylee Wood', 'Veronica Avluv'] and not 'bu' in new_tags:
            new_tags.append('bu')
        if fv in ['Angela White', 'Angel Wicky', 'Lena Paul', 'Joanna Angel', 'Kitana Lure', 'Phoenix Marie', 'Alison Tyler', 'Anissa Kate', 'Blanche Bradburry', 'Bridgette B', 'Jasmine Jae', 'Veronica Avluv'] and not 'mi' in new_tags:
            new_tags.append('mi')
        if fv in ['Megan Rain', 'Marley Brinx', 'Charlotte Satre', 'Cherry Kiss', 'Adria Rae', 'AJ Applegate', 'Samantha Rone', 'Emily Willis', 'Eveline Dellai', 'Silvia Dellai', 'Gia Derza', 'Holly Hendrix', 'Ivana Sugar', 'Riley Reid', 'Selvaggia'] and not 'st' in new_tags:
            new_tags.append('st')
        if fv in ['Anissa Kate', 'Anna Polina', 'Clea Gaultier'] and not 'fr' in new_tags:
            new_tags.append('fr')
        if fv in ['Tina Kay'] and not 'uk' in new_tags:
            new_tags.append('uk')
        if fv in ['Emily Willis', 'Angela White', 'Jolee Love', 'Marley Brinx', 'Megan Rain'] and not 'br' in new_tags:
            new_tags.append('br')
        if fv in ['Angela White', 'Jolee Love'] and not 'br' in new_tags:
            new_tags.append('br')
    new_tags = list(set(new_tags))
    new_tags.sort()
    # if new_people != org_people or new_tags != org_tags or new_name != org_name:
    if True:
        newest_name = Video.name_sort(new_name, new_tags, new_file_count, new_people, new_is_movie)
        os.rename(raw_file.path, f"{all_files}{os.path.sep}{newest_name}")

for person in tqdm(session.query(Person).all()):
    if person.name in ['Emily Willis', 'Angela White', 'Jolee Love', 'Marley Brinx', 'Megan Rain', 'Adriana Chechik', 'Adria Rae', 'Alison Tyler', 'Anissa Kate', 'Ania Kinski', 'Anna De Ville', 'Anna Polina', 'Avil Love', 'Bella Rolland', 'Billie Star', 'Eliza Ibarra', 'Casey Calvert', 'Charlotte Sartre', 'Eliza Ibarra', 'Francesca Le', 'Franceska Jaimes', 'Francys Belle', 'Holly Hendrix', 'Ivy Lebelle', 'Jane Wilde', 'Jasmine Jae', 'Kira Noir', 'Lady Dee', 'Lady Gang', 'Lana Rhoades', 'Lasirena69', 'Maddy May', 'Maria Visconti', 'Monika Wild', 'Nicole Black', 'Nicole Love', 'Sandra Zee', 'Lady Zee', 'Sasha Rose'] and not 'br' in person.default_tags:
        person.default_tags.append('br')
    if person.name in ['AJ Applegate', 'Angel Wicky', 'Blanche Bradburry', 'Brittany Bardot', 'Candice Dare', 'Cherie Deville', 'Cherry Kiss', 'Cory Chase', 'Dee Williams', 'Florane Russel', 'Haley Reed', 'Ivana Sugar', 'Jillian Janson', 'Kate England', 'Kira Thorn', 'Kristy Black', 'Lola Taylor', 'London River', 'Manuela Rubi', 'Nikyta Rubi', 'Natalia Starr', 'Nathaly Cherie', 'Paige Owens', 'Phoenix Marie', 'Rebecca Volpetti', 'Rebel Rhyder', 'Ria Sunn', 'Samantha Rone', 'Selvaggia'] and not 'bl' in person.default_tags:
        person.default_tags.append('bl')
    if person.name in ['Dredd'] and not 'bbc' in person.default_tags:
        person.default_tags.append('bbc')
    if person.name in ['Tina Kay', 'Candice Dare', 'Kate England', 'London River'] and not 'uk' in person.default_tags:
        person.default_tags.append('uk')
    if person.name in populars and not 'fv' in person.default_tags:
        person.default_tags.append('fv')
    if person.name in ['Angela White', 'Angel Wicky', 'Lena Paul', 'Gabbie Carter', 'Savannah Bond', 'Joanna Angel', 'Kitana Lure', 'Phoenix Marie', 'Alison Tyler', 'Anissa Kate', 'Blanche Bradburry', 'Bridgette B', 'Ivy Lebelle', 'Jasmine Jae', 'Jolee Love', 'Lasirena69', 'Stella Cox', 'Taylee Wood', 'Veronica Avluv', 'Billie Star', 'Brittany Bardot', 'Dee Williams', 'Chloe Lamour', 'Florane Russel', 'Francesca Le', 'Franceska Jaimes', 'Jasmine Jae', 'Keisha Grey', 'Lana Rhoades', 'Liya Silver', 'London River', 'Manuela Rubi', 'Nikyta Rubi', 'Maria Visconti', 'Nathaly Cherie'] and not 'bu' in person.default_tags:
        person.default_tags.append('bu')
    if person.name in ['Angela White', 'Angel Wicky', 'Lena Paul', 'Joanna Angel', 'Kitana Lure', 'Phoenix Marie', 'Alison Tyler', 'Anissa Kate', 'Blanche Bradburry', 'Bridgette B', 'Jasmine Jae', 'Veronica Avluv', 'Ania Kinski', 'Brittany Bardot', 'Cherie Deville', 'Cory Chase', 'Dee Williams', 'Francesca Le', 'Lauren Phillips', 'London River', 'Nathaly Cherie'] and not 'mi' in person.default_tags:
        person.default_tags.append('mi')
    if person.name in ['Megan Rain', 'Marley Brinx', 'Charlotte Satre', 'Cherry Kiss', 'Adria Rae', 'AJ Applegate', 'Samantha Rone', 'Emily Willis', 'Eveline Dellai', 'Silvia Dellai', 'Gia Derza', 'Holly Hendrix', 'Ivana Sugar', 'Riley Reid', 'Selvaggia', 'AJ Applegate', 'Anna De Ville', 'Avi Love', 'Candice Dare', 'Casey Calvert', 'Charlotte Sartre', 'Francys Belle', 'Haley Reed', 'Holly Hendrix', 'Ivana Sugar', 'Jane Wilde', 'Jillian Janson', 'Kira Noir', 'Kira Thorn', 'Korra Del Rio', 'Kristy Black', 'Lady Dee', 'Lola Taylor', 'Monika Wild', 'Nicole Black', 'Paige Owens', 'Rebecca Volpetti', 'Sandra Zee', 'Lady Zee', 'Sasha Rose', 'Selvaggia'] and not 'st' in person.default_tags:
        person.default_tags.append('st')
    if person.name in ['Anissa Kate', 'Anna Polina', 'Clea Gaultier', 'Ania Kinski'] and not 'fr' in person.default_tags:
        person.default_tags.append('fr')
    if person.name in ['Cherry Kiss', 'Kitana Lure', 'Ivana Sugar', 'Lola Taylor', 'Maria Visconti', 'Natalia Starr', 'Sasha Rose'] and not 'ru' in person.default_tags:
        person.default_tags.append('ru')
    if person.name in ['Eveline Dellai', 'Silvia Dellai', 'Joey White', 'Sami White', 'Sandra Zee', 'Lady Zee', 'Manuela Rubi', 'Nikyta Rubi'] and not 'ss' in person.default_tags:
        person.default_tags.append('ss')
    if person.name in ['Korra Del Rio', 'Aubrey Kate', 'Chanel Santini', 'Daisy Taylor', 'Emma Rose'] and not 'ts' in person.default_tags:
        person.default_tags.append('ts')
session.commit()

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
