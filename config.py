from sys import platform
import requests
import json
import slugify


populars = ['Dredd', 'Emily Willis', 'Gabbie Carter', 'Ivana Sugar',
            'Joey White', 'Lady Zee', 'Liya Silver', 'Sami White', 'Sandra Zee', ]

tags_distro = {
    'fv':
    ['Dredd', 'Emily Willis', 'Gabbie Carter', 'Ivana Sugar', 'Joey White',
     'Lady Zee', 'Liya Silver', 'Sami White', 'Sandra Zee', ],
    'br':
    ['Francesca Le', 'Adria Rae', 'Adriana Chechik', 'Alison Tyler', 'Angela White', 'Ania Kinski', 'Anissa Kate', 'Anna De Ville', 'Anna Polina', 'Avil Love', 'Bella Rolland', 'Billie Star', 'Casey Calvert', 'Charlotte Sartre', 'Eliza Ibarra', 'Eliza Ibarra', 'Emily Willis', 'Franceska Jaimes',
     'Francys Belle', 'Holly Hendrix', 'Ivy Lebelle', 'Jane Wilde', 'Jasmine Jae', 'Jolee Love', 'Kira Noir', 'Lady Dee', 'Lady Gang', 'Lady Zee', 'Lana Rhoades', 'Lasirena69', 'Maddy May', 'Maria Visconti', 'Marley Brinx', 'Megan Rain', 'Monika Wild', 'Nicole Black', 'Nicole Love', 'Sandra Zee', 'Sasha Rose'],
    'bl':
    ['AJ Applegate', 'Angel Wicky', 'Blanche Bradburry', 'Brittany Bardot', 'Candice Dare', 'Cherie Deville', 'Cherry Kiss', 'Cory Chase', 'Dee Williams', 'Florane Russel', 'Haley Reed', 'Ivana Sugar', 'Jillian Janson', 'Kate England',
     'Kira Thorn', 'Kristy Black', 'Lola Taylor', 'London River', 'Manuela Rubi', 'Natalia Starr', 'Nathaly Cherie', 'Nikyta Rubi', 'Paige Owens', 'Phoenix Marie', 'Rebecca Volpetti', 'Rebel Rhyder', 'Ria Sunn', 'Samantha Rone', 'Selvaggia'],
    'bu':
        ['Alison Tyler', 'Angel Wicky', 'Angela White', 'Anissa Kate', 'Billie Star', 'Blanche Bradburry', 'Bridgette B', 'Brittany Bardot', 'Chloe Lamour', 'Dee Williams', 'Florane Russel', 'Francesca Le', 'Franceska Jaimes', 'Gabbie Carter', 'Ivy Lebelle', 'Jasmine Jae', 'Jasmine Jae',
            'Joanna Angel', 'Jolee Love', 'Keisha Grey', 'Kitana Lure', 'Lana Rhoades', 'Lasirena69', 'Lena Paul', 'Liya Silver', 'London River', 'Manuela Rubi', 'Maria Visconti', 'Nathaly Cherie', 'Nikyta Rubi', 'Phoenix Marie', 'Savannah Bond', 'Stella Cox', 'Taylee Wood', 'Veronica Avluv', ],
        'st':
        ['Adria Rae', 'AJ Applegate', 'AJ Applegate', 'Anna De Ville', 'Avi Love', 'Candice Dare', 'Casey Calvert', 'Charlotte Sartre', 'Charlotte Satre', 'Cherry Kiss', 'Emily Willis', 'Eveline Dellai', 'Francys Belle', 'Gia Derza', 'Haley Reed', 'Holly Hendrix', 'Holly Hendrix', 'Ivana Sugar', 'Ivana Sugar', 'Jane Wilde',
            'Jillian Janson', 'Kira Noir', 'Kira Thorn', 'Korra Del Rio', 'Kristy Black', 'Lady Dee', 'Lady Zee', 'Lola Taylor', 'Marley Brinx', 'Megan Rain', 'Monika Wild', 'Nicole Black', 'Paige Owens', 'Rebecca Volpetti', 'Riley Reid', 'Samantha Rone', 'Sandra Zee', 'Sasha Rose', 'Selvaggia', 'Silvia Dellai', ],
        'mi':
        ['Alison Tyler', 'Angel Wicky', 'Angela White', 'Ania Kinski', 'Anissa Kate', 'Blanche Bradburry', 'Bridgette B', 'Brittany Bardot', 'Cherie Deville', 'Cory Chase', 'Dee Williams',
            'Francesca Le', 'Jasmine Jae', 'Joanna Angel', 'Kitana Lure', 'Lauren Phillips', 'Lena Paul', 'London River', 'Nathaly Cherie', 'Phoenix Marie', 'Veronica Avluv', ],
        'uk': ['Candice Dare', 'Kate England', 'London River', 'Tina Kay', ],
        'fr': ['Ania Kinski', 'Anissa Kate', 'Anna Polina', 'Clea Gaultier', ],
        'ru': ['Cherry Kiss', 'Ivana Sugar', 'Kitana Lure', 'Lola Taylor', 'Maria Visconti', 'Natalia Starr', 'Sasha Rose'],
        'ss': ['Eveline Dellai', 'Joey White', 'Lady Zee', 'Manuela Rubi', 'Nikyta Rubi', 'Sami White', 'Sandra Zee', 'Silvia Dellai', ],
        'ts': ['Aubrey Kate', 'Chanel Santini', 'Daisy Taylor', 'Emma Rose', 'Korra Del Rio', ],
        'as': ['Alexis Tae', 'May Thai', ],
        'b': ['Ana Foxxx', 'Dredd', 'Kira Noir', 'Zaawaadi', ],
}

api_token = '95JaRiuNgWFw7UvpYgas7VpP6EV8VNEndjb0zO9z'
api_url_base = 'https://api.metadataapi.net/'
headers = {
    'Authorization': 'Bearer {0}'.format(api_token),
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def get_person_info(person_name):
    api_url = '{0}performers/{1}'.format(api_url_base, slugify.slugify(person_name))
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


if platform == 'win32' or platform == 'win64':
    all_files = 'X:\\Diziler\\Supergirl'
    raw_files = 'X:\\Diziler\\Legion'
elif platform == 'linux':
    all_files = '/home/noyana/Videos/.pro/favorites/'
    raw_files = '/home/noyana/Videos/.pro/download/'
