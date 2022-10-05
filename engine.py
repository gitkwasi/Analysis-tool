from collections import OrderedDict
import json
from pprint import pprint
from datetime import datetime, timedelta






orders = './pivoted.json'
coordinates ='./coordinates.json'




class District_engine:
    def __init__(self) -> None:
        with open(orders, 'r') as f:
            self.orders = json.load(f)
        with open(coordinates, 'r') as f:
            self.coordinates = json.load(f)

        self.facility_name = None
        self.facility_district = None
        self.start_date = None
        self.end_date = None
        self.product_type = None
        self.order_id = None
        self.package_id = None
        self.priority = None

    def calc_time_range(self,start_date, end_date):
        if start_date == '' and end_date == '':
            return None
        else:
            s_date= datetime.strptime(start_date, '%Y-%m-%d')
            e_date= datetime.strptime(end_date, '%Y-%m-%d')
            delta = e_date - s_date
            return [s_date + timedelta(days=i) for i in range(delta.days + 1)]

    def count_unqiue_dates(self,date_list):
        
        date_dict = OrderedDict()
        if not date_list:
            return None
        else:
            for date in date_list:
                frequency = date_list.count(date)
                date_dict[date] = frequency
            return date_dict

    def count_unique_facilities(self, faclities_list):
        facility_dict = {}
        for facility in faclities_list:
            frequency = faclities_list.count(facility)
            facility_dict[facility] = frequency
        return facility_dict

    
    def district_performance(self, product_variable =None, district_variable = None, start_date = None, end_date = None):
        
        
        """ This function will take the product type as a variable and 
            show district performance
        """
        
        self.facility_district = district_variable
        self.product_type = product_variable
        self.start_date = start_date
        self.end_date = end_date
        
        delta = District_engine().calc_time_range(self.start_date, self.end_date)  # Get all the dates in between the start and the end dates
       
        
        
        dates_of_interest = [] # A list containing dates objects that get passed to the count_unqiue_dates function above
        contributing_fac_list = []
        result_dict = {}
        count = 0
        
        for item in self.orders:
            date = item["ORDER_DATE1"]
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            if item["HEALTH_FACILITY_LOCALITY"] == self.facility_district and item["PRODUCT_TYPE"] == self.product_type and date_obj in delta:
                count += 1
                contributing_fac_list.append(item["HEALTH_FACILITY_NAME"])
                dates_of_interest.append(date_obj.strftime('%d/%m/%Y'))
                
        
        facility_coordinates = [coordinate for coordinate in self.coordinates if coordinate["HEALTH_FACILITY_LOCALITY"] == self.facility_district]
        unique_date_dict = District_engine().count_unqiue_dates(dates_of_interest)
        unique_facilities_dict = District_engine().count_unique_facilities(contributing_fac_list)
        result_dict['count'] = count
        result_dict['unique_date_count'] = unique_date_dict
        result_dict['district_name']= self.facility_district
        result_dict['product_type']= self.product_type
        result_dict['facilities'] = facility_coordinates
        result_dict['contributing_facilities'] = unique_facilities_dict
        pprint(unique_date_dict)
        return result_dict
        



        # Count the district name and number of unique orders in a day

        

class Facility_engine(District_engine):
    def __init__(self) -> None:
        self.facility_name: str = None
        self.start_date: str = None
        self.end_date: str = None
        

    


    
    def facility_performance(self, facility_name: str = None, product_names: list = None, start_date: str = None, end_date:str = None):
        """
        This function will take the facility name, product type, dates of interest 
        and return a dictionary in the relevant form to be used on the frontend 
        It loops through the list products and extracts from the data items that match with the desired facility 
        
        """
        
        self.start_date = start_date
        self.end_date = end_date

        result_dict = {}
        order_list = []
        unprocessed_dates = []
        processed_dictionary = {}
        
        delta = District_engine().calc_time_range(self.start_date, self.end_date)
        
        facilities_list = [facilities for facilities in District_engine().orders if  facilities['HEALTH_FACILITY_NAME'] == facility_name[0]] # List comprehension to get a list of all orders of a facility of interest
        
       
        for product in product_names:
            for items in facilities_list:
                if product == items['PRODUCT_TYPE']:
                    order_list.append(items)
            result_dict[product]=order_list
        
        
        processed_date_dictionary= None
        for key in result_dict.keys():
            product_list = result_dict[key]
            for dates in product_list:
                time_obj = datetime.strptime(dates['ORDER_DATE1'], '%Y-%m-%d')
                if time_obj in delta:
                    unprocessed_dates.append(time_obj.strftime('%d/%m/%Y'))
                processed_date_dictionary = District_engine().count_unqiue_dates(unprocessed_dates)
            
            processed_dictionary[key] = processed_date_dictionary

                
        

        pprint(processed_dictionary)
        return processed_dictionary
        

      
        