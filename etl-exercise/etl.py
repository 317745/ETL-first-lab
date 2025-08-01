import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime
from sqlalchemy import create_engine, text

import warnings
warnings.filterwarnings('ignore') 

def extract_data(path):
    def extract_from_xml(path):
        dfs = []
        for i in range(1, 4):
            dfs.append(pd.read_xml(f'etl-exercise/data/used_car_prices{i}.xml'))
        return pd.concat(dfs)

    def extract_from_json(path):
        dfs = []
        for i in range(1, 4):
            dfs.append(pd.read_json(f'etl-exercise/data/used_car_prices{i}.json', lines=True))
        return pd.concat(dfs)

    def extract_from_csv(path):
        dfs = []
        for i in range(1, 4):
            dfs.append(pd.read_csv(f'etl-exercise/data/used_car_prices{i}.csv'))
        return pd.concat(dfs)

    df_xml = extract_from_xml(path)
    df_json = extract_from_json(path)
    df_csv = extract_from_csv(path)

    return [df_csv, df_json, df_xml]

def transform_data(data): 
    return pd.concat([data[0], data[1], data[2]])

def load_to_csv(df, csv_path):
    try:
        df.to_csv(csv_path)
        return 'ok'
    except Exception as e:
        return 'not ok'

def load_to_database(df, sql_connection, table_name):
    try:
        df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
        return 'oki'
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

def fetch_all_cars():
    try:
        engine = get_db_connection()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM used_cars_table")).fetchall()
            return result
    except Exception as e:
        return e

data_extracted = extract_data('etl-exercise/data/used_car_prices')
data_transformed = transform_data(data_extracted)
csv_status = load_to_csv(data_transformed, 'etl-exercise/data/cars.csv')
db_status = load_to_database(data_transformed, get_db_connection(), 'used_cars_table')
print(fetch_all_cars())
