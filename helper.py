"""Helper functions for server.py."""


######### -------- DATE OF SUBMISSION -------- #########
######### ------------------------------------ #########
# datetime is used to assign the date of submission for a phrase
# for newly created phrases

from datetime import datetime

def format_date_now():
    """Create a string of the current date in the form %Y-%m-%d.
    >>> format_date_now()
    2021-03-05
    """
    
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')

    phrase_date = year + '-' + month + '-' + day
    return phrase_date


######### -------- GOOGLE GEOCODE API -------- #########
######### ------------------------------------ #########

# for API authentication from Google
import os
import urllib.request
import json

API_KEY = os.environ['GOOGLE_API_KEY']
GEOCODE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

def geocode(address):
    # Join the parts of the URL together into one string.
    params = urllib.parse.urlencode({"address": address, "key": API_KEY,})
    url = f"{GEOCODE_BASE_URL}?{params}"

    result = json.load(urllib.request.urlopen(url))

    if result["status"] in ["OK", "ZERO_RESULTS"]:
        return result["results"]

    raise Exception(result["error_message"])


######### ---- PREPPING PHRASES FOR REGION-BASED SORTS ---- #########
######### ------------------------------------------------- #########

# pacific = {'Pacific':['CA','HI','OR','WA','AK','NV','NM']}
# west = {'West':['AZ','CO','UT','ID','WY','MT','TX','OK','NE']}
# midwest = {'Midwest':['ND','SD','MN','WI','IA','KS','MO','AR''IL']}
# midatlantic = {'Mid Atlantic':['MI','IN','OH','PA','WV','VA','DC','MD','NC']}
# southeast = {'Southeast':['TN','SC','GA','FL','AL','MS','LA','KY','PR']}
# new_england = {'New England':['ME','NH','VT','MA','RI','CT','NY','NJ','NYC','DE']}
# territories = {'Territories':['AS','DC','FM','GU','MH','MP','PW','PR','VI']}

def get_state_full_name(state_abbr):
    """Given a state's two-letter abbreviation, 
       return its full name.
       
       >>> print(get_state_full_name('OH'))
       Ohio"""
    
    states_dict = {'Alabama':'AL', 'Alaska':'AK', 'Arizona':'AZ', 'Arkansas':'AR', 'California':'CA', 'Colorado':'CO', 'Connecticut':'CT', 'Delaware':'DE', 'Florida':'FL', 'Georgia':'GA', 'Hawaii':'HI', 'Idaho':'ID', 'Illinois':'IL', 'Indiana':'IN', 'Iowa':'IA', 'Kansas':'KS', 'Kentucky':'KY', 'Louisiana':'LA', 'Maine':'ME', 'Maryland':'MD', 'Massachusetts':'MA', 'Michigan':'MI', 'Minnesota':'MN', 'Mississippi':'MS', 'Missouri':'MO', 'Montana':'MT', 'Nebraska':'NE', 'Nevada':'NV', 'New Hampshire':'NH', 'New Jersey':'NJ', 'New Mexico':'NM', 'New York':'NY', 'NYC':'NY', 'North Carolina':'NC', 'North Dakota':'ND', 'Ohio':'OH', 'Oklahoma':'OK', 'Oregon':'OR', 'Pennsylvania':'PA', 'Rhode Island':'RI', 'South Carolina':'SC', 'South Dakota':'SD', 'Tennessee':'TN', 'Texas':'TX', 'Utah':'UT', 'Vermont':'VT', 'Virginia':'VA', 'Washington':'WA', 'West Virginia':'WV', 'Wisconsin':'WI', 'Wyoming':'WY', 'American Samoa':'AS', 'District of Columbia':'DC', 'Washington DC':'DC', 'Federated States of Micronesia':'FM', 'Guam':'GU', 'Marshall Islands':'MH', 'Northern Mariana Islands':'MP', 'Palau':'PW', 'Puerto Rico':'PR', 'Virgin Islands':'VI'}
  
    for i in states_dict:
        for full_name, abbr in states_dict.items():
            if abbr == state_abbr:
                return full_name   


