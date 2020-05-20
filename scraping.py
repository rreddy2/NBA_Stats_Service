import urllib
from bs4 import BeautifulSoup
from requests import get

def checkForNone(s):
    if s.text is None:
        return str(s.b.text)
    elif s.span != None:
        return '-'
    else:
        return str(s.text)

def parseRow(row):
    elements = (row.find_all('td'))
    obj = {}
    if(len(elements) == 13):
        obj['year'] = str(elements[0].a.text[0:4])
        obj['team'] = str(elements[1].a.text)
        obj['gp'] = checkForNone(elements[2])
        obj['gs'] = checkForNone(elements[3])
        obj['mpg'] = checkForNone(elements[4])
        obj['fg'] = checkForNone(elements[5])
        obj['three'] = checkForNone(elements[6])
        obj['ft'] = checkForNone(elements[7])
        obj['rpg'] = checkForNone(elements[8])
        obj['apg'] = checkForNone(elements[9])
        obj['spg'] = checkForNone(elements[10])
        obj['bpg'] = checkForNone(elements[11])
        if elements[12].text is None:
            obj['ppg'] = str(elements[12].b.text.replace('\n',''))
        else:
            obj['ppg'] = str(elements[12].text.replace('\n',''))
    # before all stats were recorded
    elif len(elements) == 9:
        obj['year'] = str(elements[0].a.text[0:4])
        obj['team'] = str(elements[1].a.text)
        obj['gp'] = checkForNone(elements[2])
        obj['mpg'] = checkForNone(elements[3])
        obj['fg'] = checkForNone(elements[4])
        obj['ft'] = checkForNone(elements[5])
        obj['rpg'] = checkForNone(elements[6])
        obj['apg'] = checkForNone(elements[7])
        if elements[8].text is None:
            obj['ppg'] = str(elements[8].b.text.replace('\n',''))
        else:
            obj['ppg'] = str(elements[8].text.replace('\n',''))
    return obj

def parseRowCareer(row):
    elements = (row.find_all('td'))
    obj = {}
    if(len(elements) == 12):
        obj['gp'] = checkForNone(elements[1])
        obj['gs'] = checkForNone(elements[2])
        obj['mpg'] = checkForNone(elements[3])
        obj['fg'] = checkForNone(elements[4])
        obj['three'] = checkForNone(elements[5])
        obj['ft'] = checkForNone(elements[6])
        obj['rpg'] = checkForNone(elements[7])
        obj['apg'] = checkForNone(elements[8])
        obj['spg'] = checkForNone(elements[9])
        obj['bpg'] = checkForNone(elements[10])
        obj['ppg'] = str(elements[11].text.replace('\n', ''))
    elif len(elements) == 8:
        obj['gp'] = checkForNone(elements[1])
        obj['mpg'] = checkForNone(elements[2])
        obj['fg'] = checkForNone(elements[3])
        obj['ft'] = checkForNone(elements[4])
        obj['rpg'] = checkForNone(elements[5])
        obj['apg'] = checkForNone(elements[6])
        obj['ppg'] = str(elements[7].text.replace('\n', ''))
    return obj

def parseTableYearByYear(t, playoffFlag):
    rows = t.find_all('tr')
    rows = rows[1:]
    obj = []
    for row in rows:
        temp = parseRow(row)
        obj.append(temp)
    
    for item in obj:
        for field in item:
            if '*' in item[field]:
                item[field] = item[field][:-1]
            if playoffFlag == False:
                if field == 'year':
                    first_year = str(item[field][2:4])
                    second_year = str(int(first_year) + 1)
                    if len(second_year) == 1:
                        second_year = '0'+second_year
                    item[field] = first_year + '-' + second_year
    # If player was an all star then remove both rows
    # If player wasn't an all star only remove the last row
    obj[:] = [x for x in obj if x != {}]

    return obj

def parseTableCareer(t):
    rows = t.find_all('tr')
    # remove the column headers
    rows = rows[1:]
    # remove everything but the Career Totals
    if 'All-Star' in rows[len(rows)-1].find('td').text:
        rows = rows[len(rows)-2]
    else:
        rows = rows[len(rows)-1]

    obj = parseRowCareer(rows)
    return obj


def load_websites(search):
    url = "https://en.wikipedia.org/wiki/" + search
    response = get(url)

    soup = BeautifulSoup(response.text, features="html.parser")
    soup.prettify()

    links = soup.find_all('table', 'wikitable sortable')
    labels = soup.find_all('span')
    tables = []
    
    if len(links) != 0:
        for label in labels:
            if "Playoffs" in label.text:
                tables.append(links[0])
                tables.append(links[1])
        
        if len(tables) != 2:
            tables.append(links[0])

    return tables


def scrape_wiki_yearly(search):
    statsTables = load_websites(search)
    
    if len(statsTables) == 0:
        statsTables = load_websites(search + '_(basketball)')

    result = {}

    if len(statsTables) == 1:
        regularSeason = statsTables[0]
        result["regular_season"] = parseTableYearByYear(regularSeason, False)
    else:
        regularSeason = statsTables[0]
        playoffs = statsTables[1]
        result["regular_season"] = parseTableYearByYear(regularSeason, False)
        result["playoffs"] = parseTableYearByYear(playoffs, True)  

    return result

def scrape_wiki_career(search):
    statsTables = load_websites(search)
    
    if len(statsTables) == 0:
        statsTables = load_websites(search + '_(basketball)')

    regularSeason = statsTables[0]
    # check if player went to the playoffs
    playoffs = statsTables[1]

    result = {}

    result["regular_season"] = parseTableCareer(regularSeason)
    result["playoffs"] = parseTableCareer(playoffs)    

    return result
