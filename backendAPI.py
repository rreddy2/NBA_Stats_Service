import flask
from flask import request, jsonify
from playerStatsScraping import scrape_wiki_yearly,scrape_wiki_career

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to get career averages for both regular season and 
# playoffs in one JSON object
@app.route('/api/v1/CareerYearByYear', methods=['GET'])
def api_CareerYearByYear():
    player_name = request.args.get('name')
    result = scrape_wiki_yearly(player_name)
    return jsonify(result)

# A route to get career totals for both regular season and
# playoffs in one JSON object
@app.route('/api/v1/CareerTotals', methods=['GET'])
def api_CareerTotals():
    player_name = request.args.get('name')
    result = scrape_wiki_career(player_name)
    return jsonify(result)


app.run()