"""This file looks at CDC Data, furnished through Socrata, with a Pandas dataframe."""

# !/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy
import pandas as pd
from sodapy import Socrata
import model



# to get the global_var for token, import os and call 'environ'
# the token in stored as the value of 'SOCRATA_APP_TOKEN' key
# this value was set up through an export in the secrets.sh file

import os
client = Socrata('data.cdc.gov', os.environ['SOCRATA_APP_TOKEN'])
# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cdc.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("9mfq-cb36", limit=10000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)


row_count = (results_df.shape[0]) # df.shape shows the number of rows
#print(row_count)
#print(results_df)
#print(results_df.columns)

for row in range(row_count):
    submission_date = results_df.loc[row, 'submission_date']
    while submission_date[0:10] == '2021-02-20': 
        print(submission_date[0:10], results_df.loc[row, 'state'], results_df.loc[row, 'tot_death'])
        break
    # return looks like: 
    # 2021-02-20 WY 662
    # 2021-02-20 NH 1153
    # 2021-02-20 KY 4426
    # 2021-02-20 IN 12336
    # 2021-02-20 CA 48825
    # 2021-02-20 AZ 15480
    # 2021-02-20 WA 4822
    # 2021-02-20 NC 10896
    # 2021-02-20 FSM 0
    # 2021-02-20 NJ 22834
    # 2021-02-20 ND 1438
    #etc ... there are 25K rows to look through

# for 'submission_date' -- make a query
# print(results_df.query('submission_date[0:10] == 2021-02-20'))

#############
#Working on querying the db efficiently so as to return a few stats about a particular date.
#############

##### ----- INFO ABOUT THIS DATAFRAME ----- #####
# [15 columns]
# column headings are:
# Index(['submission_date', 'state', 'tot_cases', 'conf_cases', 'prob_cases',
#        'new_case', 'pnew_case', 'tot_death', 'conf_death', 'prob_death',
#        'new_death', 'pnew_death', 'created_at', 'consent_cases',
#        'consent_deaths'],
#        dtype='object')