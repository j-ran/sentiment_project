"""Server for sentiment-parsing app."""

######### -------- IMPORTED MODULES -------- #########
######### ------------------------------------ #######

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import requests
import crud
import json
import urllib.request

# datetime is used to assign the date of "date of submission" 
# for newly created phrases
from datetime import datetime

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
    
    response = requests.get(f'https://data.cdc.gov/resource/9mfq-cb36.json?&submission_date={phrase_date}T00:00:00.000')
    # print a check: is the query successful, i.e., a 200?
    print('***1'*10, response.status_code)

    response = response.json()
    print(len(response)) # response is a list with 60 items in it
                        # it is grouped by locality (states and territories)
    national_data = response
    
    # To get a particular state's data
    # First, need to convert the state name into its 2-letter abbr.
    def geocode(address):
        # Join the parts of the URL together into one string.
        params = urllib.parse.urlencode({"address": address, "key": API_KEY,})
        url = f"{GEOCODE_BASE_URL}?{params}"

        result = json.load(urllib.request.urlopen(url))

        if result["status"] in ["OK", "ZERO_RESULTS"]:
            return result["results"]

        raise Exception(result["error_message"])

    results = geocode(address=phrase_state)
    # print a check
    print('***2'*10, [result["formatted_address"] for result in results])
    
    print('***3'*10, phrase_state)
    # check if the state is already abbreviated or not
    if len(phrase_state) > 2:
        # get the state's abbreviated name from its full name
        # so that it can be found with the CDC API
        state_short_name = (results[0]['address_components'][0]['short_name'])   
        state_short_name = str(state_short_name)
        state_short_name = state_short_name[2:-2]     
    else:
        state_short_name = phrase_state    
    print('***4'*10, f'__{state_short_name}__')
    # get the CDC data from the API query response
    for state_full_data in national_data:
        if state_full_data['state'] == state_short_name:
            tot_death = state_full_data['tot_death']
        
        state_abbr = state_full_data['state']
        print('***5'*10, f'__{state_abbr}__')      

    # This is to get a sum of all US deaths in one day. 
    # day_death_total = 0
    # for count, state_full_data in enumerate(national_data):
    #     day_death_total = day_death_total + int(state_full_data['tot_death'])
        #print(count, state_full_data['state'], state_full_data['tot_death'])
    #print('national death total for this day is', day_death_total)


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

    # create address from zipcode
    zip = request.form.get('zip')
    def geocode(address):
        # Join the parts of the URL together into one string.
        params = urllib.parse.urlencode({"address": address, "key": API_KEY,})
        url = f"{GEOCODE_BASE_URL}?{params}"

        result = json.load(urllib.request.urlopen(url))

        if result["status"] in ["OK", "ZERO_RESULTS"]:
            return result["results"]

        raise Exception(result["error_message"])

    results = geocode(zip)
    # print a check
    print('***'*10, [result["formatted_address"] for result in results])
    
    # get the state's full name from the zip
    state_full_name = [result["address_components"][3]["long_name"] for result in results]   
    state_full_name = str(state_full_name)
    state_full_name = state_full_name[2:-2]
    
    # get the city from the zip
    city_name = [result["address_components"][1]["long_name"] for result in results]   
    city_name = str(city_name)
    city_name = city_name[2:-2]

    flash(f'{zip} received – are you in {city_name}, {state_full_name}?')

    ####
    # get phrase from form
    phrase_text = request.form.get('phrase_text')
    flash(f'WHAT A PHRASE! Thank you!')
    # take in the following to make a Phrase –
    # date for CRUD is in form '%Y-%m-%d'
    phrase_date=(datetime.now().strftime('%Y')) + '-' + (datetime.now().strftime('%m')) + '-' + (datetime.now().strftime('%d'))
    print('***'*20, phrase_date)
    US_or_no=True 
    phrase_city = city_name
    phrase_state = state_full_name
    # job_at_phrase=job_at_phrase 
    job_at_phrase = request.form.get('job_at_phrase')
    # age_at_phrase=age_at_phrase
    age_at_phrase = request.form.get('age_at_phrase')
    # put this user in session
    user_id = session['user_id'] 
    print(f'***** User in session is {user_id}.') 
    phrase_and_score = crud.create_phrase_and_score(phrase_date=phrase_date, phrase_city=phrase_city, phrase_state=phrase_state, job_at_phrase=job_at_phrase, age_at_phrase=age_at_phrase, phrase_text=phrase_text, user_id=user_id, US_or_no=US_or_no)


    flash(f'I hope it\'s nice in {phrase_city} today.')
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



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


### This code below was a test. No longer needed.
##### ----  GETTING CITY AND STATE FROM ZIPCODE ---- #####
######### -------------------------------------- #########
@app.route('/zip')
def render_zip_form():
    """Display the html for the 'zipcode' form."""
    
    return render_template('zip.html')
@app.route('/zip', methods=['POST'])
def show_address_from_zip():
    zip = request.form.get('zip')

    # use geocode to parse response
    def geocode(address):
        # Join the parts of the URL together into one string.
        params = urllib.parse.urlencode({"address": address, "key": API_KEY,})
        url = f"{GEOCODE_BASE_URL}?{params}"

        result = json.load(urllib.request.urlopen(url))

        if result["status"] in ["OK", "ZERO_RESULTS"]:
            return result["results"]

        raise Exception(result["error_message"])

    results = geocode(zip)
    # print a check
    print('***'*10, [result["formatted_address"] for result in results])
    
    # get the state's full name from the zip
    state_full_name = [result["address_components"][3]["long_name"] for result in results]   
    state_full_name = str(state_full_name)
    state_full_name = state_full_name[2:-2]
    
    # get the city from the zip
    city_name = [result["address_components"][1]["long_name"] for result in results]   
    city_name = str(city_name)
    city_name = city_name[2:-2]

    flash(f'{zip} received – are you in {city_name}, {state_full_name}?')
    
    return render_template('zip.html')



### --- GETTING ADDRESS DATA FOR SIGN-IN FORM AND FOR PHRASE METADATA --- ###
######### --------------------------------------------------------- #########
# //when the user clicks off of the zip field:
# $('#zip').blur(function(){
#   var zip = $(this).val();
#   var city = '';
#   var state = '';

#   //make a request to the google geocode api

#   $.getJSON('http://maps.googleapis.com/maps/api/geocode/json?address=43214&key=AIzaSyBNh5ATRGwWXYusbg_1zxFwHcfTF9ukmc4').success(function(response){
#     //find the city and state
#     var address_components = response.results[0].address_components;
#     $.each(address_components, function(index, component){
#       var types = component.types;
#       $.each(types, function(index, type){
#         if(type == 'locality') {
#           city = component.long_name;
#         }
#         if(type == 'administrative_area_level_1') {
#           state = component.short_name;
#         }
#       });
#     });

#     //pre-fill the city and state
#     $('#city').val(city);
#     $('#state').val(state);
#   });
# });
