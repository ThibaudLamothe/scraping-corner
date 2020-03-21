from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
import json

###### Existing functions

def read_file(file_name='data.txt'):
    """ Example of file name 'data.txt' """
    with open(file_name, "r") as fichier:
        file = fichier.read()
    return file

def read_jl_file(file_name):
    values = []
    with open(file_name, 'rb') as f:
        line = '---'
        while len(line) > 1:
            line = f.readline()
            values.append(line)
    values = values[:-1]
    values = [json.loads(i) for i in values]
    df = pd.DataFrame(values)
    return df


###### Initiating app functions

app = Flask(__name__)
api = Api(app)

FILE_PATH = '/Users/thibaud/Documents/Python_scripts/02_Projects/scraping_corner/scrapped_data/corner_test/TA_paris.jl'
FILE_PATH = '../scrapped_data/corner_test/TA_paris.jl'

###### Creating Endpoints

class Product(Resource):
    def get(self):
        file = read_file(FILE_PATH)
        nb_lines = len(file.split('\n'))
        return {'Number of lines':[nb_lines]}

class Distrib(Resource):
    def get(self):
        df_jl = read_jl_file(FILE_PATH)
        tmp = df_jl['rating'].value_counts()
        rep = tmp.to_dict()
        return rep


api.add_resource(Product, '/lines')
api.add_resource(Distrib, '/distrib')


if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8051, debug=True)
    # app.run(host='0.0.0.0', port=8051, debug=True)