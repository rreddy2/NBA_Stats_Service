import urllib
from bs4 import BeautifulSoup
from requests import get
import operator

def checkForNone(s):
	if s.text is None:
		return str(s.b.text)
	elif s.span != None:
		return '-'
	else:
		return str(s.text)

	# rows have different indexes

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

# rows have different indexes
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

def avgRowValues(elem, i, prop):
	return str((float(elem[i][prop]) + float(elem[i+1][prop]))/2)
	"""
	# remove rows where player switched teams
	def checkTeamSwitch(obj):
		result = []
		# if player only played 1 season it won't work
		if len(obj) > 1:
			for i in range(0, len(obj)):
				combineYears = False

				for j in range(i+1, len(obj)):
					if obj[i]['year'] == obj[j]['year']:
						print obj[i]
						print obj[j]
						combineYears = True
				if combineYears == False:
					result.append(obj[i])
				else:
					# check if its modern stats or old stats
					if len(obj[i]) == 9:
						# old stats
						newRow = {}
						newRow['year'] = obj[i]['year']
						newRow['team'] = str(obj[i]['team'] + '/' + obj[i+1]['team'])
						newRow['gp'] = str(int(obj[i]['gp']) + int(obj[i+1]['gp']))
						newRow['mpg'] = avgRowValues(obj,i, 'mpg')
						newRow['fg'] = avgRowValues(obj,i, 'fg')
						newRow['ft'] = avgRowValues(obj,i, 'ft')
						newRow['rpg'] = avgRowValues(obj,i, 'rpg')
						newRow['apg'] = avgRowValues(obj,i, 'apg')
						newRow['ppg'] = avgRowValues(obj,i, 'ppg')
						result.append(newRow)
					else:
						# modern stats
						newRow = {}
						newRow['year'] = obj[i]['year']
						newRow['team'] = str(obj[i]['team'] + '/' + obj[i+1]['team'])
						newRow['gp'] = str(int(obj[i]['gp']) + int(obj[i+1]['gp']))
						newRow['gs'] = str(int(obj[i]['gs']) + int(obj[i+1]['gs']))
						newRow['mpg'] = avgRowValues(obj,i, 'mpg')
						newRow['fg'] = avgRowValues(obj,i, 'fg')
						newRow['ft'] = avgRowValues(obj,i, 'ft')
						newRow['spg'] = avgRowValues(obj,i, 'spg')
						newRow['bpg'] = avgRowValues(obj,i, 'bpg')
						newRow['three'] = avgRowValues(obj, i, 'three')
						newRow['rpg'] = avgRowValues(obj,i, 'rpg')
						newRow['apg'] = avgRowValues(obj,i, 'apg')
						newRow['ppg'] = avgRowValues(obj,i, 'ppg')
						result.append(newRow)
			return result
		else:
			return obj
	"""

	# only remove the all star (if there) and career rows

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

	# Consolidate the years where player switched teams mid-season
	# and output the averages
	"""
	obj = checkTeamSwitch(obj)
	"""

	return obj

	# remove all the rows that aren't Career

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
	play = False
	if len(links) != 0:
		for label in labels:
			if "Playoffs" in label.text:
				play = True
				tables.append(links[0])
				tables.append(links[1])
				break
		if play == False:
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
		result['regular_season'] = parseTableYearByYear(regularSeason, False)
		playoffsList = parseTableYearByYear(playoffs, True)
		# Trying to fill in empty playoff years with zeros
		emptyPlayoffs = {}
		for i in range(len(result['regular_season'])):
			madePlayoffs = False
			for j in range(len(playoffsList)):
				if result['regular_season'][i]['year'][3:] == playoffsList[j]['year'][2:]:
					madePlayoffs = True
			if not madePlayoffs:
				if int(result['regular_season'][i]['year'][3:]) < 50:
					temp = '20' + str(result['regular_season'][i]['year'][3:])
				else:
					temp = '19' + str(result['regular_season'][i]['year'][3:])
				emptyPlayoffs[temp] = result['regular_season'][i]['team']
		for k in emptyPlayoffs:
			playoffsList.append({
					'ppg': '0', 'apg': '0', 'rpg': '0', 'spg': '0', 'bpg': '0', 
					'fg': '0', 'ft': '0', 'three': '0', 'team': emptyPlayoffs[k], 'gp': '0', 
					'gs': '0', 'mpg': '0', 'year': k
				})
		playoffsList.sort(key=operator.itemgetter('year'))
		result['playoffs'] = playoffsList
	return result

def scrape_wiki_career(search):
	statsTables = load_websites(search)
		
	if len(statsTables) == 0:
		statsTables = load_websites(search + '_(basketball)')

	result = {}

	if len(statsTables) == 1:
		regularSeason = statsTables[0]
		result["regular_season"] = parseTableCareer(regularSeason)
	else:
		regularSeason = statsTables[0]
		playoffs = statsTables[1]
		result["regular_season"] = parseTableCareer(regularSeason)
		result["playoffs"] = parseTableCareer(playoffs)  

	return result
