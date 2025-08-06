'''
/home/steven/Escritorio/ETL/etl-exercise/test_extractors.py
'''
import os
import pytest
import tempfile

from etl import *

'''
CSV
'''

def csv_files():
    contentCsv1 = 'car_model,year_of_manufacture,price,fuel\ncorolla altis,2013,10373.13,Petrol'
    contentCsv2 = 'car_model,year_of_manufacture,price,fuel\nalto 800,2017,4253.731343283582,Petrol'

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False, encoding='utf-8') as temp_file1:
        temp_file1.write(contentCsv1)
        temp_file1.flush() 
        path1 = temp_file1.name
    
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False, encoding='utf-8') as temp_file2:
        temp_file2.write(contentCsv2)
        temp_file2.flush() 
        path2 = temp_file2.name
    
    return path1, path2

def empty_directory():
    temp_dir = tempfile.TemporaryDirectory().name
    return temp_dir

def malformed_csv():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False, encoding='utf-8') as temp_file:
        temp_file.write('car_model,year_of_manufacture,price, fuel\ncorolla altis,2013,10373.13,"Petrol')
        temp_file.flush()
        path = temp_file.name
        
    return path

def test_valid_csv_files():
    csvs = csv_files()
    test = extract()
    csv1Data, csv1Ok = test.extract_from_csv(csvs[0])
    cvs2Data, csv2Ok = test.extract_from_csv(csvs[1])

    assert csv1Ok is True
    assert csv2Ok is True

def test_empty_dir():
    dir = empty_directory()
    test = extract()

    with pytest.raises(Exception) as e:
        csvData, csvOk = test.extract_from_csv(dir)
    assert str(e.value) == 'There are no files that finished with .csv'

def test_malformed_csv():
    file = malformed_csv()
    test = extract()
    csvData, csvOk = test.extract_from_csv(file)
    assert csvOk is False

'''
JSON
'''
def json_file():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False, encoding='utf-8') as jsonFile:
        jsonFile.write('''{"car_model":"ritz","year_of_manufacture":2012,"price":4626.8656716418,"fuel":"Diesel"}\n
        {"car_model":"ritz","year_of_manufacture":2011,"price":3507.4626865672,"fuel":"Petrol"}''')
        jsonFile.flush()
        path = jsonFile.name
    return path

def json_file_malformed():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False, encoding='utf-8') as jsonFile:
        jsonFile.write('''{"car_model";"ritz","year_of_manufacture":2012,"price":4626.8656716418,"fuel":"Diesel"}
        {"car_model":"ritz","year_of_manufacture":2011,"price":3507.4626865672,"fuel";"Petrol"}''')
        jsonFile.flush()
        path = jsonFile.name
    return path

def json_file_no_field():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False, encoding='utf-8') as jsonFile:
        jsonFile.write('''{"car_model";"ritz","year_of_manufacture":2012,"price":4626.8656716418}
        {"car_model":"ritz","year_of_manufacture":2011,"price":3507.4626865672,"fuel";"Petrol"}''')
        jsonFile.flush()
        path = jsonFile.name
    return path

def testJsonFile():
    file = json_file()
    test = extract()
    jsonData, jsonOk = test.extract_from_json(file)

    assert jsonOk is True
    assert list(jsonData.columns) == ['car_model','year_of_manufacture','price','fuel']

def testJsonMalformed():
    file = json_file_malformed()
    test = extract()
    jsonData, jsonOk = test.extract_from_json(file)

    assert jsonOk is False and jsonData is None

def testJsonNoField():
    file = json_file_no_field()
    test = extract()
    jsonData, jsonOk = test.extract_from_json(file)

    assert jsonOk is False

'''
XML
'''

def xml_file():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.xml', delete=False, encoding='utf-8') as file:
        file.write('''<?xml version="1.0" encoding="UTF-8" ?>
                        <root>
                            <row>
                                <car_model>corolla altis</car_model>
                                <year_of_manufacture>2013</year_of_manufacture>
                                <price>10373.134328358208</price>
                                <fuel>Petrol</fuel>
                            </row>
                            <row>
                                <car_model>etios cross</car_model>
                                <year_of_manufacture>2015</year_of_manufacture>
                                <price>6716.417910447762</price>
                                <fuel>Petrol</fuel>
                            </row>
                        </root>
                   ''')
        file.flush()
        path = file.name

    return path

def xml_file_nested():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.xml', delete=False, encoding='utf-8') as file1:
        file1.write('''<?xml version="1.0" encoding="UTF-8" ?>
                        <root>
                            <row>
                                <carmodel>
                                    <year_of_manufacture>2013</year_of_manufacture>
                                    <price>10373.134328358208</price>
                                </car_model>
                                <fuel>Petrol</fuel>
                            </row>
                            <row>
                                <car_model>etios cross</car_model>
                                <year_of_manufacture>2015</year_of_manufacture>
                                <price>6716.417910447762</price>
                                <fuel>Petrol</fuel>
                            </row>
                        </root>
                   ''')
        file1.flush()
        path1 = file1.name

    return path1

def xml_file_missing_data():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.xml', delete=False, encoding='utf-8') as file1:
        file1.write('''<?xml version="1.0" encoding="UTF-8" ?>
                        <root>
                            <row>
                                <car_model>corolla altis</car_model>
                                <year_of_manufacture>2013</year_of_manufacture>
                                <price>10373.134328358208</price>
                            </row>
                            <row>
                                <year_of_manufacture>2015</year_of_manufacture>
                                <price>6716.417910447762</price>
                                <fuel>Petrol</fuel>
                            </row>
                        </root>
                   ''')
        file1.flush()
        path1 = file1.name

    return path1


def xmlFileTest():
    file = xml_file()
    test = extract()
    xmlData, xmlOk = test.extract_from_xml(file)
    assert xmlOk is True

def xmlNested():
    file = xml_file_nested()
    test = extract()
    xmlData, xmlOk= test.extract_from_xml(file)
    assert xmlOk is False

def xmlMissingData():
    file = xml_file_missing_data()
    test = extract()
    xmlData, xmlOk = test.extract_from_xml(file)
    assert xmlOk is True