from sys import platform

populars = ['Emily Willis', 'Gabbie Carter', 'Muslim', 'Liya Silver', 'Joey White', 'Sami White', 'Ivana Sugar',
            'Lady Zee', 'Sandra Zee', 'Dredd']
if platform == 'win32' or platform == 'win64':
    video_paths_dict = {'ordinary': 'X:\\Diziler\\Vikings\\', 'lbqtq': 'X:\\Diziler\\The Gifted\\',
                        'movie': 'X:\\Diziler\\Criminal Minds\\', 'unpopular': 'X:\\Diziler\\Doctor Who\\',
                        'favorite': 'X:\\Diziler\\Supergirl\\'}
    video_paths = ['X:\\Diziler\\Vikings\\', 'X:\\Diziler\\The Gifted\\', 'X:\\Diziler\\Criminal Minds\\',
                   'X:\\Diziler\\Doctor Who\\', 'X:\\Diziler\\Supergirl\\']
    raw_files = 'X:\\Diziler\\Legion\\'

elif platform == 'linux':
    video_paths_dict = {'favorite': '/home/noyana/Videos/.pro/favorites/', 'ordinary': '/home/noyana/Videos/.pro/ordinary',
                        'lbgtq': '/home/noyana/Videos/.pro/lgbtq/', 'unpopular': '/home/noyana/Videos/.pro/unpopular/',
                        'movie': '/home/noyana/Videos/.pro/movies/'}
    video_paths = ['/home/noyana/Videos/.pro/favorites/', '/home/noyana/Videos/.pro/ordinary', '/home/noyana/Videos/.pro/lgbtq/',
                   '/home/noyana/Videos/.pro/unpopular/', '/home/noyana/Videos/.pro/movies/']
    raw_files = '/home/noyana/Videos/.pro/download/'
