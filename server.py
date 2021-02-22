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

    phrases = []
    #NB: all phrases are
    # phrase_collection = crud.get_phrase_collection()
    a_few_phrases = crud.get_a_few_phrases()
    for each_phrase in a_few_phrases:
        print(each_phrase)
        a_or_an = crud.get_a_or_an(each_phrase.job_at_phrase)
        print(each_phrase.job_at_phrase)
        phrases.append((a_or_an, each_phrase.job_at_phrase, each_phrase.phrase_text, each_phrase.phrase_id))

    print(phrases)     # not working currently
                                                              # the last 'a_or_an' is applied to all phrases
        
    return render_template('phrase_collection.html', 
                            phrases=phrases) # Explaining this in English –
                                                # on the left is the var on the html page, in Jinja
                                                # on the right is what that same var is called here


@app.route('/phrases/<phrase_id>')
def show_metadata(phrase_id):
    """Show metadata for a particular phrase."""

    phrase = crud.get_phrase_by_phrase_id(phrase_id)

    return render_template('phrase_metadata.html', phrase=phrase)


@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('That email is already registered. Please sign in rather than creating a new account.')
        
    else:
        crud.create_user(fname, lname, email, password, consent=False)
        flash('Account created! Please log in.')

    return redirect('/')    

@app.route('/login')
def login():    
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    """Log in an existing user with email, or with username and password."""
    
    # get email from form
    email = request.form.get('email')
    # return who the user is (from phrases db)
    user = crud.get_user_by_email(email)
    
    # if email exists:
    if user:
        # add user to session
        session['user_id'] = user
        # this is from Cori – return jsonify({'status': 'ok', 'username_email': username_email})
    # else:
    #     # display error text 
    #     # TODO: display create account form
    #     return jsonify({'status': 'error', 'msg': 'NOPE, password does not match a user in the db'})


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