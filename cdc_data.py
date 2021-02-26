#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
import model
# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata('data.cdc.gov', '42GjiuP7dzylFFUbnbhnyEIyt')

# App Token = '42GjiuP7dzylFFUbnbhnyEIyt'
# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cdc.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("9mfq-cb36", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)


row_count = (results_df.shape[0]) # df.shape shows the number of rows
print(row_count)
print(results_df)
print(results_df.columns)
print(results_df.columns['submission_date'])


##### ----- INFO ABOUT THIS DATAFRAME ----- #####
# [15 columns]
# column headings are:
# Index(['submission_date', 'state', 'tot_cases', 'conf_cases', 'prob_cases',
#        'new_case', 'pnew_case', 'tot_death', 'conf_death', 'prob_death',
#        'new_death', 'pnew_death', 'created_at', 'consent_cases',
#        'consent_deaths'],
#        dtype='object')