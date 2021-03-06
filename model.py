"""Model for We Respond Sentiment Scoring project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
# NB – SQLAlchemy is creating a database out of the commands in this file.


# Five Classes in the Model –
# User, Interaction, Interaction_type, Phrase, Sentiment


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(30))
    consent = db.Column(db.Boolean, default=False)

    # TWO BACKREFS HERE –
    # interactions = a property from class Interaction 
    # accessible through the User class (which is this Class)

    # phrases = a property from class Phrase 
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
    interaction_date = db.Column(db.DateTime)

    # Using two Foreign Keys and two backrefs
    interactiontype_id = db.Column(db.Integer, 
                         db.ForeignKey('interaction_types.interactiontype_id'))
    user_id = db.Column(db.Integer,
              db.ForeignKey('users.user_id')) 
    # Add a note in the referenced Class about this table
    interaction_type = db.relationship('Interaction_type', backref='interactions')  
    user = db.relationship('User', backref='interactions')

    # phrases = a property from class Phrase 
    # accessible through the Interaction class (which is this Class)

    def __repr__(self):
        return f'<Interaction interaction_id={self.interaction_id} date={self.interaction_date}>'



class Interaction_type(db.Model):
    """A record of the type of interaction using an id and a name."""

    __tablename__ = "interaction_types"

    interactiontype_id = db.Column(db.Integer, 
                                   autoincrement=True, 
                                   primary_key=True)
    interactiontype_name = db.Column(db.String)

    # interactions = a property from class Interaction 
    # accessible through the Interaction_type Class (which is this Class)

    # phrases = a property from class Phrase 
    # accessible through the Interaction_type Class (which is this Class)

    def __repr__(self):
         return f'<Interaction_type interactiontype_id={self.interactiontype_id} interactiontype_name={self.interactiontype_name}>'


class Phrase(db.Model):
    """User input saved as Phrase."""
    
    __tablename__ = "phrases"

    phrase_id = db.Column(db.Integer, 
                          autoincrement=True, 
                          primary_key=True)
    # datetime is form %Y-%m-%d – ex. '2021-02-18' incl quotes                         
    phrase_date = db.Column(db.String)
    
    # the following three attributes relate to location –
    US_or_no = db.Column(db.Boolean, default=True)
    phrase_city = db.Column(db.String(40))
    phrase_state_abbr = db.Column(db.String(3))
    phrase_state = db.Column(db.String(40))
    phrase_region = db.Column(db.String(20))
    job_at_phrase = db.Column(db.String(20))
    age_at_phrase = db.Column(db.Integer)
    phrase_text = db.Column(db.String(140))                                    

    polar_score = db.Column(db.Integer,
                            nullable=True) # this is nullable so that phrase can be entered before score exists

    # Using two Foreign Keys and two backrefs
    interaction_id = db.Column(db.Integer, 
                     db.ForeignKey('interactions.interaction_id'))
    user_id = db.Column(db.Integer,
              db.ForeignKey('users.user_id'))              
    
    # Add a note in the referenced Class about this table
    phrase_interaction = db.relationship('Interaction', backref='phrases')
    phrase_user = db.relationship('User', backref='phrases')

    def __repr__(self):
        return f'<Phrase phrase_id={self.phrase_id} phrase_text={self.phrase_text}>'



class Sentiment(db.Model):
    """A Sentiment."""

    __tablename__ = "sentiments"

    sentiment_id = db.Column(db.Integer, 
                               autoincrement=True, 
                               primary_key=True)
    # tones will be from Ekman; on 18 Feb 2021 just '0' and '1'
    # Ekman: 'anger', 'fear', 'sadness', 'disgust', 'surprise', 'contempt', 'enjoyment'
    tone = db.Column(db.String)

    def __repr__(self):
        return f'<Sentiment sentiment_id={self.sentiment_id} tone={self.tone} keywords={self.keywords}>'



# For testing, you will want to change the postgresql database
# to a 'testdb' instead of 'db_uri'
def connect_to_db(flask_app, db_uri='postgresql:///phrases', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = False   
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to J's Sentiments db!")


if __name__ == '__main__':
    from server import app


    connect_to_db(app)