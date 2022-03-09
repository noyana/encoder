from sys import platform

populars = ['Emily Willis', 'Gabbie Carter', 'Muslim', 'Liya Silver', 'Joey White', 'Sami White', 'Ivana Sugar',
            'Lady Zee', 'Sandra Zee', 'Dredd']
if platform == 'win32' or platform == 'win64':
    all_files = 'X:\\Diziler\\Supergirl'
    raw_files = 'X:\\Diziler\\Legion'
elif platform == 'linux':
    all_files = '/home/noyana/Videos/.pro/favorites/'
    raw_files = '/home/noyana/Videos/.pro/download/'
