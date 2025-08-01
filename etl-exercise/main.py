import sqlite3
from log import log_progress
from etl import extract, transform, load_to_csv, load_to_db


def main():
    log_file = "log_file.txt" 
    target_file = "transformed_data.csv"
    table_attribs = ['car_model','year_of_manufacture','price','fuel']
    db_name = 'Used_Cars.db'

    # Log the initialization of the ETL process 
    log_progress("ETL Job Started") 
    
    # Log the beginning of the Extraction process 
    log_progress("Extract phase Started") 

    # Extract
    extracted_data = extract()
    log_progress("Data extraction complete.")
    
    # Log the beginning of the Transformation process 
    log_progress("Transform phase Started") 

    # Transform
    transformed_data = transform(extracted_data)
    log_progress("Data transformation complete.")

    # Load
    load_to_csv(transformed_data, target_file)
    log_progress("Data loading complete.")

    load_to_db(transformed_data, sql_connection, table_name)
    log_progress('Data loaded to Database as table. Running the query')



if __name__ == "__main__":
    main()
