## IMPORTS ######
import sys, requests, csv, math
import unicodecsv as csv_u
from datetime import date


## VARIABLES ####### 
api = 'https://itunes.apple.com/lookup?id='
d1 = date(2019, 11, 24)


## HELPER FUNCTIONS
def read_data_csv():
    """Generates a list of dictionaries with  App Ids as keys
    Returns: 
        data (list): list of dictionaries.
    """
    with open('./preprocessed/id_data_combined.csv') as file:
        data = [{k: v for k, v in row.items()} for row in csv.DictReader(file, skipinitialspace=True)]
     
    return data

def en(lang_array):
    """Checks if the list of app langauges incldues english
    Parms:
        lang_array (array): list of languages application available
    Returns: 
        0 (int): english not present
        1 (int): english present.
    """
    if 'EN' in lang_array:
        return 1
    return 0

def calc_time(date_string):
    """Calculates the duration of time between two dates
    Params:
        date_string (string): date in form of string
    Returns: 
        d.days (int): number of days lapsed
    """
    d0 = date(int(date_string[:4]), int(date_string[5:7].lstrip("0")), int(date_string[8:10]))
    d = d1 - d0
    return d.days

def call_apple_api(id):
    """Calls Apple API and returns a dictionary of features
    Params:
        id (string): application id
    Returns: 
        app_data (dictionary): dictionary of features for each app
    """
    app_data = {}
    try:
        dataset = requests.get(api + id)
        dataset_json = dataset.json()
        dataset_format = dataset_json['results'][0]
        if dataset_format['primaryGenreId'] == 6014 and dataset_format['userRatingCount'] > 4:
            app_data['app_id'] = id
            app_data['user_rating_count'] = dataset_format['userRatingCount']
            app_data['price'] = dataset_format['price']
            app_data['age_rating'] = int(dataset_format['trackContentRating'][:-1])
            app_data['language_en'] = en(dataset_format['languageCodesISO2A'])
            app_data['language_sum'] = len(dataset_format['languageCodesISO2A'])
            app_data['size'] = int(dataset_format['fileSizeBytes'])/1000000
            app_data['release_date'] = calc_time(dataset_format['releaseDate'])
            app_data['last_update'] = calc_time(dataset_format['currentVersionReleaseDate'])
            app_data['supported_devices'] = len(dataset_format['supportedDevices'])
            app_data['genres'] = list(map(int, dataset_format['genreIds']))
            app_data['average_user_rating'] = math.ceil(dataset_format['averageUserRating'])
            if bool(dataset_format['averageUserRatingForCurrentVersion']):
                app_data['rating_current_version'] = math.ceil(dataset_format['averageUserRatingForCurrentVersion'])
                app_data['user_rating_count_current_version'] = dataset_format['userRatingCountForCurrentVersion']
            else:
                app_data['rating_current_version'] = 5
                app_data['user_rating_count_current_version'] = 23
           
    except:
        'error'

    return app_data

def add_api_data(data):
    """Iterates through app IDS to call app
    Params:
        data (dictionary):  dictionary of app ids to be cal api
    Returns: 
        combined_data (list): list of all applications and features
    """
    combined_data = []
    for app_dict in data:
        api_data = call_apple_api(app_dict['ID'])
        if bool(api_data):
            print(api_data['app_id']) 
            combined_data.append(api_data)
    return combined_data

def write_data_csv(data):
    """Writes list of dictionaries to CSV
    Params:
        data (list):  list of all applications and features
    """
    keys = data[0].keys()
    with open('project_data_subset.csv', 'wb') as output_file:
        dict_writer = csv_u.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


## MAIN FUNCTION #####
def main(arg):
    # import app ids from dataset
    id_data = read_data_csv()
    # retrieve add data from api
    combined_data = add_api_data(id_data)
    # write data to csv
    write_data_csv(combined_data)

    

if __name__ == "__main__":
    main(sys.argv)

