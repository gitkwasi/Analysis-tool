from unittest import result
from geopy.distance import geodesic as GD
import json
from datetime import date, datetime, time
from pprint import pprint
import re

coordinates ='./coordinates.json'
order_data_str = './pivoted.json'
lmd_cycle_str = './lmd_cycle.json'




travel_speed = 50  # Travel speed in km/h
Medical_store = (6.072546206595685, -0.24863969471717115) # Coordinates of the regional medical store
lmd_weeks = [4,12,18,28,36,42]

lmd_data = open(lmd_cycle_str, 'r')
lmd_data = json.load(lmd_data)

order_data = open(order_data_str, 'r')
order_data = json.load(order_data)



# Get the facility name , district and the date of the order
# feed it to the function
# Let it return the proximity weight , LMD weight, unique facility ID



def get_LMD_weight(district= None, date= None,):
    date_of_order = datetime.strptime(date, '%Y-%m-%d')
    date_of_order_timestamp = date_of_order.timestamp()
    _, week_number, _ = date_of_order.isocalendar()
    if date_of_order < datetime.strptime('2021-01-01', '%Y-%m-%d'):
        return 0, 0
    else:
        
        lmd_dates_of_interest = [datetime.strptime(data["date"], '%Y-%m-%d') for data in lmd_data if (data['district']).lower() == district.lower() ]

        lmd_dates = [lmd_date.date() for lmd_date in lmd_dates_of_interest if lmd_date < date_of_order]
        if not lmd_dates:
            return 0, 0
        else:
            closest_lmd_date = max(lmd_dates)
            _, closest_LMD_week, _ = closest_lmd_date.isocalendar()
            LMD_weight = week_number/(closest_LMD_week + 5)
            returning_results = [LMD_weight, date_of_order_timestamp]
            return returning_results

      
    

def get_proximity_id_weight(site_id):
    data = open('weighted_coord.json', 'r')
    data_json = json.load(data)
    for dataset in data_json:
        if site_id ==  dataset["site_id"]  :
            return dataset["weight"]
        
                    

def table_generator():
    
    learning_table_list = []
    
    for item in order_data:
        learning_table_dict = {}
        # Get the required data from the order table 
        site_id = item["DELIVERY_SITE_ID"]
        district = item["HEALTH_FACILITY_LOCALITY"]
        date = item["ORDER_DATE1"]
        order_count = item["Count of ORDER_ID"]
        
        # Plug the data in the following dunctions and get the apropriate return values
        LMD_weight_time_stamp = get_LMD_weight(district= district, date= date)
        ID_prox_weight = get_proximity_id_weight(site_id= site_id)
        
        # Bluid the ML table
        learning_table_dict["id"] = site_id
        learning_table_dict["LMD_weight"] = LMD_weight_time_stamp[0]
        learning_table_dict["order_time_stamp"] = date #datetime.strptime(date, '%Y-%m-%d').timestamp()
        learning_table_dict["proximity_weight"] = ID_prox_weight
        learning_table_dict["order_count"] = order_count
        
        learning_table_list.append(learning_table_dict)
    model_table = open("MLs_table.json", 'w')
    json.dump(learning_table_list, model_table)
# delivery site ID, LMD weight , Proximity weight, number of orders, 
    



def generate_prox_weight(): 
    with open(coordinates, 'r') as f:
        data = data = json.load(f)
        result_list = []

        for sample in data:
            
            coord = (sample['latitude'], sample['longitude'])
            dist = GD(Medical_store, coord).km
            weight = (dist/travel_speed)/2
            sample.update({'weight':weight})
            sample.update({'id':id})
            result_list.append(sample)
            
    weighted_coord = open('weighted_coord.json', 'w')
    json.dump(result_list, weighted_coord)
    
if __name__ == '__main__':
    table_generator()
    # get_LMD_weight(district= "Upper West Akyem", date="2021-09-08")