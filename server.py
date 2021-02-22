"""Server for sentiment-parsing app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

# this import causes Jinja to show errors for undefined variables
# otherwise Jinja is silent on undefined variables
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "123"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/phrases')
def see_phrases():
    """View the phrase collection."""

    #NB: all phrases are
    # phrase_collection = crud.get_phrase_collection()
    a_few_phrases = crud.get_a_few_phrases()
    for each_phrase in a_few_phrases:
        a_or_an = crud.get_a_or_an(each_phrase.job_at_phrase) # not working currently
                                                              # the last 'a_or_an' is applied to all phrases
        
    return render_template('phrase_collection.html', 
                            phrases=a_few_phrases,
                            a_or_an=a_or_an) # What is this in English?
                                                # on the left is the var on the html page, in Jinja
                                                # on the right is what that same var is called here


# @app.route('/movies/<movie_id>')
# def show_movie(movie_id):
#     """Show details on a particular movie."""

#     movie = crud.get_movie_by_id(movie_id)

#     return render_template('movie_details.html', movie=movie)


# @app.route('/users')
# def all_users():
#     """View all users."""

#     users = crud.get_users()

#     return render_template('all_users.html', users=users)


# @app.route('/users/<user_id>')
# def show_user(user_id):
#     """Show details on a particular user."""

#     user = crud.get_user_by_id(user_id)

#     return render_template('user_details.html', user=user)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)