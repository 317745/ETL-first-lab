import glob 
import pandas as pd 
import glob
import xml.etree.ElementTree as ET 

from datetime import datetime
from sqlalchemy import create_engine, text

import warnings
warnings.filterwarnings('ignore') 

class extract:
    def __init__(self):
        pass
        
    def extract_from_xml(self, path):
        if path.endswith('.xml'):
            try: 
                df = pd.read_xml(path)
                return df, True
            except Exception as e: 
                return None, False
        else:   
            dfs = []
            file_path = glob.glob('/home/steven/Escritorio/ETL/etl-exercise/data/*.xml')
            if not file_path:
                raise ValueError('There are no files that finished with .xml')
            try:
                for i in file_path:
                    df = pd.read_xml(i)
                    dfs.append(df)
                return pd.concat(dfs), True
            except Exception as e:
                    return None, False

    def extract_from_json(self, path):
        if path.endswith('.json'):
            try:
                df = pd.read_json(path, lines=True)
                return df, True
            except Exception as e:
                return None, False
        else:
            dfs = []
            file_path = glob.glob('/home/steven/Escritorio/ETL/etl-exercise/data/*.json')
            if not file_path:
                raise ValueError('There are no files that finished with .json')
            try:
                for i in file_path:
                    df = pd.read_json(i, lines=True)
                    dfs.append(df)
                return pd.concat(dfs), True
            except Exception as e:
                return None, False

    def extract_from_csv(self, path):
        if path.endswith('.csv'):
            try:
                df = pd.read_csv(path)
                return df, True
            except Exception as e:
                return None, False
        else:
            dfs = []
            file_path = glob.glob('/home/steven/Escritorio/ETL/etl-exercise/data/*.csv')
            if not file_path:
                raise ValueError('There are no files that finished with .csv')
            try:
                for i in file_path:
                    df = pd.read_csv(i)
                    dfs.append(df)
                return pd.concat(dfs), True
            except Exception as e:
                return None, False

    def extract_all_data(self, path):
        xmlData, xmlOk = self.extract_from_xml(path)
        csvData, csvOk = self.extract_from_json(path)
        jsonData, jsonOk = self.extract_from_json(path)

        if not (xmlOk and csvOk and jsonOk):
            raise ValueError('An error has happened in one or more extractions.')
        
        return xmlData, csvData, jsonData
    
def transform(data):
    df = pd.concat([data[0], data[1], data[2]])
    df['price'] = round(df['price'], 2)
    return df

def load_to_csv(df, csv_path):
    try:
        df.to_csv(csv_path)
        return 'ok'
    except Exception as e:
        return e

def get_db_connection():
    try: 
        engine = create_engine(
            'mysql+pymysql://root:juanjose@localhost:3306/Used_Cars'
        )
        return engine
    except Exception as e:
        return e
    
def load_to_db(df, sql_connection, table_name):
    try:
        df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
        return 'ok'
    except Exception as e:
        return e
