"""This file uses a pandas module to translate a csv into a dataframe that seeds the database."""

import os
from datetime import datetime # not sure I will call 'date'; I can parse 'datetime'

#### This code is because the pandas dataframe creates a 'numpy.int64' error
# as described in Stack Overflow here – https://stackoverflow.com/questions/50626058/psycopg2-cant-adapt-type-numpy-int64
import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)
####

# import csv 
import crud
import model
import server

# import helper function to get phrase_state_abbr
import helper

os.system('dropdb phrases')
os.system('createdb phrases')

model.connect_to_db(server.app)
model.db.create_all()

# defining this here to make it easier to notice if it needs to change
csv_filename = 'werespond_quotes04.csv'

##### Import pandas to interpret the csv #####

import pandas as pd
from sqlalchemy import create_engine


columns = [
    "phrase_text",
    "job_at_phrase",
    "interaction_id", # this is which interview
    "name",
    "age_at_phrase",
    "city_and_state", # this will be split into 'city' and 'state'
    "phrase_date", # can accept the forms 2/26/21, 02/26/21, 20210226, and will return '2021-02-26' as a string
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


#### clean dataframe and run crud functions to seed db ####
row_count = (df.shape[0]) # df.shape shows the number of rows
for row in range(row_count):
    # make a new user out of the rows of the csv
    name_list = (df.loc[row, 'name']).split(' ')
    fname = name_list[0]
    lname = name_list[1]
    email = str(df.loc[row, 'email'])
    # use crud function to ensure user is unique and has an email before adding
    user = crud.get_user_by_email(email) 
    if not user:    
        user = crud.create_user(fname, lname, email, password='***', consent=True)
    if email == 'nan':
        continue
    # make a new phrase out of the rows of the csv
    #### get, reformat, and return the date ####
    phrase_date = (df.loc[row, 'phrase_date'])
    split_date = phrase_date.split('/')
    # if year is missing, add year to indicate 2020
    if len(split_date) == 2:
        split_date.append('20')
    # format all dates in month/day/year    
    elif len(split_date) == 1:
        split_date = str(split_date)[:] # the '[:]' breaks an item into characters
        # test - print('year is', split_date[4:6], 'month is', split_date[6:8], 'day is', split_date[8:10])
        split_date = split_date[6:8], split_date[8:10], split_date[4:6] 
    # if the month is not in 2-digits, make it so         
    if len(split_date[0]) < 2 and split_date[0] != '0':
        split_date[0] = split_date[0].zfill(2) # numeric_string.zfill(total_digits) will prepend zeros up to total_digits
    # if the day is not in 2-digits, make it so
    if len(split_date) == 3 and len(split_date[1]) == 1:    
        split_date[1] = split_date[1].zfill(2)    
    # format all dates in month/day/year
    phrase_date = '/'.join(split_date)
    format = '%m/%d/%y'
    # the following code takes what I have (above) and changes to the order needed for crud.py
    phrase_date = datetime.strptime(phrase_date, format).strftime('%Y-%m-%d')
    #phrase_date = datetime.strptime(phrase_date, '%Y-%m-%d')
    
    #### get, format, and return city and state #### -- LOCATION DATA NEEDS TO BE CHANGED FOR SEED
    city_and_state = (df.loc[row, 'city_and_state']).split(', ')
    phrase_city = city_and_state[0]
    phrase_state_abbr = city_and_state[1] 
    phrase_state = helper.get_state_full_name(phrase_state_abbr)
    phrase_region = helper.get_region(phrase_state_abbr)
    
    # get other variables from the dataframe
    job_at_phrase = (df.loc[row, 'job_at_phrase'])
    age_at_phrase = (df.loc[row, 'age_at_phrase'])
    phrase_text = (df.loc[row, 'phrase_text'])
    phrase_text = phrase_text.rstrip()

    # score the phrase and add to db
    crud.create_phrase_and_score(phrase_date, phrase_city, phrase_state_abbr, phrase_state, phrase_region, job_at_phrase, age_at_phrase, phrase_text, user.user_id)

    
    # Attributes belonging to class Phrase:
    # "phrase_text"
    # "job_at_phrase"
    # "interaction_id", # this is which interview
    # "age_at_phrase"
    # "phrase_city"
    # "phrase_state_abbr"
    # "phrase_state"
    # "phrase_region"
    # "phrase_date"
    # "user_id"


# columns = [
#     "phrase_text",
#     "job_at_phrase",
#     "interaction_id", # this is which interview
#     "name",
#     "age_at_phrase",
#     "city_and_state", # this will be split into 'city' and 'state'
#     "phrase_city",
#     "phrase_state_abbr",
#     "phrase_state",
#     "phrase_region"
#     "phrase_date", # can accept the forms 2/26/21, 02/26/21, 20210226, and will return '2021-02-26' as a string
#     "email", # this is referenced from the User class
#     "user_id"
# ]    