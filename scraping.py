import urllib
from bs4 import BeautifulSoup
from requests import get

def checkForNone(s):
    if s.string is None:
        return str(s.b.string)
    elif s.span != None:
        return '-'
    else:
        return str(s.string)

def parseRow(row):
    elements = (row.find_all('td'))
    obj = {}
    if(len(elements) == 13):
        obj['year'] = str(elements[0].a.string[0:4])
        obj['team'] = str(elements[1].a.string)
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

        if elements[12].string is None:
            obj['ppg'] = str(elements[12].b.string.replace('\n',''))
        else:
            obj['ppg'] = str(elements[12].string.replace('\n',''))
    return obj

def parseTable(t):
    rows = t.find_all('tr')
    rows = rows[1:]
    obj = []
    for row in rows:
        temp = parseRow(row)
        obj.append(temp)
    
    for item in obj:
        for field in item:
            #print(item)
            if '*' in item[field]:
                item[field] = item[field][:-1]
            if field == 'year':
                first_year = str(item[field][2:4])
                second_year = str(int(first_year) + 1)
                if len(second_year) == 1:
                    second_year = '0'+second_year
                item[field] = first_year + '-' + second_year
    obj = obj[:-2]
    return obj

def load_websites(search):
    url = "https://en.wikipedia.org/wiki/" + search
    response = get(url)

    soup = BeautifulSoup(response.text, features="html.parser")
    soup.prettify()

    links = soup.find_all('table', 'wikitable')
    tables = []

    for link in links:
        thead = link.find_all('abbr')
        if len(thead) != 0:
            tables.append(link)
    return tables


def scrape_wiki(search):
    statsTables = load_websites(search)
    
    if len(statsTables) == 0:
        statsTables = load_websites(search + '_(basketball)')

    regularSeason = statsTables[0]
    playoffs = statsTables[1]

    result = {}
    result["regular_season"] = parseTable(regularSeason)
    result["playoffs"] = parseTable(playoffs)    

    return result