def get_state_abbr(state_full_name):
    """Given a state's full name as it appears for Google Geocode API, 
    return its valid abbreviation for the CDC Covid Tracking API.
       
       >>> print(get_state_abbr('Puerto Rico'))
       PR"""
    
    states_dict = {'Alabama':'AL', 'Alaska':'AK', 'Arizona':'AZ', 'Arkansas':'AR', 'California':'CA', 'Colorado':'CO', 'Connecticut':'CT', 'Delaware':'DE', 'Florida':'FL', 'Georgia':'GA', 'Hawaii':'HI', 'Idaho':'ID', 'Illinois':'IL', 'Indiana':'IN', 'Iowa':'IA', 'Kansas':'KS', 'Kentucky':'KY', 'Louisiana':'LA', 'Maine':'ME', 'Maryland':'MD', 'Massachusetts':'MA', 'Michigan':'MI', 'Minnesota':'MN', 'Mississippi':'MS', 'Missouri':'MO', 'Montana':'MT', 'Nebraska':'NE', 'Nevada':'NV', 'New Hampshire':'NH', 'New Jersey':'NJ', 'New Mexico':'NM', 'New York':'NY', 'NYC':'NY', 'North Carolina':'NC', 'North Dakota':'ND', 'Ohio':'OH', 'Oklahoma':'OK', 'Oregon':'OR', 'Pennsylvania':'PA', 'Rhode Island':'RI', 'South Carolina':'SC', 'South Dakota':'SD', 'Tennessee':'TN', 'Texas':'TX', 'Utah':'UT', 'Vermont':'VT', 'Virginia':'VA', 'Washington':'WA', 'West Virginia':'WV', 'Wisconsin':'WI', 'Wyoming':'WY', 'American Samoa':'AS', 'District of Columbia':'DC', 'Washington DC':'DC', 'Federated States of Micronesia':'FM', 'Guam':'GU', 'Marshall Islands':'MH', 'Northern Mariana Islands':'MP', 'Palau':'PW', 'Puerto Rico':'PR', 'Virgin Islands':'VI'}
  
    state_abbr = (states_dict[state_full_name]) 
    return state_abbr


######### -------- REGION-BASED SORTS -------- #########
######### ------------------------------------ #########

def get_random_region():
    regions_list = ['Pacific', 'West', 'Midwest','Mid-Atlantic', 'Southeast', 'New England', 'Territories']
    rand_index = randint(0, len(regions_list)-1)
    rand_region = regions_list[rand_index]
    return rand_region

def get_region(get_state_abbr):
    """Return the region for a phrase. 
       This takes in a state's full name from the function 'get_state_abbr' 
       and returns the region to which that state belongs. 
    
    >>> get_region('OH')
    Mid-Atlantic

    >>> (get_region(get_state_abbr('Ohio')))
    Mid-Atlantic"""


    regions_list=[{'Pacific':['CA','HI','OR','WA','AK','NV','NM']}, {'West':['AZ','CO','UT','ID','WY','MT','TX','OK','NE']}, {'Midwest':['ND','SD','MN','WI','IA','KS','MO','AR''IL']}, {'Mid-Atlantic':['MI','IN','OH','PA','WV','VA','DC','MD','NC']}, {'Southeast':['TN','SC','GA','FL','AL','MS','LA','KY','PR']}, {'New England':['ME','NH','VT','MA','RI','CT','NY','NJ','NYC','DE']},{'Territories':['AS','DC','FM','GU','MH','MP','PW','PR','VI']}]

    for i in range(len(regions_list)):
        for region, states in (regions_list[i]).items():
            if get_state_abbr in states:
                return(region)        


######### -------- MOST-RECENT PHRASE -------- #########
######### ------------------------------------ #########
def get_most_recent_of_user_phrases(user_phrases):

    """This function makes sure we get the phrase-just-created.

        NB – almost! It actually gets phrases from the most recent DAY! 
        Because I stored datetime as a date-based string, not as a datetime object with real time.
        To correct later.

        The argument, user_phrases, is a list of Phrase objects returned 
        from 'crud.get_phrase_by_user_id(user_id)'.
    """
# compare dates of the phrases and find the most recent
# can use adapted bubble sort since only looking for most recent,
# not looking for full sort
    phrase_dates_list = [(user_phrases[0])]
    for i in range(len(user_phrases)-1):
        date = user_phrases[i].phrase_date
        date = date.replace('-', '')
        date = int(date)
        next_date = user_phrases[(i + 1)].phrase_date
        next_date = next_date.replace('-', '')
        next_date = int(next_date)
        if date > next_date:
            user_phrases[i].phrase_date, user_phrases[(i + 1)].phrase_date = user_phrases[(i + 1)].phrase_date, user_phrases[i].phrase_date  
        else:
            phrase_dates_list.append(user_phrases[(i + 1)].phrase_date)
    
    most_recent_date_string = (phrase_dates_list[-1])
    # find the first phrase that matches that day
    for phrase in user_phrases:
        if phrase.phrase_date == most_recent_date_string:
            return phrase



# Testing strip-white-space Python methods: 
# s1 = ' Looking at strip. '
# s2 = 'Looking at strip right.  '
# s3 = '  Looking at strip left.'
# print(s1.strip())
# print(s2.rstrip())
# print(s3.lstrip())
# print(s1)
# print(s2)
# print(s3)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

