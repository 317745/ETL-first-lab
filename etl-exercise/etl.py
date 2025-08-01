import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime
from sqlalchemy import create_engine, text

import warnings
warnings.filterwarnings('ignore') 

def extract(path):
    def extract_from_xml(path):
        dfs = []
        for i in range(1, 4):
            file_path = f'{path}{i}.xml'
            try:
                df = pd.read_xml(file_path)
                dfs.append(df)
            except Exception as e:
                print(f'{file_path}')
        return pd.concat(dfs)

    def extract_from_json(path):
        dfs = []
        for i in range(1, 4):
            df = pd.read_json(f'{path}{i}.json', lines=True)
            dfs.append(df)
        return pd.concat(dfs)

    def extract_from_csv(path):
        dfs = []
        for i in range(1, 4):
            df = pd.read_csv(f'{path}{i}.csv')
            dfs.append(df)
        return pd.concat(dfs)

    df_xml = extract_from_xml(path)
    df_json = extract_from_json(path)
    df_csv = extract_from_csv(path)

    return [df_csv, df_json, df_xml]

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
