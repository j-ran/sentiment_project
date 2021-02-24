"""Server for sentiment-parsing app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud

# datetime is used to assign the date of "date of submission" 
# for newly created phrases
from datetime import datetime

# this import causes Jinja to show errors for undefined variables
# otherwise Jinja is silent on undefined variables
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "123"
app.jinja_env.undefined = StrictUndefined


#### --- HOMEPAGE --- ####
@app.route('/')
def show_phrases_homepage():
    """View homepage, which is also a phrase collection."""

    phrases = []
    #NB: all phrases are
    # phrase_collection = crud.get_phrase_collection()
    a_few_phrases = crud.get_a_few_phrases()
    for each_phrase in a_few_phrases:
        a_or_an = crud.get_a_or_an(each_phrase.job_at_phrase)
        # turn the phrase into a tuple that keeps its attributes together
        phrases.append((a_or_an, each_phrase.job_at_phrase, each_phrase.phrase_text, each_phrase.phrase_id))
        
    return render_template('homepage.html', 
                            phrases=phrases) # Explaining this in English –
                                                # on the left is the var on the html page, in Jinja
                                                # on the right is what that same var is called here
@app.route('/phrases/<phrase_id>')
def show_metadata(phrase_id):
    """Show metadata for a particular phrase."""

    phrase = crud.get_phrase_by_phrase_id(phrase_id)

    return render_template('phrase_metadata.html', phrase=phrase)


#### --- LOGIN --- ####
@app.route('/create_account')
def show_login_page():
    """Display the html where the 'login' and 'create_account' forms are."""
    return render_template('login.html')


@app.route('/create_account', methods=['POST'])
def create_account():
    """Create a new user account."""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    user = crud.get_user_by_email(email)
    
    if user:
        flash('That email is already registered. Please sign in rather than creating a new account.')
        return render_template('login.html', user=user)
    
    else:
        password = request.form.get('password')
        user = crud.create_user(fname=fname, lname=lname, email=email, password=password, consent=False)
        session['user_id'] = user.user_id
        flash('Account created! Please log in.')
        return render_template('login.html', user=user) ### SHOULD THIS BE user=session[user_id]                      


@app.route('/login')
def render_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    """Log in an existing user with email and password."""
    
    # get email from form
    email = request.form.get('email')
    # get password from form
    password = request.form.get('password')
    # return who the user is (from phrases db)
    user = crud.get_user_by_email(email)
    
    # if email exists:
    if user:
        # and if the password is correct:
        if password == user.password: 
            flash(f'You are logged in.')
        # add user to session 
            session['user_id'] = user.user_id 
            return redirect('/see_user_phrase_collection')
        
        # if password doesn't match email
        else:
            flash(f'{email} is in the database, but the password isn\'t right. Please try again!')
            #return render_template('login.html')

    else:
        flash(f'There is no record of the email "{email}." Please create an account.')
        #return render_template('login.html')
    
    #return redirect('/') 
    return render_template('login.html')                    


#### --- MAKE A NEW PHRASE --- ####
@app.route('/create_new_phrase')
def render_phrase_form():
    """Display the html for the 'create_new_phrase' form."""
    return render_template('add_new_phrase.html')


@app.route('/create_new_phrase', methods=['POST'])
def create_new_phrase():
    """Create a 140 char phrase with metadata."""

    # get phrase from form
    phrase_text = request.form.get('phrase_text')
    flash(f'WHAT A PHRASE! To see it with other phrases, go back to the homepage. Thank you!')

    #return render_template('add_new_phrase.html', phrase_text=phrase_text)
    #return redirect('/', phrase_text=phrase_text) # probably this will go to a display page of phrases ...
                                                  # for now, it goes to homepage

# def create_phrase_metadata():
#     """Create the metadata for a new phrase."""

    # take in the following:
    phrase_date=str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day)
    US_or_no=True 
    # phrase_city=phrase_city 
    phrase_city = request.form.get('phrase_city')
    # phrase_state=phrase_state, 
    phrase_state = request.form.get('phrase_state')
    # job_at_phrase=job_at_phrase, 
    job_at_phrase = request.form.get('job_at_phrase')
    # age_at_phrase=age_at_phrase,
    age_at_phrase = request.form.get('age_at_phrase') 

    phrase_and_score = crud.create_phrase_and_score(phrase_date=phrase_date, phrase_city=phrase_city, phrase_state=phrase_state, job_at_phrase=job_at_phrase, age_at_phrase=age_at_phrase, phrase_text=phrase_text, US_or_no=US_or_no)

    #return render_template('add_new_phrase.html', phrase_and_score=phrase_and_score)
    return render_template('login.html', phrase_and_score=phrase_and_score)


#### --- DISPLAY USER-SPECIFIC PHRASES --- ####
@app.route('/see_user_phrase_collection')
def see_user_phrase_collection():
    """View all of the phrases of the user in session."""
    # check if user_id is in session
    # if in session, get all phrases from CRUD function
    if 'user_id' in session:
        
        user_id = session['user_id']
        phrases = crud.get_phrase_by_user_id(user_id)
        print('********', phrases)
        return render_template('user_phrases.html', phrases=phrases)
    
    else:
        return redirect('/')
    



# phrases = Phrase.query.filter_by(user_id=user.id).all()
##### SOME EXTRA STUFF
# @app.route('/login')
# def login():    
#     # add code to let a user enter email and password
#     # a redirect to a page of their phrases
#     return render_template('login.html')

# THERE ARE MELONS HERE 
# DO I NEED THIS CODE SOMEWHERE?
    # if "username" in session.keys():
    #     return redirect("/top-melons")
    # else:
    #     return render_template("homepage.html")


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)