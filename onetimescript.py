import os
import json
import csv
import time
from db import db, DomainRank
from sqlalchemy.orm import sessionmaker


"""
This is a one-time script to update the `sorted-top1million.txt` and `domain-rank.json` files with the latest list of top 1 million websites.

The latest `top-1m.csv` can be downloaded from Tranco List(https://tranco-list.eu/) (this CSV is updated every month). 
In this `onetimescript.py`, we read the file `/static/data/top-1m.csv`, populate data, and store it into a sorted list (`sorted-top1million.txt`) and a JSON file (`domain-rank.json`) for easy access while assessing URLs.

If you want to update the list and JSON on your local machine, follow these steps:
1. Download the `top-1m.csv` file from Tranco List (https://tranco-list.eu/)
2. Copy it to the `/static/data/` directory.
3. Execute the `onetimescript.py` file. It takes about 10-20 seconds to execute the script.

Last Executed Date With Latest top-1m.csv : 2024-03-04
"""

class OneTimeScript:
    def __init__(self):
        self.file_path = 'static/data/top-1m.csv'
        self.output_txt_path = 'static/data/sorted-top1million.txt'
        self.output_json_path = 'static/data/domain-rank.json'

    def check_file_existence(self):
        # Check if the required file exists
        if not os.path.exists(self.file_path):
            print("File does not exist.")
            print("Please add file", self.file_path)
            return False
        return True

    def create_sorted_arr_and_dict(self):
        # Create sorted list and dictionary from CSV data
        try:
            if not self.check_file_existence():
                return {'status': 'ERROR', 'msg':"File does not exist. Please add file at " + self.file_path}

            start = time.time()
            domain_data_array = []
            domain_data_dict = {}

            with open(self.file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    # domain_data_array.append(row[1])  # saving domain to list
                    domain_data_dict[row[1]] = row[0]  # saving domain : rank to dict

            # # Sort the list by domain name
            # sorted_domain_data = sorted(domain_data_array)

            # # Save the sorted data to a new file
            # with open(self.output_txt_path, 'w') as outfile:
            #     for row in sorted_domain_data:
            #         outfile.write(row + '\n')

            # Write the dictionary to the JSON file
            with open(self.output_json_path, 'w') as outfile:
                json.dump(domain_data_dict, outfile)

            end = time.time()

            print('Script Executed Successfully.')
            print('Execution Time:', round(end - start, 2), 'seconds')
            return {'status': 'SUCCESS', 'msg':'Execution Time: ' + str(round(end - start, 2)) + ' seconds'}

        except Exception as e:
            print(f"Error: {e}")
            return {'status': 'ERROR', 'msg':"Error: " + str(e)}
    

    def populate_db_from_csv(self):
        try:
            start = time.time()

            if not self.check_file_existence():
                return {'status': 'ERROR', 'msg':"File does not exist. Please add file at " + self.file_path}
            
            Session = sessionmaker(autoflush=False, bind=db.engine)
            session = Session()
            batch_size = 10000  # Adjust based on your system's capabilities
            with open(self.file_path, 'r') as file:
                reader = csv.reader(file)
                batch = []
                for index, row in enumerate(reader):
                    batch.append({'domain_name': row[1], 'rank': int(row[0])})
                    if (index + 1) % batch_size == 0:
                        db.session.bulk_insert_mappings(DomainRank, batch)
                        db.session.commit()
                        batch = []
                if batch:
                    db.session.bulk_insert_mappings(DomainRank, batch)
                    db.session.commit()
            end = time.time()
            return {'status': 'SUCCESS', 'msg':'Execution Time: ' + str(round(end - start, 2)) + ' seconds'}

        except Exception as e:
            print(f"Error: {e}")
            return {'status': 'ERROR', 'msg':"Error: " + str(e)}

        


def update_db():
    script = OneTimeScript()
    db_response = script.populate_db_from_csv()
    return db_response

def update_json():
    script = OneTimeScript()
    script_response = script.create_sorted_arr_and_dict()
    return script_response
