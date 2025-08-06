from etl import get_db_connection
from sqlalchemy import text 

def vehicles2015():
    engine = get_db_connection()
    with engine.connect() as conn:
        vehicles = conn.execute(text('''
                        SELECT * 
                        FROM used_cars_table
                        WHERE year_of_manufacture > 2015
                          ''')).fetchall()
        for vehicle in vehicles:
            model = vehicle[0]
            year = vehicle[1]
            price = vehicle[2]
            fuel = vehicle[3]
            #print(f'Vehicle model: {model}, year: {year}, fuel: {fuel} and price: {price}')