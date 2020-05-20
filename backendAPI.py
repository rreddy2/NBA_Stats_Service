import flask
from flask import request, jsonify
from scraping import scrape_wiki

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
    result = scrape_wiki(player_name)
    return jsonify(result)

app.run()