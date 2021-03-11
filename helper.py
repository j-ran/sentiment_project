"""Helper functions for server.py."""

# The following is defined in model.py –
from model import db, connect_to_db, User, Phrase, Sentiment #Interaction, Interaction_type
from score import swn_polarity

from random import choice, randint

from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

######### -------- DATE OF SUBMISSION -------- #########
######### ------------------------------------ #########
# datetime is used to assign the date of submission for a phrase
# for newly created phrases

# do you have the right import?
# from datetime import datetime

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


######### ---- ENCHANT SPELLING SUGGESTER ---- #########
######### ------------------------------------ #########
# See info on PyEnchant here:
# http://pyenchant.github.io/pyenchant/tutorial.html

import enchant  
from enchant.tokenize import get_tokenizer, EmailFilter

def suggester(word):
    """If word not in Enchant's English language dictionary, 
    suggest 3 alternatives.

    >>> suggester("helo")
    ['hole', 'help', 'helot']
    >>> suggester("hello")
    None

    """
    
    d = enchant.Dict("en_US")
    if d.check(word) == False:
        return (d.suggest(word)[:3])
        

def is_email(email_entry):
    """Using a Filter for emails, check that an entry
    contains an email.email
    
    >>> is_email("send an email to fake@example.com please")
    True
    >>> is_email("send an email to fakeexample.com please")
    False
    """

    tknzr1 = get_tokenizer("en_US")
    tknzr_list1 = [w for w in tknzr1(email_entry)]
    tknzr2 = get_tokenizer("en_US", filters=[EmailFilter])
    tknzr_list2 = [w for w in tknzr2(email_entry)]
    print(len(tknzr_list1), len(tknzr_list2))
    if (len(tknzr_list1)) == (len(tknzr_list2)): 
        #print("Please make sure that's an email!")
        return False
    else:
        #print("ok") 
        return True   


######### ---- CDC SOCRATA API FOR VACCINATIONS ---- #########
######### ------------------------------------------ #########
import crud 
import requests

def get_vaccine_data(phrase_id):
    """Show vaccine total for the day of a particular phrase. 
       Query the CDC API for COVID data.
       The total will be int(0) if no vaccines have been allocated.
       The total will be int(0) if one of the APIs does not return. """

    phrase = crud.get_phrase_by_phrase_id(phrase_id)
    #phrase_state = phrase.phrase_state
    print(phrase.phrase_text)
    phrase_date = str(phrase.phrase_date)
    print(phrase_date)
    phrase_date_str = phrase_date[:10]
    print(phrase_date_str)

    def get_most_recent_past_monday(phrase_date_str):
        """Takes in the date as a string, such as '2021-02-04' 
        and returns the most recent past Monday. 
        The string is in form'%Y-%m-%d'.
        
        >>> get_most_recent_past_monday('2021-02-04')
        2021-02-01
        """

        date_str = phrase_date_str
        date_str_obj = datetime.strptime(date_str, '%Y-%m-%d') #create datetime obj
        #print(date_str_obj)
        day = date_str_obj.weekday() # index of weekday, with Monday at '0' index
        #print(day)
        days = (0 - day) # how many days from Monday
        # print(days)
        new_date=str(date_str_obj + timedelta(days=days)) # datetime obj into a datetime.datetime obj
        #print(new_date)
        mon_date=new_date[:10]                            # so as to use with timedelta

        return mon_date # – should be of the form str(2021-02-15)
    
    mon_date = get_most_recent_past_monday(phrase_date_str)
    print(f'mon_date = <{mon_date}>')
    # vaccine01 is Pfizer; starts 2020-12-14
    vaccine01_response = requests.get(f'https://data.cdc.gov/resource/saz5-9hgg.json?week_of_allocations={mon_date}T00:00:00.000')
    # vaccine02 is Moderna; starts 2020-12-21
    vaccine02_response = requests.get(f'https://data.cdc.gov/resource/b7pe-5nws.json?week_of_allocations={mon_date}T00:00:00.000')
    # vaccine03 is Janssen; starts 2021-03-01
    vaccine03_response = requests.get(f'https://data.cdc.gov/resource/w9zu-fywh.json?week_of_allocations={mon_date}T00:00:00.000')

    # if one of the queries is successful (meaning returning int(200)), continue:
    if vaccine01_response.status_code == 200 or vaccine02_response.status_code == 200 or vaccine03_response.status_code == 200: 
        print('***pfizer'*3, vaccine01_response.status_code)
        print('***moderna'*3, vaccine02_response.status_code)
        print('***janssen'*3, vaccine03_response.status_code)
    else:
        print('else return on status.code')
        tot_vaccines = 0
        return tot_vaccines
    
    response01 = vaccine01_response.json()
    response02 = vaccine02_response.json()
    response03 = vaccine03_response.json()
    
    # if one of the responses contain numbers, continue:
    if bool(response01) == True or bool(response02) == True or bool(response03) == True:
        print(bool(response01)) 
    else:
        print('else return on Truthies')
        tot_vaccines = 0
        return tot_vaccines
    
    # get Pfizer total from API return
    response01_nums = []
    if response01[0]:
        for i in range(len(response01)):
            num = int(response01[i]['_2nd_dose_allocations'])
            response01_nums.append(num)
        response01_tot = sum(response01_nums)    
        # print('***response01_tot'*10, response01_tot)

    # get Moderna total from API return
    response02_nums = []
    if response02[0]:
        for i in range(len(response02)):
            num = int(response02[i]['_2nd_dose_allocations'])
            response02_nums.append(num)
        response02_tot = sum(response02_nums)    
        # print('***response02_tot'*10, response02_tot)
    
    # get Janssen total from API return
    response03_nums = []
    if response03[0]:
        for i in range(len(response03)):
            num = int(response03[i]['_1st_dose_allocations'])
            response03_nums.append(num)
        response03_tot = sum(response03_nums)    
        # print('***response03_tot'*10, response03_tot)
       
    tot_vaccines = (response01_tot + response02_tot + response03_tot)
    print('***tot_vaccines'*10, tot_vaccines)
    return tot_vaccines    


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


######### ------ MONTH-NAME CONVERSION ------ #########
######### ----------------------------------- #########
def month_name_from_num(month_num):
    month_name_dict = { '01':'January', '02':'February', 
                        '03':'March', '04':'April', 
                        '05':'May', '06':'June',
                        '07':'July', '08':'August', 
                        '09':'September', '10':'October', 
                        '11':'November', '12':'December'
                        }
    return month_name_dict[month_num]



######### ------- FEELINGS-BASED SORT ------- #########
######### ------------------------------------ #########
def sort_by_feeling(feeling):
    """Return all phrases that match either a "0" or "1" feeling."""
    
    sql = """SELECT phrase_text FROM phrases 
             WHERE polar_score = :polar_score
             """
    cursor = db.session.execute(sql, {"polar_score": feeling})
    result = cursor.fetchall()

    return result



if __name__ == '__main__':
    from server import app
    connect_to_db(app)

