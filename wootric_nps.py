# Google imports
from __future__ import print_function
from email.quoprimime import body_check
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

#Wootric imports
from re import A
from numpy import empty
import requests
import time
import csv
import datetime
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv #load environment variable file
from collections import defaultdict

from sklearn.metrics import jaccard_score

# Other function imports
import wootric_nps_sum

# Creating Google Sheets Scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

credentials = None
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = ''
service = build('sheets', 'v4', credentials=credentials)

#
#

#Create todays time in unix format and create original epoch time
current_epoch_time = int(time.time())
current_epoch_time = str(current_epoch_time)
og_epoch_time='86406'
num_days = 112
view_data = []
counter = 0

# Setting up path/env for wootric api key
env_path = Path('.') / '.env' #('.') represents current directory
load_dotenv(dotenv_path=env_path)
token = os.environ['ACCESS_TOKEN']

headers = {
    'Authorization': f'Bearer {token}'
}

#
#


# Loop through wootric survey data
while True:
    counter+=1
    if counter < num_days:
        lower_timestamp = int(current_epoch_time) #S- int(og_epoch_time)
        data_field = f"?created[lt]={current_epoch_time}&created[gt]={lower_timestamp}"
        api_base_url = "https://api.wootric.com/v1"
        endpoint_path = f"/responses/{data_field}"
        endpoint = f"{api_base_url}{endpoint_path}"
        r = requests.get(endpoint, headers=headers)
        data = r.json()
        view_data.extend(data)
        
        print(f"Day: {counter}")
        current_epoch_time = lower_timestamp

    if counter > num_days:
        break

# Initialize rows with an initial header row
rows = [['ID', 'Score', 'Text', 'Created At', 'Email', 'CSM', 'Firm ID', 'Firm Name',  '', 'All Firms', 'Average', 'Num Surveys']]

print(view_data)

# create keys for each value from the surveys
for survey in view_data:
    row = [
        survey['id'],
        survey['score'],
        survey['text'],
        survey['created_at'],
        survey['end_user']['email'],
        ' ',
        ' ',
        ' ',
        ' ',
        ' ',
        ' ',
        ' ',
    ]
    rows.append(row)



# Range, value render, date/time for Google Sheets API
range_ = "test!A1:Z3000"
value_render_option = 'UNFORMATTED_VALUE'
date_time_render_option = 'FORMATTED_STRING'


# send values to the body
body = {
    'values':rows
}

with open('client_list.csv') as loopfile:
    client_data = csv.DictReader(loopfile, dialect='excel')
    for client in client_data:
        for i in body['values']:
            if client['Email'] == i[4]:
                i[6] = client['ID']
                i[7] = client['Firm_Name']

with open('csm_list.csv') as loopfile:
    csm_data = csv.DictReader(loopfile, dialect='excel')
    for csm in csm_data:
        for i in body['values']:
            if csm['firm_id'] == i[6]:
                i[5] = csm['CSM']


        
firm_ls = []
survey_ls = []
leng_ls = []



scores = wootric_nps_sum.sum_avg(body, firm_ls, survey_ls, leng_ls)

count = 0
count_two = 0
len_firmls = len(firm_ls)

for i, row in enumerate(body['values']):
    if not i or not row:
        continue
    count+=1
    if count_two < len_firmls:
            row[9] = firm_ls[count_two]
            row[10] = survey_ls[count_two]
            row[11] = leng_ls[count_two]
            count_two+=1

        



# update values in spreadsheet
result = service.spreadsheets().values().update(
    spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_,
    valueInputOption='RAW',body=body).execute()

# output how many cells were updated
print('{0} cells updated.'.format(result.get('updatedCells')))
print('{0} cells updated.'.format(result.get('updatedCells')))
