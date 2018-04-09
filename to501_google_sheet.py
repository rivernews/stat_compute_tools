
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

def check_data_have_req_teams(data_all_club_set, data_club_name_type, club_sequence):
    for club in club_sequence:
        # change to data's form - if data is abbr, change to abbr
        if data_club_name_type == 'abbr':
            req_club_abbr = abbr_dictionary[ club ]
        else:
            req_club_abbr = club
        if req_club_abbr not in data_all_club_set:
            print("Require club (abbr)", req_club_abbr, "but no player in data belongs to this club.")
            exit()


# sheet data from: https://www.kaggle.com/crawford/us-major-league-soccer-salaries/data
def get_all_players_by_sheet(year, service, data_club_name_type):
    all_players = []
    data_all_club_set = {}
    global club_sequence

    # API read 2016
    '''
    API read operation
    '''
    # target spreadsheet
    spreadsheetId = '1JGY4E7BzhetFN5EQbHmUiwKnB1t_x2DzNnGBsPjE1Zw'
    rangeName = year + '!A2:F'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        for row in values:
            all_players.append( Player(row[0] , row[4]) )
            if row[0] not in data_all_club_set:
                data_all_club_set[ row[0] ] = ""

    check_data_have_req_teams(data_all_club_set, data_club_name_type, club_sequence )

    return all_players

def get_all_teams_statistics(club_sequence, all_players):
    team_salary_avg = []
    dp_num = []
    all_num = []
    dp_salary_avg = []
    club_abbrs = []
    for club in club_sequence:
        # dependency 1: abbrv should exist in abbr.json
        # dependency 2: must have that club players, using that abbrv. *** players can have more club than our abbr.json
        salary_data = getClubMeanSalary( abbr_dictionary[club] , all_players)
        
        team_salary_avg.append(salary_data['all'])
        dp_num.append(salary_data['# of dp'])
        all_num.append(salary_data['# of all'])
        dp_salary_avg.append(salary_data['dp'])
        club_abbrs.append(abbr_dictionary[club])
    return {
        'club_abbrs': club_abbrs,
        'team_salary_avg': team_salary_avg,
        'dp_num': dp_num,
        "all_num": all_num,
        'dp_salary_avg': dp_salary_avg
    }

def main():
    # manually edit variable
    global YEAR 
    YEAR = '2015'
    global data_club_name_type
    data_club_name_type = 'abbr'

    # global variable
    service = settle_all_google_stuff()
    global abbr_dictionary 
    abbr_dictionary = readJsonToDict("abbr.json")
    global range_by_year 
    range_by_year = {
        "2017": ["42", "63"],
        "2016": [ "22", "41"],
        "2015": ["2", "21"],
    }
    global club_sequence 
    club_sequence = []
    
    '''
    API read operation
    '''
    # target spreadsheet
    spreadsheetId = '1JGY4E7BzhetFN5EQbHmUiwKnB1t_x2DzNnGBsPjE1Zw'
    rangeName = 'Salary Avg!A' + range_by_year[YEAR][0] +  ':O' + range_by_year[YEAR][1]
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        for row in values:
            club_sequence.append( row[2] )

    # organizing acquired data
    if YEAR == '2017':
        all_players = get_players_by_web()
        statistics = get_all_teams_statistics(club_sequence, all_players)
    else:
        all_players = get_all_players_by_sheet(YEAR, service, data_club_name_type)
        statistics = get_all_teams_statistics(club_sequence, all_players)
    
    '''
    API write operation
    '''
    data = []
    data.append({
        'range': 'Salary Avg!D'+ range_by_year[YEAR][0] +':H' + range_by_year[YEAR][1],
        'values': [
            statistics['club_abbrs'],
            
            statistics['all_num'],
            statistics['team_salary_avg'],
            statistics['dp_num'],
            statistics['dp_salary_avg']
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
