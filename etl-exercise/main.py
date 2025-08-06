'''
/home/steven/Escritorio/ETL/etl-exercise/main.py
'''

import sqlite3
from log import log_progress
from etl import extract, transform, load_to_csv, load_to_db, get_db_connection
from db_queries import vehicles2015
from test_extractors import *


def main():
    log_file = "log_file.txt" 
    target_file = "/home/steven/Escritorio/ETL/etl-exercise/data/transformed_data.csv"
    table_name = 'used_cars_table'
    table_attribs = ['car_model','year_of_manufacture','price','fuel']
    db_name = 'Used_Cars'

    # Log the initialization of the ETL process 
    log_progress("ETL Job Started") 
    
    # Log the beginning of the Extraction process 
    log_progress("Extract phase Started") 

    # Extract
    data = extract()
    extracted_data = data.extract_all_data('/home/steven/Escritorio/ETL/etl-exercise/data')
    log_progress("Data extraction complete.")
    
    # Log the beginning of the Transformation process 
    log_progress("Transform phase Started") 

    # Transform
    transformed_data = transform(extracted_data)
    log_progress("Data transformation complete.")

    # Load
    load_to_csv(transformed_data, target_file)
    log_progress("Data loading complete.")

    load_to_db(transformed_data, get_db_connection(), table_name)
    log_progress('Data loaded to Database as table. Running the query')

    vehicles2015()
    log_progress('Post-2015 vehicles presented.')

    def run_all_tests():
        test_valid_csv_files()
        test_empty_dir()
        test_malformed_csv()
        testJsonFile()
        testJsonMalformed()
        testJsonNoField()
        xmlFileTest()
        xmlNested()
        xmlMissingData()
    
    run_all_tests()

if __name__ == "__main__":
    main()
    