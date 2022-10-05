from flask import Flask 
from flask import request, render_template, jsonify
import json
from .engine import District_engine, Facility_engine

app = Flask(__name__)




@app.route('/')
def get_district_product():

    if request.args.get('product_variable') == None or request.args.get('district_variable')== None and request.args.get("start_date")== None and  request.args.get("end_date")== None:
        return render_template('base.html', results = None, district_product = None, facility_product =None)
    else:    
        district = request.args.get("district_variable")
        product = request.args.get("product_variable")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        returned_result = District_engine().district_performance(product, district, start_date, end_date)
        return render_template('base.html', results = returned_result, district_product = None, facility_product =None)


@app.route("/facility")
def get_facility_product():
    """
    This  function routes the request to the  Facility_engine for processing and receives the output as a 
    dictionary that is trasnported to the frontend for rendering
    """
    
    product_names=  request.args.getlist('product')
    facility_name =  request.args.getlist('facility_variable')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    returned_results = Facility_engine().facility_performance(facility_name=facility_name, product_names=product_names, start_date=start_date, end_date=end_date)

    return render_template('base.html' , results = None, district_product = None, facility_product = returned_results)
    
        