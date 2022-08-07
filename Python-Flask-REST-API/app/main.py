from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

user='elastic'
password='4Rmpp5kea3U2pt30QT0j71Q6'  ###Specify your elasticsearch password here
es = Elasticsearch("https://localhost:9200",http_auth=(user,password),verify_certs=False) 
index_name='cities'

@app.route('/', methods=['GET'])
def get():
    city = request.args.get('city')
    #print (city)

    if city is None:
        if es.ping():
            output = "Elasticsearch is UP!"
            return jsonify(output)
        else:
            output = "Elasticsearch is DOWN!"  
            return jsonify(output)  
    else:
        output = "use search city function"

    print("Total Cities:")
    print(es.count(index=index_name))

    #city = input("Enter the city to get the population: ")

    doc = {'query': {'bool': {'must': [{'match': {'city': city}}]}}}

    #def search_elasticsearch(_es,_index_name,_doc):
    citysearch = es.search(index=index_name, body=doc)
    population = citysearch["hits"]["hits"][0]["_source"]["population"]
    output=population
    #return population        
        
    return jsonify(output)

@app.route('/', methods=['POST'])
def post():
    country = request.args.get('country')
    city = request.args.get('city')
    population= request.args.get('population')

    id=city+country

    doc = {
        'city': city,
        'country': country,
        'population': population,
    }

    #def insert_elasticsearch(_es,_index,_id,_doc):
    ret = es.index(index=index_name, id=id, body=doc)
    output = ret
    #return ret

    return jsonify(output)

@app.route('/', methods=['PUT'])
def put():
    #country = request.args.get('country')
    city = request.args.get('city')
    population= request.args.get('population')

    #id=city+country

    print("Total Cities:")
    print(es.count(index=index_name))

    matchdoc = {'query': {'bool': {'must': [{'match': {'city': city}}]}}}
    body = {'query': {'bool': {'must': [{'match': {'city': city}}]}}}
    updatedoc = {
			'doc' : {
				'population': population
			}
		}

    citysearch = es.search(index=index_name, body=matchdoc)
    current_population_id = citysearch["hits"]["hits"][0]["_id"]
    print(current_population_id)

    ret = es.update(index=index_name, id=current_population_id, body=updatedoc)
    print ('Updated Record:', ret)
    output = ret

    return output

if __name__ == "__main__":
    app.run(host='0.0.0.0')

