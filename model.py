"""Model for We Respond Sentiment Scoring project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# QUESTION: do I import my language modules here, too? Such as __ .

db = SQLAlchemy()


# Six Classes in the Model –
# User, Interaction, Interaction_type, Phrase, Sentiment, Score

# I have a few possible Inherited Classes to create ...
# In the commments for Backrefs, is it correct what I said? Are they "ghost" references to a TABLE or to a CLASS? Are they a "list" or a "table" or an "attribute"?


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(15))
    lname = db.Column(db.String(15))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(30))
    consent = db.Column(db.Boolean, default=False)

    # TWO BACKREFS HERE –
    # interactions = a list of Interaction objects 
    # accessible through the User class (which is this Class)

    # phrases = a list of Phrase objects 
    # accessible through the User class (which is this Class)

    def __repr__(self):
        return f'<User user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email}>'



class Interaction(db.Model):
    """Audit of interactions with the db."""
    # -- maybe call this "log" or "audit"
    
    __tablename__ = "interactions"

    interaction_id = db.Column(db.Integer, 
                               autoincrement=True, 
                               primary_key=True)
    interaction_date = db.Column(db.DateTime) # QUESTION - just 'Date'?

    # Using two Foreign Keys and two backrefs
    interactiontype_id = db.Column(db.Integer, 
                         db.ForeignKey('interaction_types.interactiontype_id'))
    user_id = db.Column(db.Integer,
              db.ForeignKey('users.user_id')) 
    # Add a note in the referenced Class about this table
    interaction_type = db.relationship('Interaction_type', backref='interactions')  
    user = db.relationship('User', backref='interactions')

    # phrases = a list of Phrase objects 
    # accessible through the Interaction class (which is this Class)

    def __repr__(self):
        return f'<Interaction interaction_id={self.interaction_id} date={self.interaction_date}>'



class Interaction_type(db.Model):
    """A record of the type of interaction."""

    __tablename__ = "interaction_types"

    interactiontype_id = db.Column(db.Integer, 
                                   autoincrement=True, 
                                   primary_key=True)
    interactiontype_name = db.Column(db.str)

    # interactions = a list of Interaction objects 
    # accessible through the Interaction_type Class (which is this Class)

    # phrases = a list of Phrase objects 
    # accessible through the Interaction_type Class (which is this Class)

    def __repr__(self):
         return f'<Interaction_type interactiontype_id={self.interactiontype_id} interactiontype_name={self.interactiontype_name}>'

# I BELIEVE THIS CLASS NEEDS A CHILD CLASS FOR EACH TYPE OF INTERACTION. IS THAT A GOOD IDEA?

##### NO INTEGER ID, but give it a name (a unique string). -- No, actually leave it.



class Phrase(db.Model):
    """User input saved as Phrase."""
    
    __tablename__ = "phrases"

    phrase_id = db.Column(db.Integer, 
                               autoincrement=True, 
                               primary_key=True)
    phrase_date = db.Column(db.DateTime) # QUESTION - just 'Date'?
    
    # the following three attributes relate to location
    # I have decided to do US locations only.
    US_or_no = db.Column(db.Boolean, default=True)
    phrase_city = db.Column(db.String(20))
    phrase_state = db.Column(db.String(2))
    
    job_at_phrase = db.Column(db.String(20))
    age_at_phrase = db.Column(db.Integer(3)) #how to specify the limits on this field? Is this correct ... does it mean the largest age =< 1000?
    phrase_text = db.Column(db.String(120))                                    

    # Using three Foreign Keys and three backrefs
    interaction_id = db.Column(db.Integer, 
                     db.ForeignKey('interactions.interaction_id'))
    user_id = db.Column(db.Integer,
              db.ForeignKey('users.user_id')) 
    score_id = db.Column(db.Integer,
               db.ForeignKey('scores.score_id'))  
               # nullable            
    # Add a note in the referenced Class about this table
    phrase_interaction = db.relationship('Interaction', backref='phrases')
    phrase_user = db.relationship('User', backref='phrases')
    phrase_score = db.relationship('Score', backref='phrases')  

    def __repr__(self):
        return f'<Phrase phrase_id={self.phrase_id} phrase_text={self.phrase_text}>'



class Sentiment(db.Model):
    """A Sentiment."""

    __tablename__ = "sentiments"

    sentiment_id = db.Column(db.Integer, 
                               autoincrement=True, 
                               primary_key=True)
    # tone (i.e, name); not yet complete
    tone = db.Column(db.String)
    # keywords – this is either going to come from CSV or API.
    # (standford web project csv, or SentiNet API) 
    # need to determine
    keywords = db.Column(db.String)
    
    # Then ... subclasses, like 'anger', 'fear', 'joy', etc.?
    # Each subclass has a score range, like 0-10, 11-20, etc.?

    # scores = a list of Score objects 
    # accessible through the Sentiment Class (which is this Class) 

    def __repr__(self):
        return f'<Sentiment sentiment_id={self.sentiment_id} tone={self.tone} keywords={self.keywords}>'


class Score(db.Model):
    """A Score for a phrase."""    

    __tablename__ = "scores"

    score_id = db.Column(db.Integer, 
                         autoincrement=True, 
                         primary_key=True)

    # Using two Foreign Keys, 
    # one new backref (sentiment_score)
    # and one establshed backref (phrases)
    phrase_id = db.Column(db.Integer, 
                db.ForeignKey('phrases.phrase_id'))
    sentiment_id = db.Column(db.Integer,
                   db.ForeignKey('sentiments.sentiment_id')) 
    
    # Backrefs  
    sentiment_score = db.relationship('Sentiment', backref='scores')

    # phrases = a list of Phrase objects 
    # accessible through the Score Class (which is this Class)        

    def __repr__(self):
        return f'<Score score_id={self.score_id}>'


# For testing, you will want to change the postgresql database
# to a 'testdb' instead of 'db_uri'

def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = True   
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to J's Sentiments db!")


if __name__ == '__main__':
    from server import app


    connect_to_db(app)