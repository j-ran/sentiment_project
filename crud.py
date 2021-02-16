""" File for Create, Read, Update, Delete data (the CRUD). 
A CRUD file helps simplify the Flask route functions called in server.py. """

# The following is defined in model.py –
from model import db, connect_to_db,
                  User, 
                  Interaction, 
                  Interaction_type, 
                  Phrase, 
                  Sentiment, 
                  Score



def create_user(fname, lname, email, password, consent=False):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password, consent=False) # is consent default value added here as well as in arguments?

    db.session.add(user)
    db.session.commit()

    return user


def create_interaction(user, interaction_date):
    """Create and return a new interaction with the server."""
# How to identify the user – with user_id? Do I list that as passed in?
# QUESTION: Can I auto-log interaction date without passing it in as "interaction_date"?
# not really sure from how to get this info ...
    interaction = Interaction(user=users.user_id, interaction_date=interaction_date)
    db.session.add(interaction)
    db.session.commit()

    return interaction


def log_interaction_type(interactiontype_name):
    """Create and return a new entry in the server interaction log."""

    interactiontype = Interaction_type(interactiontype_name=interactiontype_name)
# I want to make four interaction types ONLY. How do I do this?
# I think they are Booleans.
# signup; login; phrase_added; seed_interview_J; seed_interview_K  

#####
# will need to look at headers and see what is returned in the request body
# find which header matches with which activity
# login, logout, posting a phrase, viewing phrase (get)
######
    db.session.add(interaction_type)
    db.session.commit()

    return interaction_type
   

def create_phrase(pass in a phrase from my current .csv)
    """Create and return a new phrase."""
# open the csv in the seeddatabase.py, not here
# pass in a phrase that is string as argument


def create_sentiment(...)
    """Create and return a new sentiment."""
# I don't think this is right ...
# no, do it in seeddatbase -- tone and keywords


def create_score(all the arguments needed for a score, including a Sentiment class)
    """Create and return a new score for a phrase."""
#


# Copy-paste this into crud.py each time, too – 
# it is to connect interactively to the database in order to test functions.

if __name__ == '__main__':
    from server import app
    connect_to_db(app)