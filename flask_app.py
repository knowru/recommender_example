from flask import Flask
from flask import request
import json
import knowledge
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def recommend():
    if request.method == 'POST':
        return json.dumps({'recommendations': knowledge.run(request.get_json())})
    elif request.method == 'GET':
        return json.dumps({'status': 'ok'})

'''
curl -X POST -d '{"movie_name": "American Sniper (2014)", "k": 10}' -H "Content-Type: application/json" -H "Accept: application/json" localhost:5000
{"recommendations": [{"genres": ["Drama", "Thriller", "War"], "name": "Eye in the Sky (2015)"}, {"genres": ["Comedy"], "name": "Neighbors (2014)"}, {"genres": ["Action", "Biography", "Drama"], "name": "Lone Survivor (2013)"}, {"genres": ["Action", "Adventure", "Thriller"], "name": "Spectre (2015)"}, {"genres": ["Drama"], "name": "A Hologram for the King (2016)"}, {"genres": ["Action", "Thriller"], "name": "Blood Father (2016)"}, {"genres": ["Comedy", "Drama", "Romance"], "name": "Silver Linings Playbook (2012)"}, {"genres": [], "name": "War for the Planet of the Apes (2017)"}, {"genres": ["Horror", "Mystery"], "name": "Sinister (2012)"}, {"genres": ["Action", "Drama", "Thriller"], "name": "13 Hours: The Secret Soldiers of Benghazi (2016)"}]}
'''