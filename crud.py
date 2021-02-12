""" File for Create, Read, Update, Delete data (the CRUD). 
A CRUD file helps simplify the Flask route functions called in server.py. """

# The following is defined in model.py –
from model import db, connect_to_db, User, Interaction, Interaction_type, Phrase, Score, Sentiment
# if you import Sentiment, it is for a backref to Score



def create_user(fname, lname, email, password, consent=False):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password, consent=False) # is consent default value added here as well as in arguments?

    db.session.add(user)
    db.session.commit()

    return user



def create_interaction(user, interaction_date):
    """Create and return a new interaction with the server."""

    interaction = Interaction(user=users.user_id, interaction_date=interaction_date)

    db.session.add(interaction)
    db.session.commit()

    return interaction



def log_interaction_type(interactiontype_name):
    """Create and return a new entry in the server interaction log."""

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
   


def create_phrase(phrase):
    """Create and return a new phrase."""
# open the csv in the seed_database.py, not here
# pass in a phrase that is string as argument
    new_phrase = Phrase(phrase=phrase_text)

    db.session.add(new_phrase)
    db.session.commit()

    return new_phrase



def create_score(phrase):
    """Create and return a new score for a phrase."""
#
    # input phrase
    # run the parts of the phrase through a function
    # that is part of spaCy library
    # return score

    new_score = Score(phrase=phrase_text)
    
    # 'analyze_text_with_syntax_and_weight' function from spaCy
    # return an Integer
    # assign to variable 'new_score'

    db.session.add(new_score)
    db.session.commit()

    return new_score



# def create_sentiment(tone)
#     """Create and return a new sentiment."""
## This is done in seed_database with tone and keywords, not here



# Copy-paste this into crud.py each time, too – 
# it is to connect interactively to the database in order to test functions.

if __name__ == '__main__':
    from server import app
    connect_to_db(app)