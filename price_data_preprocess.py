## IMPORTS ######
import sys, requests, csv, math
import unicodecsv as csv_u
from datetime import date


## VARIABLES ####### 
api = 'https://itunes.apple.com/lookup?id='
d1 = date(2019, 11, 23)


## HELPER FUNCTIONS
def read_data_csv():
    """Generates a list of dictionaries with  App Ids as keys
    Returns: 
        data (list): list of dictionaries.
    """
    with open('url_data_v2.csv') as file:
        data = [{k: v for k, v in row.items()} for row in csv.DictReader(file, skipinitialspace=True)]
     
    return data

def call_apple_api(id):
    app_data = {}
    try:
        dataset = requests.get(api + id)
        dataset_json = dataset.json()
        dataset_format = dataset_json['results'][0]
        if dataset_format['primaryGenreId'] == 6014:
            app_data['app_id'] = id
            app_data['url'] = dataset_format['trackViewUrl']
    except:
        'error'
    return app_data

def call_apple_website(id, url):
    price_data = {}
    try:
        webpage = requests.get(url)
        page_text = webpage.text
        price_data['app_id'] = id
        if "app-header__list__item--in-app-purchase" in page_text:
            price_data['in_app_purchase'] = 1
        else:
            price_data['in_app_purchase'] = 0
    except:
        'error'
    return price_data

def request_url(data):
    combined_data = []
    for app_dict in data:
        api_data = call_apple_api(app_dict['ID'])
        if bool(api_data):  
            print(api_data['app_id'])
            combined_data.append(api_data)
    return combined_data

def request_price(data):
    combined_price_data = []
    for url_dict in data:
        price_data = call_apple_website(url_dict['app_id'], url_dict['url'])
        if bool(price_data): 
            print(price_data['app_id'])
            combined_price_data.append(price_data)
    return combined_price_data

def write_data_csv(data):
    """Writes list of dictionaries to CSV
    Params:
        data (list):  list of all applications and features
    """
    keys = data[0].keys()
    with open('price_data_v2.csv', 'wb') as output_file:
        dict_writer = csv_u.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


## MAIN FUNCTION #####
def main(arg):
    # import app ids from dataset
    id_data = read_data_csv()
    # retrieve urls from data
    # url_data = request_url(id_data)
    # retrieve price information via url data
    price_data = request_price(id_data)
    # write data to csv
    write_data_csv(price_data) 

    

if __name__ == "__main__":
    main(sys.argv)

