"""Server for sentiment-parsing app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud

# this import causes Jinja to show errors for undefined variables
# otherwise Jinja is silent on undefined variables
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "123"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def see_phrases_homepage():
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
        session['user_id'] = user ### Is this user.user_id?
        flash('Account created! Please log in.')
        return render_template('login.html', user=user) ### SHOULD thiS BE user=session[user_id]                      


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
            flash(f'Thank you. You are being logged in.')
        # add user to session 
            session['user_id'] = user ### Is this user.user_id?
            return render_template('user_phrases.html')
        
        # if password doesn't match email
        else:
            flash(f'{email} is in the database, but the password isn\'t right. Please try again!')
            #return render_template('login.html')

    else:
        flash(f'There is no record of the email "{email}." Please create an account.')
    
    
    return render_template('login.html', user=user)                     


@app.route('/create_new_phrase', methods=['POST'])
def create_new_phrase():
    """Create a 140 char phrase."""

    # get phrase from form
    phrase_text = request.form.get('phrase_text')
    flash(f'WHAT A PHRASE! In order to add it to the database, we need to be able to display the following fields. \nBy filling out and submitting these fields, you agree for us to use your phrase. Thank you!')

    return redirect('/', phrase_text=phrase_text)

@app.route('/create_phrase_metadata', methods=['POST'])
def create_phrase_metadata():
    """Create the metadata for a new phrase."""

    # take in the following:
    phrase_date='20210223' # -- THIS IS DATETIME.DATETIME.NOW, in an acceptable form
    US_or_no=True 
    # phrase_city=phrase_city 
    phrase_city = request.form.get('phrase_city')
    # phrase_state=phrase_state, 
    phrase_state = request.form.get('phrase_state')
    # job_at_phrase=job_at_phrase, 
    job_at_phrase = request.form.get('job_at_phrase')
    # age_at_phrase=age_at_phrase,
    age_at_phrase = request.form.get('age_at_phrase') 

    phrase_and_score = create_phrase_and_score(phrase_date=phrase_date, phrase_city=phrase_city, phrase_state=phrase_state, job_at_phrase=job_at_phrase, age_at_phrase=age_at_phrase, phrase_text=phrase_text, US_or_no=US_or_no)

    return redirect('/', phrase_and_score=phrase_and_score)


@app.route('/see_user_phrase_collection', methods=['POST'])
def see_user_phrase_collection():
    """View all of the phrases of the user in session."""

    return render_template(user_phrase_collection.html)
    

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