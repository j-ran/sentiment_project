"""Server for sentiment-parsing app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import requests
import crud
import json

# datetime is used to assign the date of "date of submission" 
# for newly created phrases
from datetime import datetime

# this import causes Jinja to show errors for undefined variables
# otherwise Jinja is silent on undefined variables
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "123"
app.jinja_env.undefined = StrictUndefined


######### ------------- HOMEPAGE ------------- #########
######### ------------------------------------ #########
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


######### - METADATA FOR SPECIFIC PHRASES - #########
######### --------------------------------- #########
@app.route('/phrases/<phrase_id>')
def show_metadata(phrase_id):
    """Show metadata for a particular phrase. 
       Query the CDC API for COVID data."""

    phrase = crud.get_phrase_by_phrase_id(phrase_id)
    phrase_state = phrase.phrase_state
    phrase_date = str(phrase.phrase_date)
    phrase_date = phrase_date[:10]
    # print a check: is the date correct?
    # print('***1'*10, (f'phrase_date is {phrase_date}.'))
    response = requests.get(f'https://data.cdc.gov/resource/9mfq-cb36.json?state={phrase_state}&submission_date={phrase_date}T00:00:00.000')
    # print a check: is the query successful, i.e., a 200?
    # print('***2'*10, response.status_code)
    
    # print('this is the response BEFORE .json', response)
    # OUTPUT: <Response [200]>

    # format 'response' for further parsing 
    response = response.json()
    
    # print('this is the response AFTER .json', response)
    # OUTPUT: [{'submission_date': '2020-05-20T00:00:00.000', 'state': 'CA', 'tot_cases': '84057', 'new_case': '2262.0', 'pnew_case': '0', 'tot_death': '3436', 'new_death': '102.0', 'pnew_death': '0', 'created_at': '2020-05-21T15:41:38.000', 'consent_cases': 'Not agree', 'consent_deaths': 'Not agree'}]

    # create a formatted string of the Python JSON object
    response_str = json.dumps(response, sort_keys=True)
    print(response_str[0:17])
    print('***3'*10)
    # this is the full string:
    print(response_str)

    ### The return from the API is a string with 'json.dumps'
    ### I need to reconstruct it as a dictionary that I can call.
    ### I am reconstructing the string as a dictionary with 'json.loads'

    print('***4'*10)
    as_python = json.loads(response_str)
    python_dict = as_python[0]
    tot_death = python_dict['tot_death']
    print(tot_death)

    return render_template('phrase_metadata.html', phrase=phrase, tot_death=tot_death)


######### ------------- LOGIN ------------- #########
######### ------------------------------------ #########
@app.route('/login')
def show_login_page():
    """Display the html where the 'login' and 'create_account' forms are."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Login existing user and put into session."""
    
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if user:
    
        if password == user.password: 
            # add user to session 
            session['user_id'] = user.user_id 
            return redirect('/add_new_phrase') 
        else:
            flash('The password doesn\'t match the email. Please try again.')
            return render_template('login.html', user=user)
    
    else:
        flash('Thanks! We don\'t have any phrases from you yet. Please create an account.')
        return redirect('/create_account')


@app.route('/create_account')
def show_create_account():
    """Display the html where the 'login' and 'create_account' forms are."""

    return render_template('login.html')


@app.route('/create_account', methods=['POST'])
def create_account():
    """Create new account and put user into session."""
        
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email') # how do I get these to get here?
    print('**********', email)
    password = request.form.get('password') # how do I get these to get here?
    user = crud.get_user_by_email(email)
    
    if user: 
        flash(f'{email} is already in the database. Please go to login.')
        return redirect('/login')
    
    else:
        new_user = crud.create_user(fname=fname, lname=lname, email=email, password=password, consent=False)
        session['user_id'] = new_user.user_id
        
        flash(f'Account for {new_user.fname} created!')
        return render_template('add_new_phrase.html', user=user, new_user=new_user)                      


######### -------- ADD A NEW PHRASE -------- #########
######### ---------------------------------- #########
@app.route('/add_new_phrase')
def render_phrase_form():
    """Display the html for the 'add_new_phrase' form."""
    
    return render_template('add_new_phrase.html')


@app.route('/add_new_phrase', methods=['POST'])
def add_new_phrase():
    """Create a 140 char phrase with metadata."""

    # get phrase from form
    phrase_text = request.form.get('phrase_text')
    flash(f'WHAT A PHRASE! Thank you!')
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
    # put this user in session
    user_id = session['user_id'] 
    print(f'***** User in session is {user_id}.') 
    phrase_and_score = crud.create_phrase_and_score(phrase_date=phrase_date, phrase_city=phrase_city, phrase_state=phrase_state, job_at_phrase=job_at_phrase, age_at_phrase=age_at_phrase, phrase_text=phrase_text, user_id=user_id, US_or_no=US_or_no)
    
    return render_template('add_new_phrase.html', phrase_and_score=phrase_and_score)


######### ----- DISPLAY USER-SPECIFIC PHRASES ----- #########
######### ----------------------------------------- #########
@app.route('/see_user_phrase_collection')
def see_user_phrase_collection():
    """View all of the phrases of the user in session."""
    # check if user_id is in session
    # if in session, get all phrases from CRUD function
    if 'user_id' in session:
        user_id = session['user_id']
        phrases = crud.get_phrase_by_user_id(user_id)
        
        return render_template('user_phrases.html', phrases=phrases)
    
    else:
        flash(f'Please log-in to see your phrases.')
        return redirect('/login')


### --- GETTING ADDRESS DATA FOR SIGN-IN FORM AND FOR PHRASE METADATA --- ###
######### --------------------------------------------------------- #########
//when the user clicks off of the zip field:
$('#zip').blur(function(){
  var zip = $(this).val();
  var city = '';
  var state = '';

  //make a request to the google geocode api

  $.getJSON('http://maps.googleapis.com/maps/api/geocode/json?address=43214&key=AIzaSyBNh5ATRGwWXYusbg_1zxFwHcfTF9ukmc4').success(function(response){
    //find the city and state
    var address_components = response.results[0].address_components;
    $.each(address_components, function(index, component){
      var types = component.types;
      $.each(types, function(index, type){
        if(type == 'locality') {
          city = component.long_name;
        }
        if(type == 'administrative_area_level_1') {
          state = component.short_name;
        }
      });
    });

    //pre-fill the city and state
    $('#city').val(city);
    $('#state').val(state);
  });
});






if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)