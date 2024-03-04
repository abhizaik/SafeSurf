import json
import csv
import time
import os


"""
This is a one-time script to update the `sorted-top1million.txt` and `domain-rank.json` files with the latest list of top 1 million websites.

The latest `top-1m.csv` can be downloaded from [Tranco List](https://tranco-list.eu/) (this CSV is updated every month). 
In this `onetimescript.py`, we read the file `/static/data/top-1m.csv`, populate data, and store it into a sorted list (`sorted-top1million.txt`) and a JSON file (`domain-rank.json`) for easy access while assessing URLs.

If you want to update the list and JSON on your local machine, follow these steps:
1. Download the `top-1m.csv` file from Tranco List (https://tranco-list.eu/)
2. Copy it to the `/static/data/` directory.
3. Execute the `onetimescript.py` file. It takes about 10-20 seconds to execute the script.

Last Executed Date With Latest top-1m.csv : 2024-03-04
"""


def create_sorted_arr_and_dict():

    try:

        if not os.path.exists('static/data/top-1m.csv'):   
            print("File does not exist.")
            print("Please add file static/data/top-1m.csv")
            return 0

        start = time.time()
        domain_data_array = []
        domain_data_dict = {}

        with open('static/data/top-1m.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                domain_data_array.append(row[1]) # saving domain to list
                domain_data_dict[row[1]] = row[0] # saving domain : rank to dict

        # Sort the list by domain name
        sorted_domain_data = sorted(domain_data_array)

        # Open the file in write mode to clear the contents
        with open('static/data/sorted-top1million.txt', 'w') as outfile:
            pass

        # Save the sorted data to a new file
        with open('static/data/sorted-top1million.txt', 'w') as outfile:
            for row in sorted_domain_data:
                outfile.write(row + '\n')

        # Open the file in write mode to clear the contents
        with open('static/data/domain-rank.json', 'w') as outfile:
            pass

        # Write the dictionary to the file
        with open('static/data/domain-rank.json', 'w') as outfile:
            json.dump(domain_data_dict, outfile)

        end = time.time()

        print('Script Executed Successfully.')
        print('Execution Time : ', round(end - start,2),'seconds')

    except Exception as e:
        print(f"Error: {e}")


create_sorted_arr_and_dict() 
