## IMPORTS ######
import sys, requests, csv, math
import unicodecsv as csv_u

## HELPER FUNCTIONS #####
def read_price_data_csv():
    with open('./preprocessed/price_data.csv') as file:
        data = [{k: v for k, v in row.items()} for row in csv.DictReader(file, skipinitialspace=True)]
     
    return  data

def read_exist_data_csv():
    with open('./preprocessed/project_data_subset_5.csv') as file:
        data = [{k: v for k, v in row.items()} for row in csv.DictReader(file, skipinitialspace=True)]
     
    return data

def combine_data(price_data, subset_data):
    all_data = []
    for record in subset_data:
        for price in price_data:
            if record['app_id'] == price['app_id']:
                record['in_app_purchase'] = price['in_app_purchase']
                all_data.append(record)
    return all_data
    
def write_data_csv(data):
    keys = data[0].keys()
    with open('./processed/project_data_user_count_5.csv', 'wb') as output_file:
        dict_writer = csv_u.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

## MAIN FUNCTION #####
def main(arg):
    # import price data
    price_data = read_price_data_csv()
    # import all data
    subset_data = read_exist_data_csv()
    # combine data
    all_data = combine_data(price_data, subset_data)
    # write data to csv
    write_data_csv(all_data) 

    

if __name__ == "__main__":
    main(sys.argv)

