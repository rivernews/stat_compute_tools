
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import json
from to501_final_scrap_web import *

'''
Google Sheet API: https://developers.google.com/sheets/api/guides/values#writing_to_a_single_range
'''
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def settle_all_google_stuff():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    return service

def writeDictToJson(fileName, dictionary):
    with open(fileName, 'w') as file:
        json.dump(dictionary, file)

def readJsonToDict(fileName):
    with open(fileName, 'r') as file:
        d = json.load(file)
    return d


def main():
    service = settle_all_google_stuff()

    # target spreadsheet
    spreadsheetId = '1JGY4E7BzhetFN5EQbHmUiwKnB1t_x2DzNnGBsPjE1Zw'
    rangeName = 'Salary Avg!A42:N63'

    # load local data
    club_sequence_2017 = []
    abbr_dictionary = readJsonToDict("abbr.json")
    players_2017 = get_players()

    '''
    API read operation
    '''
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        for row in values:
            club_sequence_2017.append( row[2] )

    # organizing acquired data
    team_salary_avg = []
    dp_num = []
    dp_salary_avg = []
    club_abbrs = []
    for club in club_sequence_2017:
        salary_data = getClubMeanSalary( abbr_dictionary[club] , players_2017)
        team_salary_avg.append(salary_data['all'])
        dp_num.append(salary_data['# of dp'])
        dp_salary_avg.append(salary_data['dp'])
        club_abbrs.append(abbr_dictionary[club])

    '''
    API write operation
    '''
    print(club_abbrs)
    data = []
    data.append({
        'range': 'Salary Avg!D42:G63',
        'values': [
            club_abbrs,
            team_salary_avg,
            dp_num,
            dp_salary_avg
        ],
        'majorDimension': 'COLUMNS'
    })
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheetId, body=body).execute()
    

    
    
    
        


if __name__ == '__main__':
    main()
