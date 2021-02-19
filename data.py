""" Seed Data from We Respond 2020 
Collected by Janaki Ranpura in collaboration with artist Katherine Wilkinson.
Side note: a useful how-to on CSV in Python at 
info at https://careerkarma.com/blog/python-csv-module/
"""

from random import choice, randint
import csv


def create_phrase_statement(csv_filename):
    dict = {}
    printed_phrases = []


    with open(csv_filename, "r") as f:
        contents = csv.reader(f)
        # return the right data (for now, only the phrase [index 2] and the kind of person who said it [index 3])

        for row in contents:
            # this way of writing a dictionary means
            # what's on the left is the key
            # and what's on the right is 'values'
            dict[row[2]] = row[3]

        #v.1 – print all phrases 
        for phrase_id, (phrase, person) in enumerate(dict.items()):
            print(f'{phrase_id} – A {person} said, "{phrase}"')
        # -- end v.1


        # v.2 – print random choice of phrases   
        # for phrase_id, (phrase, person) in enumerate(dict.items()):  
        #     a_phrase = (f'{phrase_id} – A {person} said, "{phrase}"')
        #     printed_phrases.append(a_phrase)
            
        # for n in range(randint(3, 10)):
        #      print('\n***')
        #      print(choice(printed_phrases))
        # -- end v.2


        # v.3 – Improve grammar and look
        #       of random printed phrases   
        vowels = ['a', 'e', 'i', 'o', 'u']
        capitals = ['F','H','M','N','R','S','X']
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
        # -- end v.3  


        # ALT v.1: to list number and list phrases
        # need to declare 'i = 0' at top of funx
        # for phrase, person in (dict.items()):
        #     i = i + 1
        #     print(f'{i} – A {person} said, "{phrase}"')  
        # If this method used, phrases will start at '1'.  
    
    #return dict


# TEST THE FUNCTION
create_phrase_statement("werespond_quotes02.csv")
#print(create_phrase_statement("werespond_quotes02.csv"))