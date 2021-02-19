"""This file uses a pandas module to translate a csv into a dataframe that seeds the database."""

# pip3 freeze a requirements.txt for these imports if creating anew
import os
import json 
from random import choice, randint # probably won't use this
from datetime import date, datetime # not sure I will call 'date'; I can parse 'datetime'

##
# notes on datetime
# >>> date_str1 = "February 18, 2021"
# >>> format1 = "%B %d, %Y"
# >>> date_formatted = datetime.strptime(date_str1, format1)
# Without .strptime 
# it is of form %Y-%m-%d – ex. '2021-02-18' incl quotes
##

#import csv 
import crud
import model
import server
import score


os.system('dropdb phrases')
os.system('createdb phrases')

model.connect_to_db(server.app)
model.db.create_all()

# defining this here to make it easier to notice if it needs to change
csv_filename = 'werespond_quotes04.csv'

##### pandas to interpret the csv #####
# Imports
import pandas as pd
from sqlalchemy import create_engine


columns = [
    "phrase_text",
    "job_at_phrase",
    "interaction_id", # this is which interview
    "name",
    "age_at_phrase",
    "city_and_state", # this is actually city and state
    "phrase_date",
    "email"
]

# Load in the data
df = pd.read_csv(
    csv_filename, # passed in above; otherwise, this would be a filename in quotes
    names=columns
)

##### Instantiate sqlachemy.create_engine object #####
# Usual form is: 
# engine = create_engine('postgresql://postgres:password@localhost:5432/phrases')
# however, it will pass in default args for what is not provided

engine = create_engine('postgresql:///phrases')

# Save the data from dataframe to
# postgreSQL table "phrases_dataset"
df.to_sql(
    'phrases_dataset', # this name needs to be different from the tablename (I think it is the df name)
    engine,
    index=False, # Not copying over the index
    if_exists='append' # this code suggested by Paresa Morton
)

#### clean the df before creating db ####

# get unique emails and unique users

# dup =df.query('phrase_city == "Columbus"', inplace = True) 

#### run crud functions to create data from the dataframe ####



row_count = (df.shape[0]) # df.shape shows the number of rows
for row in range(row_count):
    # make a new user out of the rows of the csv
    name_list = (df.loc[row, 'name']).split(' ')
    fname = name_list[0]
    lname = name_list[1]
    email = str(df.loc[row, 'email'])
    # use crud function to ensure user is unique and has an email before adding
    user = crud.get_user_by_email(email) 
    if not user and email != 'nan':    
        crud.create_user(fname, lname, email, password='***', consent=True)

    # make a new phrase out of the rows of the csv
    phrase_date = (df.loc[row, 'phrase_date'])
    print(phrase_date)
    
    ### reformat the date
    
    city_and_state = (df.loc[row, 'city_and_state']).split(', ')
    phrase_city = city_and_state[0]
    phrase_state = city_and_state[1] 
    job_at_phrase = (df.loc[row, 'job_at_phrase'])
    age_at_phrase = (df.loc[row, 'age_at_phrase'])
    phrase_text = (df.loc[row, 'phrase_text'])
    # score the phrase and add to db
    crud.create_phrase_and_score(phrase_date, phrase_city, phrase_state, job_at_phrase, age_at_phrase, phrase_text, True)

    # "phrase_text",
    # "job_at_phrase",
    # "interaction_id", # this is which interview
    # "name",
    # "age_at_phrase",
    # "city_and_state", # this is actually city and state
    # "phrase_date",
    # "email"