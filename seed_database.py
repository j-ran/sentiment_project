"""This file is takes information from a csv and adds it to the database in order to seed the database."""

# pip3 freeze a requirements.txt for these imports
import os
import json 
from random import choice, randint # double-check if I actually call this
from datetime import date, datetime # not sure I will call 'date'; I can parse 'datetime'

##
# notes on datetime
# >>> date_str1 = "February 18, 2021"
# >>> format1 = "%B %d, %Y"
# >>> date_formatted = datetime.strptime(date_str1, format1)
##

import crud
import model
import server

os.system('dropdb phrases')
os.system('createdb phrases')

model.connect_to_db(server.app)
model.db.create_all()


csv_filepath = "werespond_quotes02.csv"


def read_in_csv(csv_filepath):
    """Access the csv that contains the starting data and read it into the db using a function, in case the file path of the csv changes"""

    with open(csv_filepath, "r") as f:
        initial_interviews = csv.reader(f)
        

def make_sentence(read_in_csv): #### is it okay to use this function as an argument?        
    """Return a sentence that verifies the data."""

    dict = {}
    printed_phrases = []            
    vowels = ['a', 'e', 'i', 'o', 'u']
    capitals = ['F','H','M','N','R','S','X']

    for row in initial_interviews:
    # This way of writing a dictionary means
    # what's on the left is 'key'
    # and what's on the right is 'values'.
    # Return the right data – 
    # for now, only the phrase [index 2] 
    # and the kind of person who said it [index 3]
        dict[row[2]] = row[3]

    for phrase, person in dict.items():  
        if person[0:1] not in vowels and capitals:
            a_phrase = (f'A {person} said, "{phrase}"')
            printed_phrases.append(a_phrase)
        else:
            a_phrase = (f'An {person} said, "{phrase}"')
            printed_phrases.append(a_phrase)

    for n in range(randint(3, 10)):
        print('\n******')
        print(choice(printed_phrases))
        # NB -- need to add that as soon as a phrase is chosen
        # it cannot be chosen again             


read_in_csv(csv_filepath)
make_sentence(read_in_csv)        