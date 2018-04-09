import requests
import re
import statistics
from bs4 import BeautifulSoup

# excel | get all abbrev

# web | for each team, get all player data (at least salary)
'''
requests doc: http://docs.python-requests.org/en/master/user/quickstart/
'''
def scrapWebData():
    url = 'https://mlsplayers.org/salary-guide/'
    r = requests.get(url)
    with open("mls_page.html", "w") as file:
        file.write(r.text)

'''
beautiful soup doc: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#problems-after-installation
'''
# read in data
def readHtmlToSoup():
    soup = ''
    with open("mls_page.html", "r") as file:
        html = file.read()
        soup = BeautifulSoup(html, 'html.parser')

    fields_html = soup.find_all('tr')[0].find_all('th')
    players_html = soup.find_all('tr')[1:]
    return {
        'fields_html': fields_html,
        'players_html': players_html
    }

def getFieldDictionary(fields_html):
    fieldClassDictionary = {}
    for a_field in fields_html:
        fieldClassDictionary[ a_field.string ] = a_field['class'][0]
    return fieldClassDictionary

class Player():
    # get column name
    def __init__(self, club, salary):
        self.club = club
        self.salary = salary

    @classmethod
    def fromSoup(cls, player_html, fieldClassDictionary):
        cls.fieldClassDictionary = fieldClassDictionary
        return cls(cls.getPlayerField(cls, "Club",player_html ), cls.getPlayerField(cls, "Base Salary", player_html ))

    def getPlayerField(self, fieldName, player_html):
        className = self.fieldClassDictionary[fieldName]
        data = player_html.find('td', {'class', className}).string
        data = re.sub("[$,]", "", data)
        return data



def getClubMeanSalary(club_abbr, players):
    club_all_salaries = [ float(player.salary) for player in players if player.club == club_abbr ]
    thresholded_salaries = []
    dp_salaries = []
    for salary in club_all_salaries:
        if salary > 504375.0:
            dp_salaries.append(salary)
            thresholded_salaries.append(504375.0)
        else:
            thresholded_salaries.append(salary)
    
    # dp may not have
    dp_avg = 0
    if len(dp_salaries) == 0:
        dp_avg = 0.0
    else:
        dp_avg = statistics.mean(dp_salaries)

    try:
        return {
            'all': statistics.mean(thresholded_salaries),
            'dp': dp_avg,
            '# of all': len(thresholded_salaries),
            '# of dp': len(dp_salaries)
        }
    except:
        print("oops! empty")
        print("club abbr =", club_abbr)
        print("club_all_salaries =", club_all_salaries)
        exit()

def get_players_by_web():
    soup_html = readHtmlToSoup()
    fields_html = soup_html['fields_html']
    players_html = soup_html['players_html']

    fieldClassDictionary = getFieldDictionary(fields_html)

    players = []
    for player_html in players_html:
        players.append( Player.fromSoup(player_html, fieldClassDictionary) )
    
    return players

def statistics_from_web_scraper():
    pass
    
# python | compute avg

if __name__ == '__main__':
    players = get_players()
    print( getClubMeanSalary('NYCFC', players) )