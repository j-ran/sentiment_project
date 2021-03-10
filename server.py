"""Server for sentiment-parsing app."""

######### -------- IMPORTED MODULES -------- #########
######### ------------------------------------ #######

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import requests
import crud
import json
import urllib.request

from random import choice, randint

# helper functions in helper.py
import helper
import sort

# this import causes Jinja to show errors for undefined variables
# otherwise Jinja is silent on undefined variables
from jinja2 import StrictUndefined


######### -------- API AUTHENTICATION -------- #########
######### ------------------------------------ #########
# for API authentication from CDC and from Google

import os

from sodapy import Socrata
client = Socrata('data.cdc.gov', os.environ['SOCRATA_APP_TOKEN'])

API_KEY = os.environ['GOOGLE_API_KEY']
GEOCODE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


######### ------ USING FLASK AND JINJA ------ #########
######### ----------------------------------- #########

app = Flask(__name__)
app.secret_key = "123"
app.jinja_env.undefined = StrictUndefined



######### ------------ START PAGE ------------ #########
######### ------------------------------------ #########
@app.route('/start')
def show_start_page():
    """View the start page, which introduces the project."""
  
    return render_template('start.html')



######### ------- BASIC PHRASE COLLECTION ------- #########
######### --------------------------------------- #########
@app.route('/phrase_collection')
def show_phrase_collection():
    """View a phrase collection of a few random phrases."""

    phrases = []
    #NB: all phrases are
    # phrase_collection = crud.get_phrase_collection()
    a_few_phrases = crud.get_a_few_phrases()
    for each_phrase in a_few_phrases:
        a_or_an = crud.get_a_or_an(each_phrase.job_at_phrase)
        # turn the phrase into a tuple that keeps its attributes together
        phrases.append((a_or_an, each_phrase.job_at_phrase, each_phrase.phrase_text, each_phrase.phrase_id))
        
    return render_template('phrase_collection.html', 
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
    
    response = requests.get(f'https://data.cdc.gov/resource/9mfq-cb36.json?submission_date={phrase_date}T00:00:00.000')
    # print a check: is the query successful, i.e., a 200?
    print('***1'*10, response.status_code)

    response = response.json()
    print(len(response)) # response is a list with 60 items in it
                         # it is grouped by locality (states and territories)    
    national_data = response
    # get the CDC data from the API query response
    for state_full_data in national_data:
        if state_full_data['state'] == phrase.phrase_state_abbr:
            tot_death = state_full_data['tot_death']    

    return render_template('phrase_metadata.html', phrase=phrase, tot_death=tot_death)



######### ------------- LOGIN ------------- #########
######### --------------------------------- #########
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
    print('***2'*10, email)
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

    if 'user_id' in session:
        user_id = session['user_id']
    
    else:
        flash(f'Please log-in to add a phrase. Thank you!')
        return redirect('/login')

    # create address from zipcode
    zip = request.form.get('zip')
    #use the Google Geocode API from helper.py
    results = helper.geocode(zip)
    # print a check
    print('***3'*10, [result["formatted_address"] for result in results])

    # get the state's full name from the zip
    state_full_name = [result["address_components"][3]["long_name"] for result in results]   
    state_full_name = str(state_full_name)
    state_full_name = state_full_name[2:-2]
    # get the state's abbreviation from the zip  
    state_abbr = [result["address_components"][3]["short_name"] for result in results]   
    state_abbr = str(state_abbr)
    state_abbr = state_abbr[2:-2]
    # get the city from the zip
    city_name = [result["address_components"][1]["long_name"] for result in results]   
    city_name = str(city_name)
    city_name = city_name[2:-2]
    #flash(f'{zip} received – hope it\'s good where I think you are: {city_name}, {state_full_name}.')
 
    # get phrase from form
    phrase_text = request.form.get('phrase_text')
    ### Add code in here to check for a repeated phrase and rejct if it's a repeat.

    # take in the following to make a Phrase –
    phrase_date  = helper.format_date_now() # date for CRUD is in form '%Y-%m-%d', stored as a string
    print('***4'*10, phrase_date)
    US_or_no = True 
    phrase_city = city_name
    phrase_state_abbr = state_abbr
    phrase_state = state_full_name
    phrase_region = helper.get_region(helper.get_state_abbr(phrase_state))
    # job_at_phrase=job_at_phrase 
    job_at_phrase = request.form.get('job_at_phrase')
    # age_at_phrase=age_at_phrase
    age_at_phrase = request.form.get('age_at_phrase')
    # put this user in session
    #user_id = session['user_id'] 
    print('***5'*10, (f'User in session is {user_id}.')) 
    
    phrase_and_score = crud.create_phrase_and_score(phrase_date=phrase_date, phrase_city=phrase_city, phrase_state_abbr=phrase_state_abbr, phrase_state=phrase_state, phrase_region=phrase_region, job_at_phrase=job_at_phrase, age_at_phrase=age_at_phrase, phrase_text=phrase_text, user_id=user_id, US_or_no=US_or_no)

    random_region_phrases = crud.get_region_phrases_by_phrase_text()
    first_region_phrase = random_region_phrases[0]
    region_name = first_region_phrase.phrase_region


    flash(f'While we get your phrase ready, look at phrases in the {region_name} region!')
    return render_template('sort_by_one_region.html', 
                                region_phrases=random_region_phrases, 
                                phrase_region=region_name) #### You should be able to do a redirect here
                                                           #### Which means you do not have to run the crud to get random phrases.



######### ----- DISPLAY PHRASES FROM ONE REGION ----- #########
######### ------------------------------------------- #########
@app.route('/sort_by_one_region')
def sort_by_one_region():
    """Take the most recent phrase from the user
       and display in a regional collection.
       If no user in session, choose a random region
       from which to display phrases."""
    
    # check if user_id is in session
    # if in session, get all user's phrases with CRUD function
    if 'user_id' in session:
        user_id = session['user_id']
        user_phrases = crud.get_phrases_by_user_id(user_id)
        
        # return most recent phrase
        # in a collection of phrases from the same region  
        most_recent_user_phrase = helper.get_most_recent_of_user_phrases(user_phrases)
        most_recent_phrase_text = most_recent_user_phrase.phrase_text
        region_phrases = crud.get_region_phrases_by_phrase_text(most_recent_phrase_text)
        
        return render_template('sort_by_one_region.html', 
                                region_phrases=region_phrases, 
                                phrase_region=most_recent_user_phrase.phrase_region)

    # if no user is in session, return phrases from  
    # a region which is chosen randomly
    else:
        region_phrases = crud.get_region_phrases_by_phrase_text()
        first_region_phrase = region_phrases[0]
        region_name = first_region_phrase.phrase_region
        flash(f'Please log-in to see your phrase with others from your region. These are phrases from the {region_name}.')
    
        return render_template('sort_by_one_region.html', 
                                region_phrases=region_phrases,  
                                phrase_region=region_name)



######### ---- DISPLAY ONE PHRASE FROM EACH REGION ---- #########
######### --------------------------------------------- #########
@app.route('/one_phrase_per_region')
def show_one_phrase_per_region():
    """Return one phrase for each region.
       If a user is in session, include one of their phrases."""
    
    one_phrase_per_region_list = []
    
    if 'user_id' in session:
        user_id = session['user_id']
        print('****userid'*5, user_id)
        user_phrases = crud.get_phrases_by_user_id(user_id)
        rand_index = randint(0, len(user_phrases)-1)
        rand_user_phrase = user_phrases[rand_index]
        one_phrase_per_region_list.append(rand_user_phrase)
        one_phrase_per_other_regions = crud.get_one_phrase_per_region_unless_given(rand_user_phrase.phrase_region)
        for phr in one_phrase_per_other_regions:
            one_phrase_per_region_list.append(phr)

    else:
        one_phrase_per_region = crud.get_one_phrase_per_region_unless_given()
        for phr in one_phrase_per_region:
            one_phrase_per_region_list.append(phr)

    return render_template('one_phrase_per_region.html', one_phrase_per_region_list=one_phrase_per_region_list)



######### -------- SORT BY MONTH -------- #########
######### ------------------------------- #########
@app.route('/sort_three_ways')
def show_sort_three_ways():
    """Display the html for the 'sort_three_ways' form."""
    
    return render_template('sort_three_ways.html')

@app.route('/sort_by_month')
def show_sort_three_ways_month():
    """Display the html for the 'sort_three_ways' form."""
    
    return redirect('/sort_three_ways')


@app.route('/sort_by_month', methods=['POST'])
def get_phrases_by_month():
    """Return the phrases for a given month."""

    # get_args for which month
    # it is in the form of a date_string, which is taken by the helper function
    # run helper function for full month name 
    date_str = request.form.get('month')
    month_num = date_str[5:7]
    month_name = helper.month_name_from_num(month_num)
    # run helper function to get list of phrase texts
    phrases_by_month = crud.get_phrases_by_month(date_str)
    
    return render_template('sort_by_month.html', 
                            month_name=month_name, 
                            phrases_by_month=phrases_by_month)



######### -------- SORT BY FEELING -------- #########
######### --------------------------------- #########
@app.route('/sort_by_feeling')
def show_sort_three_ways_feeling():
    """Display the html for the 'sort_three_ways' form."""

    return redirect('/sort_three_ways')


@app.route('/sort_by_feeling', methods=['POST'])
def get_phrases_by_feeling():
    """Return the phrases for a given feeling."""

    feeling = request.form.get('feeling')
    phrases_by_feeling = helper.sort_by_feeling(feeling)
    
    return render_template('sort_by_feeling.html',  
                            phrases_by_feeling=phrases_by_feeling)    



######### -------- SORT BY REGION -------- #########
######### -------------------------------- #########
@app.route('/sort_by_region')
def show_sort_three_ways_region():
    """Display the html for the 'sort_three_ways' form."""
    
    return redirect('/sort_three_ways')


@app.route('/sort_by_region', methods=['POST'])
def get_phrases_by_region_name():
    """Return the phrases for a given feeling."""

    region = request.form.get('region')
    region_phrases = crud.get_phrases_by_region(region)

    return render_template('sort_by_one_region.html', 
                            region_phrases=region_phrases,  
                            phrase_region=region)



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


