from opensky_api import OpenSkyApi
from datetime import datetime
from elasticsearch import Elasticsearch
import threading
import configparser
import json
import statevector

def index_time():
    return datetime.today().strftime('%Y-%m-%d')

def update_indexes():
    config = configparser.ConfigParser()
    config.read('.config')

    es = Elasticsearch(hosts=[config['elasticsearch']['host']])
    mapping = '''
        {
            "mappings" : {
              "properties" : {
                "location" : {
                  "type" : "geo_point"
                }
              }
            }
        }
    '''
    # Create flight log index if it does not exist
    flightlog_iname = config['index_names']['flightlogs'] + '-' + index_time()
    if not es.indices.exists(index=flightlog_iname):
        es.indices.create(index=flightlog_iname, body=mapping)

def ingest():
    threading.Timer(30.0, ingest).start()

    config = configparser.ConfigParser()
    config.read('.config')

    update_indexes()

    api = OpenSkyApi()
    states = api.get_states()

    es = Elasticsearch(hosts=[ config['elasticsearch']['host'] ])
    flightlog_iname = config['index_names']['flightlogs'] + '-' + index_time()

    for s in states.states:
        sv_d = statevector.sv_to_dict(s)
        if (sv_d):
            es.index(index=flightlog_iname, body=json.dumps(sv_d))

if __name__ == '__main__':
    ingest()
