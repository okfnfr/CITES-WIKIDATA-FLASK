from flask import Flask, request, render_template, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata import WIKIDATA_REQUEST1, WIKIDATA_REQUEST2
from wikidata_citesid import WIKIDATA_REQUEST1ID, WIKIDATA_REQUEST2ID
from cites import CITES1, CITES2, CITES_KEY, CITES2_LEGISLATION
import requests
import json
from urllib.error import HTTPError

app = Flask(__name__)

endpoint_url = "https://query.wikidata.org/sparql"
def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        result = sparql.query().convert()
        print (result)
        return result
    except HTTPError as err:
        print(err.code)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['post'])
def search():
    if request.method == 'POST' :

        search = request.form['search']
        search = search.lower()
        print(search)

        #Apply Wikidata request
        wikidata_request_send = WIKIDATA_REQUEST1 + "\"" + search + "\"" + WIKIDATA_REQUEST2
        print(wikidata_request_send)

        results = get_results(endpoint_url, wikidata_request_send)

        #Filtering duplicates
        listIdsSPECIES = []
        listResults = []
        try:
            results = results["results"]["bindings"]
            for result in results:
                id = result["identifiantSPECIES"]["value"]
                print(id)
                if id not in listIdsSPECIES:
                    listIdsSPECIES.append(id)
                    listResults.append(result)
                    # print(result)
        except:
            print("Unexpected error")

        return render_template('index.html', items = listResults)

@app.route('/details/<int:citesid>')
def cites(citesid):

    # Apply Wikidata request
    wikidata_request_send = WIKIDATA_REQUEST1ID + "\"" + str(citesid) + "\"" + WIKIDATA_REQUEST2ID
    print(wikidata_request_send)

    results = get_results(endpoint_url, wikidata_request_send)
    nom = ''
    wikidataid = ''
    image = ''
    nomscientifique = ''
    rangtaxinomique = ''
    taxonsuperieur = ''

    # Filtering duplicates
    listIdsSPECIES = []
    listResults = []

    try:
        results = results["results"]["bindings"]
        for result in results:

            id = result["identifiantSPECIES"]["value"]
            print(id)
            if id not in listIdsSPECIES:
                listIdsSPECIES.append(id)
                listResults.append(result)
                # print(result)
    except:
        print("Unexpected error")

    if len(listIdsSPECIES) == 0:
        return render_template('details.html')

    try:
        nom = results[0]['itemLabel']['value']
        wikidataid = results[0]['item']['value']
        wikidataid = wikidataid.replace('http://www.wikidata.org/entity/', '')
        image = results[0]['image']['value']
        nomscientifique = results[0]['nomscientifique']['value']
        rangtaxinomique = results[0]['rangtaxinomiqueLabel']['value']
        taxonsuperieur = results[0]['taxonsuperieurLabel']['value']

    except:
        print("Unexpected error")


    # CITES distribution
    req = CITES1 + str(citesid) + CITES2
    print (req)
    result = requests.get(req, headers={'X-Authentication-Token': CITES_KEY})
    print(result.status_code)
    wjdata = json.loads(result.text)
    #print(wjdata)

    listedistribution = []
    for val in wjdata:

        # name, iso_code2, tags
        if len(val['tags']) == 0:
            name = str(val['name'])
            code = str(val['iso_code2'])
            xx = { 'name': name, 'code':  code}
            listedistribution.append(xx)

    # CITES legislation
    reqlegislation = CITES1 + str(citesid) + CITES2_LEGISLATION

    resultlegislation = requests.get(reqlegislation, headers={'X-Authentication-Token': CITES_KEY})

    wjdatalegislation = json.loads(resultlegislation.text)
    appendix = ''
    listelegislation = []
    for val in wjdatalegislation['cites_suspensions']:

        # name, iso_code2, tags
        name = str(val['geo_entity']['name'])
        code = str(val['geo_entity']['iso_code2'])
        xx = { 'name': name, 'code':  code}
        iscurrent = str(val['is_current'])
        #if iscurrent == "True":
        listelegislation.append(xx)

    try:
        val = wjdatalegislation['cites_listings']
        appendix = val[0]['appendix']
    except:
        appendix = ''
        print("Unexpected error")

    return render_template('details.html',
                           citesid=citesid,
                           nom=nom,
                           wikidataid=wikidataid,
                           image=image,
                           nomscientifique=nomscientifique,
                           rangtaxinomique=rangtaxinomique,
                           taxonsuperieur=taxonsuperieur,
                           listedistribution = listedistribution,
                           appendix=appendix,
                           listelegislation=listelegislation)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run()
