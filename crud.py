""" File for Create, Read, Update, Delete data (the CRUD). 
A CRUD file helps simplify the Flask route functions called in server.py. """

# The following is defined in model.py –
from model import db, connect_to_db, User, Phrase, Sentiment #Interaction, Interaction_type
from score import swn_polarity

from datetime import datetime
from random import choice, randint

# working as of 19 Feb 2021
def create_user(fname, lname, email, password, consent=False):
    """Create and return a new User object."""

    user = User(fname=fname, lname=lname, email=email, password=password, consent=False) # is consent default value added here as well as in arguments?

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_email(email):
    """Returns unique emails, i.e. the first occurence of any email."""
    user = User.query.filter_by(email=email).first()
    return user


# this one does not work yet; leaving it for now – 19 Feb 2021
def create_interaction(user, interaction_date):
    """Create and return a new Interaction object – this is an interaction with the server."""

    interaction = Interaction(user=interactions.user_id, interaction_date=interaction_date)

    db.session.add(interaction)
    db.session.commit()

    return interaction


# working in current form on 19 Feb 2021
def log_interaction_type(interactiontype_name):
    """Create and return a new Interaction_type object, 
       which is a new entry in the server interaction log."""

    interaction_type = Interaction_type(interactiontype_name=interactiontype_name)

    # Hypothesis on how to handle:
    # via Headers (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
        # Can track GET and POST and NEITHER.
        # GET can see if User GETs the final return of a display
        # POST can see if User logs in or sign up
        # POST can see if User enters a new phrase
        # Neither checks if the server has been queried ... ?
            # can see if the site is loaded without entering anything
 
###### NOTES FROM THU
# will need to look at headers and see what is returned in the request body
# find which header matches with which activity
# login, logout, posting a phrase, viewing phrase (get)
######
    db.session.add(interaction_type)
    db.session.commit()

    return interaction_type

    # "phrase_text"
    # "job_at_phrase"
    # "interaction_id", # this is which interview
    # "age_at_phrase"
    # "phrase_city"
    # "phrase_state_abbr"
    # "phrase_state"
    # "phrase_region"
    # "phrase_date"
    # "user_id"


# working on 07 Mar 2021
def create_phrase_and_score(phrase_date, phrase_city, phrase_state_abbr, phrase_state, phrase_region, job_at_phrase, age_at_phrase, phrase_text, user_id, US_or_no=True):
    """Create and return a new Phrase, which includes a '0' or '1' score."""
# open the csv in the seed_database.py, not here
# pass in a phrase that is string as argument
# phrase_date is a string of form %Y-%m-%d – ex. '2021-02-18'

    polar_score = swn_polarity(phrase_text)
    # test that the above works; it does 
    # print(f'Score is {polar_score}.')

    #make sure phrase has no trailing white space
    phrase_text = phrase_text.rstrip()

    # variable name from model.py in class Phrase = variable name used in this funct
    new_phrase_and_score = Phrase(phrase_date=phrase_date, US_or_no=True, phrase_city=phrase_city, phrase_state_abbr=phrase_state_abbr, phrase_state=phrase_state, phrase_region=phrase_region, job_at_phrase=job_at_phrase, age_at_phrase=age_at_phrase, phrase_text=phrase_text, polar_score=polar_score, user_id=user_id)

    db.session.add(new_phrase_and_score)
    db.session.commit()

    return new_phrase_and_score


def get_phrase_by_phrase_id(phrase_id):
    """Returns a particular phrase."""
    phrase = Phrase.query.filter_by(phrase_id=phrase_id).first()
    # How to write this with get? –
    # phrase = Phrase.query.get(phrase_id=phrase_id).one() 
    return phrase


def get_phrases_by_user_id(user_id):
    """Returns all of a single user's phrases."""
    phrases = Phrase.query.filter_by(user_id=user_id).all()
    return phrases



def get_phrase_collection():
    """Return entire phrase collection."""
    #return Phrase.query.all()
    return Phrase.query.all()


def get_a_few_phrases():
    """Return a random selection of 4 to 10 phrases."""
    
    random_phrases = []

    for n in range(randint(4, 10)):
        random_int = randint(1, len(Phrase.query.all()))    
        random_phrase = Phrase.query.filter_by(phrase_id=random_int).one()
        if random_phrase not in random_phrases:
            random_phrases.append(random_phrase)
        else:
            continue    
    return random_phrases


def get_a_few_phrases_by_region(phrase_text=None):
    """Return a random selection of 4 phrases from a region."""

    random_phrases_for_region = []
    
    # get the Phrase object belonging to the text
    if phrase_text != None:
        phrase_object = Phrase.query.filter_by(phrase_text=phrase_text).first() 
        random_phrases_for_region.append(phrase_object)
        sort_region = phrase_object.phrase_region
        phrases_from_region = Phrase.query.filter_by(phrase_region=sort_region).all()
    
    # if no phrase_text supplied, choose a region at random
    else:
        sort_region = choice(['Pacific', 'West', 'Midwest','Mid-Atlantic', 'Southeast', 'New England', 'Territories'])
        phrases_from_region = Phrase.query.filter_by(phrase_region=sort_region).all()    
    
    # return a list of non-repeating Phrases from the region
    while len(random_phrases_for_region) < 4: # break the loop when count is 4
        random_index = (randint(0, (len(phrases_from_region)-1)))
        if phrases_from_region[random_index] not in random_phrases_for_region:
            random_phrases_for_region.append(phrases_from_region[random_index])
        else:
            continue # this code is not strictly necessary    

    return random_phrases_for_region


def get_one_phrase_per_region_unless_given(given_region=None):
    """Return a phrase for each region, but skip a given region if provided."""

    one_phrase_per_region = []
    region_list = ['Pacific', 'West', 'Midwest','Mid-Atlantic', 'Southeast', 'New England', 'Territories']
    
    for one_region in region_list:  
        if one_region == given_region:
            continue
        phrases_for_one_region = Phrase.query.filter_by(phrase_region=one_region).all()
        if len(phrases_for_one_region) > 1:
            random_index = (randint(0, (len(phrases_for_one_region)-1)))  
            one_phrase_per_region.append(phrases_for_one_region[random_index])     
        elif len(phrases_for_one_region) == 1:
            one_phrase_per_region.append(phrases_for_one_region)
        else:
            continue    
    return one_phrase_per_region


def get_a_or_an(job):
    """Use 'a' or 'an' before a job title."""
    
    vowels = ['a', 'e', 'i', 'o', 'u']
    capitals = ['F','H','M','N','R','S','X']
    
    job_object = Phrase.query.filter_by(job_at_phrase=job).first()
    job = job_object.job_at_phrase
    if (job[0]) in vowels:
        return 'an'
    elif (job[0]) in capitals: # I am not certain this line works
        return 'an'
    else:
        return 'a'



# working on 19 Feb 2021
def create_sentiment(tone):
    """Create and return a new Sentiment object."""

    sentiment = Sentiment(tone=tone)

    db.session.add(sentiment)
    db.session.commit()

    return sentiment


# Copy-paste this into crud.py each time, too – 
# it is to connect interactively to the database in order to test functions.

if __name__ == '__main__':
    from server import app
    connect_to_db(app)