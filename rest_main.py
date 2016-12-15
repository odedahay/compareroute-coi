import webapp2
import mimetypes
import os
import time
from datetime import datetime
import base64
import urlparse
from httplib import HTTPResponse

import logging
import json
import itertools
import pickle

import operator

from operator import itemgetter
from collections import defaultdict

import urllib
# ------ sorting -----
from handlers import sorting, sorting_prep

from model.user_account import UserAccount
from model.admin_account import postalRecordDB

from google.appengine.api import taskqueue


'''
{
  "status": "ok",
  "data_result": [
    {
      "vehicle_details": {
        "grp_truck": [
          [
            "AAA"
          ]
        ]
      },
      "required_fields": {
        "priority_capacity": "true",
        "starting_postal": "461051",
        "propose_result": [
          [
            [
              "460102",
              "Order10",
              1,
              1
            ],
            [
              "469001",
              "Order01",
              1,
              1
            ],
            [
              "431011",
              "Order09",
              1,
              1
            ],
            [
              "098585",
              "Order05",
              1,
              1
            ],
            [
              "109680",
              "Order06",
              1,
              1
            ],
            [
              "278986",
              "Order08",
              1,
              1
            ],
            [
              "596740",
              "Order04",
              1,
              1
            ],
            [
              "596937",
              "Order03",
              1,
              1
            ],
            [
              "760450",
              "Order02",
              1,
              1
            ],
            [
              "560405",
              "Order07",
              1,
              1
            ],
            [
              "461051",
              0,
              0,
              0
            ]
          ]
        ],
        "has_return": "true"
      },
      "total_summary_saving": {
        "propose_distance": 88.685,
        "total_savings": 25.637263122589303,
        "current_distance": 119.26
      },
      "geo_code_latlng": {
        "latlng_array": [
          [
            [
              "1.334002",
              "103.937209"
            ],
            [
              "1.322995",
              "103.922194"
            ],
            [
              "1.30161",
              "103.882607"
            ],
            [
              "1.264241",
              "103.822287"
            ],
            [
              "1.280195",
              "103.815126"
            ],
            [
              "1.31153",
              "103.795481"
            ],
            [
              "1.34211",
              "103.767283"
            ],
            [
              "1.337952",
              "103.765192"
            ],
            [
              "1.422128",
              "103.844128"
            ],
            [
              "1.361599",
              "103.853662"
            ],
            [
              "1.323477",
              "103.942084"
            ]
          ]
        ]
      }
    }
  ]
}
'''

def checkInRequest(field, request):
    # if myconstants.DEBUG:
    #     logging.debug(field)

    if field in request:
        return request[field], []
    else:
        return None, [field + " missing"]

"""
{
    "starting_postal": "461051",
    "order_details": [
                       ["369974", "Order01", 1],
                        ["760450", "Order02", 1],
                        ["596937", "Order03", 1],
                        ["596740", "Order04", 1],
                        ["560405", "Order05", 1],
                        ["543262", "Order06", 1],
                        ["520156", "Order07", 1],
                        ["469001", "Order08", 1],
                        ["760450", "Order09", 1],
                        ["596937", "Order10", 1],
                        ["596740", "Order11", 1],
                        ["098585", "Order12", 1],
                        ["109680", "Order13", 1],
                        ["189637", "Order14", 1]
                    ],
    "truck_details":
    	[
      		{
	           "type_of_truck": "AAA",
	           	"truck_capacity": 5,
				"num_of_truck": 1
	      	},
	      	{
	           "type_of_truck": "BBB",
	           	"truck_capacity": 5,
				"num_of_truck": 1
	      	}

      	],
    "has_return": "true",
    "priority_capacity": "true",
    "time_windows": "false"
}

# For With Time Windows:

{
    "starting_postal": "461051",
    "order_details": [
                        ["369974", "Order01", 1, "09:00:00", "12:00:00"],
                        ["760450", "Order02", 1, "07:00:00", "8:00:00"],
                        ["596937", "Order03", 1, "13:00:00", "14:00:00"],
                        ["596740", "Order04", 1, "10:00:00", "11:00:00"],
                        ["560405", "Order05", 1, "09:30:00", "10:20:00"],
                        ["543262", "Order06", 1, "15:00:00", "18:00:00"],
                        ["520156", "Order07", 1, "14:00:00", "17:00:00"],
                        ["469001", "Order08", 1, "09:00:00", "12:00:00"],
                        ["760450", "Order09", 1, "11:00:00", "11:30:00"],
                        ["596937", "Order10", 1, "13:00:00", "15:00:00"],
                        ["596740", "Order11", 1, "16:00:00", "17:00:00"],
                        ["098585", "Order12", 1, "13:00:00", "15:00:00"],
                        ["109680", "Order13", 1, "16:00:00", "17:00:00"],
                        ["189637", "Order14", 1, "15:00:00", "18:00:00"]

                    ],
    "truck_details":
    	[
      		{
	           "type_of_truck": "AAA",
	           	"truck_capacity": 10,
				"num_of_truck": 1
	      	},
	      	{
	           "type_of_truck": "BBB",
	           	"truck_capacity": 5,
				"num_of_truck": 1
	      	}

      	],
    "has_return": "true",
    "priority_capacity": "true",
    "time_windows": "true"
}

"""

class Truck_capacity_API(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Headers'] = 'Authorization'
        self.response.headers['Access-Control-Allow-Headers'] = 'Cache-Control'
        self.response.headers['Access-Control-Allow-Credentials'] = 'true'
        self.response.headers['Content-Type'] = 'application/json;charset=utf-8'

        email = self.request.get('userId')
        api_key = self.request.get('keyId')

        # Error list for invalid postal codes
        errors = []

        api_user = "false"
        auth_user = UserAccount.check_API_auth(email, api_key)

        # Sorting postal code sequence code
        postal_sequence_list = []
        postal_sequence_current = []

        # Error Message
        error_valid_msg_truck = "Add more truck! <br />The minimum balance number for delivery truck "
        error_capacity_msg_truck = " - exceeding capacity"
        error_capacity_num_truck = "Maximum 15 Trucks only"
        error_capacity_cargo_unit = "Please check the input cargo unit - Location Details"

        maximum_truck = 15

        if auth_user == None:
            errors.extend(['Incorrect email or API Key'])

        if auth_user == True:
            api_user = "true"

        # Checking for Credit Access
        credits_account = UserAccount.check_credit_usage(email)

        if credits_account == None:
            errors.extend(['Error in Credits Access'])

        response = {}

        request_str = self.request.body
        logging.info(request_str)

        if len(errors) == 0:

            try:
                data = json.loads(request_str)
            except:
                errors.extend(['Error in JSON'])

        if len(errors) == 0:

            starting_postal, error = checkInRequest('starting_postal', data)
            errors.extend(error)

            order_details, error = checkInRequest('order_details', data)
            errors.extend(error)

            truck_details, error = checkInRequest('truck_details', data)
            errors.extend(error)

            # trigger value
            has_return, error = checkInRequest('has_return', data)
            errors.extend(error)

            # Time windows
            time_windows, error = checkInRequest('time_windows', data)
            errors.extend(error)

            priority_capacity, error = checkInRequest('priority_capacity', data)
            errors.extend(error)

            # Grp truck details
            # Type of Truck
            truck_capacity_grp = []
            company_sequence = []

            for truck_detail in truck_details:
                # extract the truck
                type_of_truck = truck_detail["type_of_truck"]
                truck_capacity = truck_detail["truck_capacity"]
                num_of_truck = truck_detail["num_of_truck"]

                truck_capacity_grp.append([str(type_of_truck), int(truck_capacity), int(num_of_truck)])

            # count the capacity
            limit_sum = 0

            # count num of truck
            truck_sum = 0

            for num_truck in range(0, len(truck_capacity_grp)):
                current_num = truck_capacity_grp[num_truck]
                capacity_limit = current_num[1]
                num_truck = current_num[2]

                limit_sum += capacity_limit
                truck_sum += num_truck

            # Show error if reach maximum truck allowed
            if truck_sum > maximum_truck:
                logging.info('Warning! ' + error_capacity_num_truck)
                errors.extend(['Warning! ' + error_capacity_num_truck])

            # Counter checking of Postal Code
            num_post_code = 0

            for index in range(0, len(order_details)):

                """ ['760450', 'Order02', '2'] """

                num_post_code += 1
                postal_pair = order_details[index]

                if time_windows == "true":

                    # Show error if one column only
                    if len(postal_pair) == 1:
                        logging.info(postal_pair)
                        errors.extend([error_capacity_cargo_unit])
                        break

                    # Show error if the two column
                    if len(postal_pair) == 2:
                        logging.info(postal_pair)
                        errors.extend([error_capacity_cargo_unit])
                        break

                    # extract each column of Delivery Location Details
                    postal_code = str(postal_pair[0])
                    order_id = str(postal_pair[1])
                    track_capacity = postal_pair[2]
                    tw_from = str(postal_pair[3])
                    tw_to = str(postal_pair[4])

                    # Check if the postal code is 5 digit only
                    if len(str(postal_code)) == 5:
                        # add "0" in the index of Postal Code
                        postal_code = "0" + postal_code

                    # Any Postal Code below 4 will throw error
                    if len(str(postal_code)) < 4:
                        errors.extend(["  Please Check ", postal_code, ", it should 6 digits <br />"])

                    # Check if the 3rd column is integer or number
                    cargo_unit = RepresentsInt(track_capacity)

                    if not cargo_unit:
                        errors.extend([postal_code + ' Error in track_capacity'])
                        break

                    # Check if postal code is a valid value i.e. Contains only five or six digits
                    if not str.isdigit(postal_code) or len(str(postal_code)) != 6:
                        logging.info('Warning! Postal Code error')
                        errors.extend(['Please check ' + postal_code + ' is not valid it should be 6 digit'])

                    # Check the limit capacity of the truck
                    if int(track_capacity) > int(limit_sum):
                        logging.info('Warning! ' + postal_code + error_capacity_msg_truck)
                        errors.extend(['Warning! ' + postal_code + error_capacity_msg_truck])

                        break

                    # Checking TW Format
                    tw_format = is_time_format(tw_from)

                    if not tw_format:
                        # send error if invalid
                        errors.extend([tw_from, ' - ', tw_to, ' - invalid Time Windows format <br />'])
                        break

                    # convert time only, add zero for those have 1 decimal
                    new_tw_from = datetime.strptime(tw_from, '%H:%M:%S').time()

                    postal_sequence_current.append(str(postal_code))
                    postal_sequence_list.append([postal_code, str(order_id), int(track_capacity), str(new_tw_from), str(tw_to)])

                else:
                    # Show error if one column only
                    if len(postal_pair) == 1:
                        logging.info(postal_pair)
                        errors.extend([error_capacity_cargo_unit])
                        break

                    # Show error if the two column
                    if len(postal_pair) == 2:
                        logging.info(postal_pair)
                        errors.extend([error_capacity_cargo_unit])
                        break

                    # extract each column of Delivery Location Details
                    postal_code = str(postal_pair[0])
                    order_id = str(postal_pair[1])
                    track_capacity = postal_pair[2]
                    # temp_id = postal_pair[3]

                    # Check if the postal code is 5 digit only
                    if len(str(postal_code)) == 5:
                        # add "0" in the index of Postal Code
                        postal_code = "0" + postal_code

                    # Check if the 3rd column is integer or number
                    cargo_unit = RepresentsInt(track_capacity)

                    if not cargo_unit:
                        errors.extend([postal_code + ' Error in track_capacity'])
                        break

                    # Check if postal code is a valid value i.e. Contains only five or six digits
                    if not str.isdigit(postal_code) or len(str(postal_code)) != 6:

                        logging.info('Warning! Postal Code error')
                        errors.extend(['Please check '+postal_code+ ' is not valid it should be 6 digit'])

                    # Check the limit capacity of the truck
                    if int(track_capacity) > int(limit_sum):
                        logging.info('Warning! ' + postal_code + error_capacity_msg_truck)
                        errors.extend(['Warning! '+postal_code + error_capacity_msg_truck])

                        break

                    postal_sequence_current.append(str(postal_code))
                    postal_sequence_list.append([str(postal_code), str(order_id), int(track_capacity)])

                # - - - - - - HQ Starting point Lat Long - - - - - #

            # For Non Multi Truck
            options_truck = "false"
            priority_capacity_comp = "false"
            sort_company = "false"
            vehicle_quantity = 0

            # Empty array
            result_route_value = []
            tw_result_route_value = []

            # variables for Time windows:
            tw_postal_list = []
            tw_latlng_array = 0

            if len(errors) == 0:

                result_list_data = sorting.sort_by_postals_chunck(
                    int(starting_postal),
                    postal_sequence_list,
                    int(vehicle_quantity),
                    email, has_return,
                    priority_capacity,
                    priority_capacity_comp,
                    api_user, sort_company, truck_capacity_grp, options_truck, time_windows, company_sequence)

                # Extracting the data from result_list_data dictionary:
                # Lat & long of Starting postal code
                origin_destination = result_list_data['origin_destination']["starting_latlong"]

                # Sorted postal code
                propose_result = result_list_data['propose_result_list']["propose_result"]
                current_result = result_list_data['propose_result_list']["current_result"]

                # Proposed Routes with sequence orders
                vehicle_postal_list_new_seq = result_list_data['postal_sequence_orders']["vehicle_postal_list_new_seq"]

                # Result data for Time Windows
                tw_proposed_seq = result_list_data['postal_tw_result']["tw_proposed_list"]

                # Group Details for Truck capacity
                grp_truck = result_list_data['truck_capacity_result']["grp_truck"]
                vehicle_quantity = result_list_data['truck_capacity_result']["vehicle_quantity"]

                # process the data:
                # Vehicle Result base of the priority:
                result_num_truck = len(propose_result)

                # Show error if the Number of truck is not enough
                if int(len(propose_result)) > int(truck_sum):
                    errors.extend([error_valid_msg_truck + " is " + str(result_num_truck)])

                # Converting HQ to lat & long value
                current_distance = sorting_prep.result_distance_latlng(current_result, origin_destination, num_post_code)
                proposed_distance = sorting_prep.result_distance_latlng(propose_result, origin_destination, num_post_code)

                if time_windows == "true":

                    for truck_count in tw_proposed_seq:
                        tw_postal_list_inner = []

                        for tw_orders in truck_count:
                            tw_postal_list_inner.append(tw_orders[0])
                        tw_postal_list.append(tw_postal_list_inner)

                    # Get the distance
                    tw_propose_route_value = sorting_prep.result_distance_latlng(tw_postal_list, origin_destination, num_post_code)

                    # Converting the total percentage saving of distance
                    difference_total = proposed_distance - tw_propose_route_value
                    tw_percentage_savings = (difference_total / proposed_distance) * 100

                    # round off the number
                    proposed_distance = round(proposed_distance, 2)
                    current_distance = round(current_distance, 2)
                    tw_percentage_savings = round(tw_percentage_savings, 2)

                    tw_result_route_savings_dic = {
                        "propose_value": proposed_distance,
                        "proposed_value_with_time_windows": tw_propose_route_value,
                        "percentage_savings": tw_percentage_savings,
                    }
                    # Total_summary_saving
                    tw_result_route_value.append(tw_result_route_savings_dic)

                    # GeoCode Map for TW
                    tw_latlng_array = map_visible(tw_postal_list)

                # GeoCode Map
                latlng_array = map_visible(propose_result)

                # Converting the total percentage saving of distance
                difference_total = current_distance - proposed_distance
                percentage_savings = (difference_total / current_distance) * 100

                # round off the number
                proposed_distance = round(proposed_distance, 2)
                current_distance = round(current_distance, 2)
                percentage_savings = round(percentage_savings, 2)

                result_route_savings_dic = {
                    "current_value": current_distance,
                    "proposed_value": proposed_distance,
                    "percentage_savings": percentage_savings,
                }

                # Total_summary_saving
                result_route_value.append(result_route_savings_dic)

                if len(errors) == 0:

                    # Converting JSON
                    response['status'] = 'ok'
                    response['data_result'] = [{
                        "required_fields": {

                            "starting_postal": starting_postal,
                            "has_return": has_return,
                            "priority_capacity": priority_capacity,

                            "vehicle_details": {
                                "grp_truck": grp_truck,
                                "vehicle_quantity": vehicle_quantity
                            },

                        },
                        "order_details_results": {

                            "postal_sequence_results": {
                                "propose_result": vehicle_postal_list_new_seq,
                                "propose_routes_total_summary_savings": result_route_value,
                                "propose_routes_postal_latlng": latlng_array
                            }
                        },
                        "time_windows_results": {
                                "time_windows_data": {
                                    "time_windows_proposed_seq": tw_proposed_seq,
                                    "time_windows_latlng_postal_code": tw_latlng_array,
                                    "time_windows_propose_route_value": tw_result_route_value,
                                },
                        }
                    }]

            else:
                errors.extend(['Error in Process'])

        if len(errors) > 0:
            response['status'] = 'error'
            response['errors'] = errors

        logging.info(response)
        self.response.out.write(json.dumps(response, indent=3))

"""
{
    "starting_postal": "461051",
    "order_details": [
                      ["469001", "Order01"],
                      ["760450", "Order02"],
                      ["596937", "Order03"],
                      ["596740", "Order04"],
                      ["098585", "Order05"],
                      ["109680", "Order06"],
                      ["560405", "Order07"],
                      ["278986", "Order08"],
                      ["431011", "Order09"],
                      ["460102", "Order10"]

                    ],
    "number_of_vehicle" : 1,
    "has_return": "true",
    "options_truck": "true"
}

# for Time Windows:
{
    "starting_postal": "461051",
    "order_details": [
                        ["369974", "Order01", "09:00:00", "12:00:00"],
                        ["760450", "Order02", "07:00:00", "8:00:00"],
                        ["596937", "Order03", "13:00:00", "14:00:00"],
                        ["596740", "Order04", "10:00:00", "11:00:00"],
                        ["560405", "Order05", "09:30:00", "10:20:00"],
                        ["543262", "Order06", "15:00:00", "18:00:00"],
                        ["520156", "Order07", "14:00:00", "17:00:00"],
                        ["469001", "Order08", "09:00:00", "12:00:00"],
                        ["760450", "Order09", "11:00:00", "11:30:00"],
                        ["596937", "Order10", "13:00:00", "15:00:00"],
                        ["596740", "Order11", "16:00:00", "17:00:00"],
                        ["098585", "Order12", "13:00:00", "15:00:00"],
                        ["109680", "Order13", "16:00:00", "17:00:00"],
                        ["189637", "Order14", "15:00:00", "18:00:00"]

                    ],
    "number_of_vehicle" : 1,
    "has_return": "true",
    "options_truck": "true",
    "time_windows": "true"
}

"""

class Multi_truck_API(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Headers'] = 'Authorization'
        self.response.headers['Access-Control-Allow-Headers'] = 'Cache-Control'
        self.response.headers['Access-Control-Allow-Credentials'] = 'true'
        self.response.headers['Content-Type'] = 'application/json;charset=utf-8'

        # api_key = self.request.authorization

        email = self.request.get('userId')
        api_key = self.request.get('keyId')

        # Error list for invalid postal codes
        errors = []

        api_user = "false"
        auth_user = UserAccount.check_API_auth(email, api_key)

        if auth_user == None:
            errors.extend(['Incorrect email or API Key'])

        if auth_user == True:
            api_user = "true"

        # Checking for Credit Access
        credits_account = UserAccount.check_credit_usage(email)

        if credits_account == None:
            errors.extend(['Error in Credits Access <br />'])

        response = {}
        request_str = self.request.body
        logging.info(request_str)

        if len(errors) == 0:

            try:
                data = json.loads(request_str)

            except:

                errors.extend(['Error in JSON'])

        if len(errors) == 0:

            starting_postal, error = checkInRequest('starting_postal', data)
            errors.extend(error)

            order_details, error = checkInRequest('order_details', data)
            errors.extend(error)

            vehicle_quantity, error = checkInRequest('number_of_vehicle', data)
            errors.extend(error)

            has_return, error = checkInRequest('has_return', data)
            errors.extend(error)

            # Time windows
            time_windows, error = checkInRequest('time_windows', data)
            errors.extend(error)

            options_truck, error = checkInRequest('options_truck', data)
            errors.extend(error)

            # Sorting postal code sequence code
            postal_sequence_list = []
            postal_sequence_current = []

            # For empty order
            temp_order_id = ['0']
            # forEmp_Capt = ['0', '0']

            # Validation for Vehicle
            if not vehicle_quantity:
                errors.extend(["number_of_vehicle" + " is empty"])

            # starting point 5 digit
            if len(str(starting_postal)) == 5:
                    starting_postal = "0" + starting_postal

            # if below 5 digit
            if len(str(starting_postal)) != 6:
                logging.info('Warning! error')
                errors.extend(['Starting Postal code is not valid, it should be 6 digit'])

            # Counter checking of Postal Code
            num_post_code = 0

            for index in range(0, len(order_details)):

                """ [u'760450', u'Order02'] """

                num_post_code += 1
                postal_pair = order_details[index]

                if time_windows == "true":

                    # Show error if one column only
                    if len(postal_pair) == 1:
                        logging.info(postal_pair)
                        errors.extend([error_capacity_cargo_unit])
                        break

                    # Show error if the two column
                    if len(postal_pair) == 2:
                        logging.info(postal_pair)
                        errors.extend([error_capacity_cargo_unit])
                        break

                    # extract each column of Delivery Location Details
                    postal_code = str(postal_pair[0])
                    order_id = str(postal_pair[1])
                    tw_from = str(postal_pair[2])
                    tw_to = str(postal_pair[3])

                    # Check if the postal code is 5 digit only
                    if len(str(postal_code)) == 5:
                        # add "0" in the index of Postal Code
                        postal_code = "0" + postal_code

                    # Any Postal Code below 4 will throw error
                    if len(str(postal_code)) < 4:
                        errors.extend(["  Please Check ", postal_code, ", it should 6 digits <br />"])

                    # Check if postal code is a valid value i.e. Contains only five or six digits
                    if not str.isdigit(postal_code) or len(str(postal_code)) != 6:
                        logging.info('Warning! Postal Code error')
                        errors.extend(['Please check ' + postal_code + ' is not valid it should be 6 digit'])

                    # Checking TW Format
                    tw_format = is_time_format(tw_from)

                    if not tw_format:
                        # send error if invalid
                        errors.extend([tw_from, ' - ', tw_to, ' - invalid Time Windows format <br />'])
                        break

                    # convert time only, add zero for those have 1 decimal
                    new_tw_from = datetime.strptime(tw_from, '%H:%M:%S').time()

                    postal_sequence_current.append(str(postal_code))
                    postal_sequence_list.append([postal_code, str(order_id), str(new_tw_from), str(tw_to)])

                else:

                    if len(postal_pair) == 1:
                        logging.info(postal_pair)
                        postal_pair.extend(temp_order_id)

                    postal_code = str(postal_pair[0])
                    order_id = str(postal_pair[1])

                    # track_capacity = int(postal_pair[2])
                    # temp_id = postal_pair[3]

                    if len(str(postal_code)) == 5:
                        postal_code = "0" + postal_code

                    # Check if postal code is a valid value i.e. Contains only five or six digits
                    if not str.isdigit(postal_code) or len(str(postal_code)) != 6:
                        logging.info('Warning! Postal Code error')
                        errors.extend(['Please check '+postal_code+ ' is not valid it should be 6 digit'])

                    postal_sequence_current.append(str(postal_code))
                    postal_sequence_list.append([str(postal_code), str(order_id)])

            # - - - - - - HQ Starting point Lat Long - - - - - #

            # For Non Multi Truck
            priority_capacity = "false"
            sort_company = "false"
            priority_capacity_comp = "false"
            company_sequence = []
            result_route_value = []
            truck_capacity_grp = []

            # variables for Time windows:
            tw_result_route_value = []
            tw_postal_list = []
            tw_latlng_array = 0

            if len(errors) == 0:

                result_list_data = sorting.sort_by_postals_chunck(
                    int(starting_postal),
                    postal_sequence_list,
                    int(vehicle_quantity),
                    email, has_return,
                    priority_capacity,
                    priority_capacity_comp,
                    api_user, sort_company, truck_capacity_grp, options_truck, time_windows, company_sequence)

                '''['postal_result', 'order_id']'''

                # Extracting dictionary
                # Lat & long of Starting postal code
                origin_destination = result_list_data['origin_destination']["starting_latlong"]

                # Sorted postal code
                propose_result = result_list_data['propose_result_list']["propose_result"]
                current_result = result_list_data['propose_result_list']["current_result"]

                # Proposed Routes with sequence orders
                vehicle_postal_list_new_seq = result_list_data['postal_sequence_orders']["vehicle_postal_list_new_seq"]
                # current_postal_list_seq = result_list_data['postal_sequence_orders']["current_postal_list_seq"]

                # Result data for Time Windows
                tw_proposed_seq = result_list_data['postal_tw_result']["tw_proposed_list"]

                # Converting HQ to lat & long value
                # origin_destination = self.convert_hq(str(starting_postal))
                current_distance = sorting_prep.result_distance_latlng(current_result, origin_destination, num_post_code)
                proposed_distance = sorting_prep.result_distance_latlng(propose_result, origin_destination, num_post_code)

                if time_windows == "true":

                    for truck_count in tw_proposed_seq:
                        tw_postal_list_inner = []

                        for tw_orders in truck_count:
                            tw_postal_list_inner.append(tw_orders[0])
                        tw_postal_list.append(tw_postal_list_inner)

                    # Get the distance
                    tw_propose_route_value = sorting_prep.result_distance_latlng(tw_postal_list, origin_destination, num_post_code)

                    # Converting the total percentage saving of distance
                    difference_total = proposed_distance - tw_propose_route_value
                    tw_percentage_savings = (difference_total / proposed_distance) * 100

                    # round off the number
                    proposed_distance = round(proposed_distance, 2)
                    current_distance = round(current_distance, 2)
                    tw_percentage_savings = round(tw_percentage_savings, 2)

                    tw_result_route_savings_dic = {
                        "propose_value": proposed_distance,
                        "proposed_value_with_time_windows": tw_propose_route_value,
                        "percentage_savings": tw_percentage_savings,
                    }
                    # Total_summary_saving
                    tw_result_route_value.append(tw_result_route_savings_dic)

                    # GeoCode Map for TW
                    tw_latlng_array = map_visible(tw_postal_list)

                # GeoCode Map
                latlng_array = map_visible(propose_result)

                # Converting the total percentage saving of distance
                difference_total = current_distance - proposed_distance
                percentage_savings = (difference_total / current_distance) * 100

                # round off the number
                proposed_distance = round(proposed_distance, 2)
                current_distance = round(current_distance, 2)
                percentage_savings = round(percentage_savings, 2)

                result_route_savings_dic = {
                    "current_value": current_distance,
                    "proposed_value": proposed_distance,
                    "percentage_savings": percentage_savings,
                }

                # Total_summary_saving
                result_route_value.append(result_route_savings_dic)

                # Send JSON Response
                response['status'] = 'ok'
                response['data_result'] = [{

                            "required_fields": {
                                "starting_postal": starting_postal,
                                "has_return": has_return,
                                "vehicle_details": {
                                    "vehicle_quantity": vehicle_quantity
                                },
                            },
                            "order_details_results": {
                                "postal_sequence_results": {
                                    "propose_result": vehicle_postal_list_new_seq,
                                    "propose_routes_total_summary_savings": result_route_value,
                                    "propose_routes_postal_latlng": latlng_array
                                },

                            },
                            "time_windows_results": {
                                "time_windows_data": {
                                    "time_windows_proposed_seq": tw_proposed_seq,
                                    "time_windows_latlng_postal_code": tw_latlng_array,
                                    "time_windows_propose_route_value": tw_result_route_value,
                                },
                            }
                        }]
            else:
                errors.extend(['Error in Process'])

        else:
            errors.extend(['Error in JSON-Data'])

        if len(errors) > 0:
            response['status'] = 'error'
            response['errors'] = errors

        logging.info(response)
        self.response.out.write(json.dumps(response, indent=3))

"""
# for companies
{
     "companies_hq": [
     	{
          "starting_postal": "469001"
     	},
     	{
          "starting_postal": "389458"
     	}
     ],
     "order_details": [
            ["369974", "Order01", 1, "Company_A"],
            ["760450", "Order02", 1, "Company_A"],
            ["596937", "Order03", 1, "Company_A"],
            ["596740", "Order04", 1, "Company_A"],
            ["560405", "Order05", 1, "Company_A"],
            ["543262", "Order06", 1, "Company_A"],
            ["520156", "Order07", 1, "Company_A"],
            ["469001", "Order08", 1, "Company_B"],
            ["760450", "Order09", 1, "Company_B"],
            ["596937", "Order10", 1, "Company_B"],
            ["596740", "Order11", 1, "Company_B"],
            ["098585", "Order12", 1, "Company_B"],
            ["109680", "Order13", 1, "Company_B"],
            ["189637", "Order14", 1, "Company_B"]
     ],

     "multi_truck_details": [
     	{
          "number_of_vehicle": 1
     	},
     	{
          "number_of_vehicle": 1
        }],
     "num_comp_val" : 2,
     "has_return": "true",
     "priority_capacity_comp": "false",
     "sort_company": "true",
     "time_windows": "false"
}

# for companies without time windows

{
     "companies_hq": [
     	{
          "starting_postal": "469001"
     	},
     	{
          "starting_postal": "389458"
     	}
     ],
     "order_details": [
                ["369974", "Order01", 1, "Company_A", "09:00:00", "12:00:00"],
                ["760450", "Order02", 1, "Company_A", "07:00:00", "8:00:00"],
                ["596937", "Order03", 1, "Company_A", "13:00:00", "14:00:00"],
                ["596740", "Order04", 1, "Company_A", "10:00:00", "11:00:00"],
                ["560405", "Order05", 1, "Company_A", "09:30:00", "10:20:00"],
                ["543262", "Order06", 1, "Company_A", "15:00:00", "18:00:00"],
                ["520156", "Order07", 1, "Company_A", "14:00:00", "17:00:00"],
                ["469001", "Order08", 1, "Company_B", "09:00:00", "12:00:00"],
                ["760450", "Order09", 1, "Company_B", "11:00:00", "11:30:00"],
                ["596937", "Order10", 1, "Company_B", "13:00:00", "15:00:00"],
                ["596740", "Order11", 1, "Company_B", "16:00:00", "17:00:00"],
                ["098585", "Order12", 1, "Company_B", "13:00:00", "15:00:00"],
                ["109680", "Order13", 1, "Company_B", "16:00:00", "17:00:00"],
                ["189637", "Order14", 1, "Company_B", "15:00:00", "18:00:00"]
     ],
     "multi_truck_details": [
     	{
          "number_of_vehicle": 1
     	},
     	{
          "number_of_vehicle": 1
        }],
     "num_comp_val" : 2,
     "has_return": "true",
     "priority_capacity_comp": "false",
     "sort_company": "true",
     "time_windows": "false"
}

///

{
     "companies_hq": [
     	{
          "starting_postal": "469001"
     	},
     	{
          "starting_postal": "389458"
     	}
     ],
     "order_details": [
             ["369974", "Order01", 1, "Company_A"],
            ["760450", "Order02", 1, "Company_A"],
            ["596937", "Order03", 1, "Company_A"],
            ["596740", "Order04", 1, "Company_A"],
            ["560405", "Order05", 1, "Company_A"],
            ["543262", "Order06", 1, "Company_A"],
            ["520156", "Order07", 1, "Company_A"],
            ["469001", "Order08", 1, "Company_B"],
            ["760450", "Order09", 1, "Company_B"],
            ["596937", "Order10", 1, "Company_B"],
            ["596740", "Order11", 1, "Company_B"],
            ["098585", "Order12", 1, "Company_B"],
            ["109680", "Order13", 1, "Company_B"],
            ["189637", "Order14", 1, "Company_B"]
     ],

     "multi_truck_details": [
	    	{
	      		"type_of_truck": "AAA",
	      		"truck_capacity": 3,
	      		"num_of_truck": 1
	    	},
	    	{
	      		"type_of_truck": "BBB",
	      		"truck_capacity": 3,
	      		"num_of_truck": 1
	    	}],
  "num_comp_val" : 2,
     "has_return": "true",
     "priority_capacity_comp": "true",
     "sort_company": "true",
     "time_windows": "false"
}
"""

class Multi_companies_API(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Headers'] = 'Authorization'
        self.response.headers['Access-Control-Allow-Headers'] = 'Cache-Control'
        self.response.headers['Access-Control-Allow-Credentials'] = 'true'
        self.response.headers['Content-Type'] = 'application/json;charset=utf-8'

        # api_key = self.request.authorization

        email = self.request.get('userId')
        api_key = self.request.get('keyId')

        # Error list for invalid postal codes
        errors = []

        api_user = "false"
        auth_user = UserAccount.check_API_auth(email, api_key)

        if auth_user == None:
            errors.extend(['Incorrect email or API Key'])

        if auth_user == True:
            api_user = "true"

        # Checking for Credit Access
        credits_account = UserAccount.check_credit_usage(email)

        if credits_account == None:
            errors.extend(['Error in Credits Access <br />'])

        response = {}
        request_str = self.request.body
        logging.info(request_str)

        if len(errors) == 0:
            try:
                data = json.loads(request_str)

            except:
                errors.extend(['Error in JSON'])

        if len(errors) == 0:

            companies_hq, error = checkInRequest('companies_hq', data)
            errors.extend(error)

            order_details, error = checkInRequest('order_details', data)
            errors.extend(error)

            multi_truck_details, error = checkInRequest('multi_truck_details', data)
            errors.extend(error)

            has_return, error = checkInRequest('has_return', data)
            errors.extend(error)

            sort_company, error = checkInRequest('sort_company', data)
            errors.extend(error)

            priority_capacity_comp, error = checkInRequest('priority_capacity_comp', data)
            errors.extend(error)

            num_comp_val, error = checkInRequest('num_comp_val', data)
            errors.extend(error)

            time_windows, error = checkInRequest('time_windows', data)
            errors.extend(error)

            # extracting data section
            starting_postal_list = []
            truck_sequence_list = []
            truck_capacity_grp = []
            postal_sequence_current = []
            postal_sequence_company = []
            company_list_grp = []
            company_sequence = []

            # Truck capacity Groupings
            truck_capacity_list_c1 = []
            truck_capacity_grp_comp1 = []

            # extract starting points:
            for starting_point in companies_hq:
                starting = starting_point["starting_postal"]

                # add zero in front if 5 digit only
                if len(str(starting)) == 5:
                    starting = "0" + starting

                # if below 5 digit
                if len(str(starting)) != 6:
                    logging.info('Warning! error')
                    errors.extend(['Starting Postal code is not valid, it should be 6 digit'])

                starting_postal_list.append(starting)

            if priority_capacity_comp == "true":

                # extract truck details list:
                for num_truck in multi_truck_details:

                    type_of_truck = num_truck["type_of_truck"]
                    truck_capacity = num_truck["truck_capacity"]
                    num_of_truck = num_truck["num_of_truck"]

                    truck_capacity_list_c1.append([[str(type_of_truck), int(truck_capacity), int(num_of_truck)]])

                truck_capacity_grp_comp1.extend(truck_capacity_list_c1)

            else:

                # extract vehicle list:
                for num_truck in multi_truck_details:
                    vehicle_truck = num_truck["number_of_vehicle"]
                    truck_sequence_list.append(vehicle_truck)

            # Counter checking of Postal Code
            num_post_code = 0

            # extract order details:
            for index in range(0, len(order_details)):

                if time_windows == "true":
                    # Counter checking of Postal Code
                    num_post_code += 1

                    postal_pair = order_details[index]

                    if len(postal_pair) == 1:
                        logging.info(postal_pair)
                        errors.extend(['Please check the postal sequence input'])
                        break

                    postal_code = str(postal_pair[0])
                    order_id = str(postal_pair[1])
                    truck_capacity = postal_pair[2]
                    company = postal_pair[3]
                    tw_from = str(postal_pair[4])
                    tw_to = str(postal_pair[5])

                    # Checking postal code
                    if len(str(postal_code)) == 5:
                        postal_code = "0" + postal_code

                    # Check if postal code is a valid value i.e. Contains only five or six digits
                    if not str.isdigit(postal_code) or len(str(postal_code)) != 6:
                        logging.info('Warning! Postal Code error')
                        errors.extend(['Please check ' + postal_code + ' is not valid, it should be 6 digit'])

                    # Checking TW Format
                    tw_format = is_time_format(tw_from)

                    if not tw_format:
                        # send error if invalid
                        errors.extend([tw_from, ' - ', tw_to, ' - invalid Time Windows format'])
                        break

                    # convert time only, add zero for those have 1 decimal
                    new_tw_from = datetime.strptime(tw_from, '%H:%M:%S').time()

                    postal_sequence_current.append([str(postal_code), str(order_id), int(truck_capacity), str(company), str(new_tw_from), str(tw_to)])

                else:

                    # Counter checking of Postal Code
                    num_post_code += 1

                    postal_pair = order_details[index]

                    if len(postal_pair) == 1:
                        logging.info(postal_pair)
                        errors.extend(['Please check the postal sequence input'])
                        break

                    postal_code = str(postal_pair[0])
                    order_id = str(postal_pair[1])
                    truck_capacity = postal_pair[2]
                    company = postal_pair[3]

                    if len(str(postal_code)) == 5:
                        postal_code = "0" + postal_code

                    # Check if postal code is a valid value i.e. Contains only five or six digits
                    if not str.isdigit(postal_code) or len(str(postal_code)) != 6:
                        logging.info('Warning! Postal Code error')
                        errors.extend(['Please check ' + postal_code + ' is not valid, it should be 6 digit'])

                    postal_sequence_current.append([str(postal_code), str(order_id), int(truck_capacity), str(company)])

            # extract company groupings:
            for company in range(len(postal_sequence_current)):
                companyList = postal_sequence_current[company]
                company_list_grp.append(companyList)

            for key, group in itertools.groupby(company_list_grp, operator.itemgetter(3)):

                # group as per company
                postal_sequence_company.append(list(group))

            # validation for company
            if int(len(postal_sequence_company)) != num_comp_val:
                errors.extend(['Please Check the number of company inputs'])

            # print len(item_dict['result'][0]['run'])

            # For Non Multi Truck
            options_truck = "false"
            priority_capacity = "false"
            vehicle_quantity = 0
            num_user_load = "true"

            if len(errors) == 0:

                propose_result_company = []
                current_result_company = []

                origin_result_company = []

                propose_result_sequence = []
                current_result_sequence = []

                latlng_array_list = []
                result_route_value = []

                # Truck capacity
                vehicle_list_grp = []
                grp_truck_name_seq = []

                # Variables for Time windows:
                propose_result_sequence_tw = []
                propose_result_postal_tw = []
                propose_result_cons_tw = []
                total_savings_tw_cons = []
                total_savings_tw = []
                latlng_array_list_tw = []

                # Consolidated Routes Empty Array
                postal_sequence_list_cons = []
                current_sequence_list_cons = []
                result_route_value_cons = []

                if priority_capacity_comp == "true":

                    # Calling function for sorting and chunking
                    for starting_post, company_sequence, truck_capacity_grp in itertools.izip(starting_postal_list, postal_sequence_company, truck_capacity_grp_comp1):

                        result_list_data = sorting.sort_by_postals_chunck(
                            starting_post, company_sequence,
                            vehicle_quantity, email, has_return,
                            priority_capacity,
                            priority_capacity_comp,
                            api_user, sort_company, truck_capacity_grp, options_truck, time_windows, postal_sequence_current)

                        # Extracting "result_list_data" dictionary
                        # Lat & long of Starting postal code
                        origin_destinations = result_list_data['origin_destination']["starting_latlong"]

                        # Sorted postal code
                        propose_result = result_list_data['propose_result_list']["propose_result"]
                        current_result = result_list_data['propose_result_list']["current_result"]

                        # Sorted postal code
                        vehicle_postal_list_new_seq = result_list_data['postal_sequence_orders']["vehicle_postal_list_new_seq"]

                        # Truck Capacity
                        truck_name = result_list_data['truck_capacity_result']["grp_truck"]
                        truck_sequence_list = result_list_data['truck_capacity_result']["vehicle_quantity"]

                        # Consolidation Sequence
                        vehicle_postal_route_cons = result_list_data['consolidation_result']["proposed_postal_route_cons"]
                        current_postal_route_cons = result_list_data['consolidation_result'][ "current_postal_route_cons"]

                        # response dictionary for TW
                        tw_proposed_seq = result_list_data['postal_tw_result']["tw_proposed_list"]
                        tw_proposed_postal = result_list_data['postal_tw_result']["tw_proposed_postal"]
                        tw_proposed_postal_cons = result_list_data['postal_tw_result']["tw_proposed_postal_cons"]

                        origin_result_company.append(origin_destinations)
                        propose_result_company.append(propose_result)
                        current_result_company.append(current_result)
                        propose_result_sequence.append(vehicle_postal_list_new_seq)

                        # Truck Capacity
                        vehicle_list_grp.append(truck_name)

                        # Consolidation
                        postal_sequence_list_cons.append(vehicle_postal_route_cons)
                        current_sequence_list_cons.append(current_postal_route_cons)

                        # Time Windows
                        propose_result_sequence_tw.append(tw_proposed_seq)
                        propose_result_postal_tw.append(tw_proposed_postal)

                        propose_result_cons_tw.append(tw_proposed_postal_cons)

                        # GeoCode Map
                        latlng_array = map_visible(propose_result)
                        latlng_array_list.append(latlng_array)

                        # GeoCode Map TW
                        latlng_array_tw = map_visible(tw_proposed_postal)
                        latlng_array_list_tw.append(latlng_array_tw)

                else:

                    for starting_post, company_sequence, vehicle_quantity in itertools.izip(starting_postal_list, postal_sequence_company, truck_sequence_list):
                        result_list_data = sorting.sort_by_postals_chunck(
                            starting_post,
                            company_sequence,
                            vehicle_quantity,
                            email, has_return,
                            priority_capacity,
                            priority_capacity_comp,
                            api_user, sort_company, truck_capacity_grp, options_truck, time_windows, postal_sequence_current)

                        # Extracting "result_list_data" dictionary
                        # Lat & long of Starting postal code
                        origin_destinations = result_list_data['origin_destination']["starting_latlong"]

                        # Sorted postal code
                        propose_result = result_list_data['propose_result_list']["propose_result"]
                        current_result = result_list_data['propose_result_list']["current_result"]

                        # Result Sorted postal with orders
                        vehicle_postal_list_new_seq = result_list_data['postal_sequence_orders']["vehicle_postal_list_new_seq"]
                        current_postal_list_seq = result_list_data['postal_sequence_orders']["current_postal_list_new_seq"]

                        # Group Truck
                        grp_truck = result_list_data['truck_capacity_result']["grp_truck"]

                        # Consolidated Sequence
                        vehicle_postal_route_cons = result_list_data['consolidation_result']["proposed_postal_route_cons"]
                        current_postal_route_cons = result_list_data['consolidation_result']["current_postal_route_cons"]

                        # Response dictionary for TW
                        tw_proposed_seq = result_list_data['postal_tw_result']["tw_proposed_list"]
                        tw_proposed_postal = result_list_data['postal_tw_result']["tw_proposed_postal"]
                        tw_proposed_postal_cons = result_list_data['postal_tw_result']["tw_proposed_postal_cons"]

                        propose_result_company.append(propose_result)
                        current_result_company.append(current_result)

                        origin_result_company.append(origin_destinations)

                        propose_result_sequence.append(vehicle_postal_list_new_seq)
                        current_result_sequence.append(current_postal_list_seq)

                        grp_truck_name_seq.append(grp_truck)

                        # Consolidated Routes List
                        postal_sequence_list_cons.append(vehicle_postal_route_cons)
                        current_sequence_list_cons.append(current_postal_route_cons)

                        # Time Windows append
                        propose_result_sequence_tw.append(tw_proposed_seq)
                        propose_result_postal_tw.append(tw_proposed_postal)
                        propose_result_cons_tw.append(tw_proposed_postal_cons)

                        # GeoCode Map
                        latlng_array = map_visible(propose_result)
                        latlng_array_list.append(latlng_array)

                # Computing the total summary saving
                for origin_destination, current_result_comp, propose_result_comp in itertools.izip(origin_result_company, current_result_company, propose_result_company):

                    current_route_value = sorting_prep.result_distance_latlng(current_result_comp, origin_destination, num_post_code)
                    propose_route_value = sorting_prep.result_distance_latlng(propose_result_comp, origin_destination, num_post_code)

                    # get the total percentage saving of distance
                    difference_total = current_route_value - propose_route_value
                    percentage_savings = (difference_total / current_route_value) * 100

                    proposed_route_val = round(propose_route_value, 2)
                    current_route_val = round(current_route_value, 2)
                    savings_route_val = round(percentage_savings, 2)

                    result_route_savings_dic = {
                        "current_value": current_route_val,
                        "proposed_value": proposed_route_val,
                        "percentage_savings": savings_route_val,
                    }

                    # Total_summary_saving
                    result_route_value.append(result_route_savings_dic)

                # Computing consolidated summary
                # Consolidate all routes using this list

                proposed_cons_list = postal_sequence_list_cons[0]
                current_cons_list = current_sequence_list_cons[0]

                # GeoCode Map for Consolidate
                latlng_cons_array = map_visible(proposed_cons_list)

                # Distance of the routes
                origin_destination_cons = origin_result_company[0]

                # get the road distance
                proposed_cons_route_value = sorting_prep.result_distance_latlng(proposed_cons_list, origin_destination_cons, num_post_code)
                current_cons_route_value = sorting_prep.result_distance_latlng(current_cons_list, origin_destination_cons, num_post_code)

                # Converting the total percentage saving of distance
                difference_total = current_cons_route_value - proposed_cons_route_value
                percentage_savings_cons = (difference_total / current_cons_route_value) * 100

                # Summary savings
                proposed_route_val_cons = round(proposed_cons_route_value, 2)
                current_route_val_cons = round(current_cons_route_value, 2)
                savings_route_val_cons = round(percentage_savings_cons, 2)

                result_route_value_cons_dic = {
                    "current_value": current_route_val_cons,
                    "proposed_value": proposed_route_val_cons,
                    "percentage_savings": savings_route_val_cons
                }

                # Total_summary_saving
                result_route_value_cons.append(result_route_value_cons_dic)

                # Time windows:
                if time_windows == "true":

                    # Consolidate data from time windows
                    propose_result_cons_tw = propose_result_cons_tw[0]

                    # get the road distance
                    proposed_tw_value_cons = sorting_prep.result_distance_latlng(propose_result_cons_tw, origin_destination_cons, num_post_code)

                    # Converting the total percentage saving of distance
                    difference_total_tw_cons = proposed_cons_route_value - proposed_tw_value_cons
                    percentage_savings_tw_cons = (difference_total_tw_cons / proposed_cons_route_value) * 100

                    proposed_route_val_tw_cons = round(proposed_tw_value_cons, 2)
                    proposed_cons_route_value = round(proposed_cons_route_value, 2)
                    savings_route_val_tw_cons = round(percentage_savings_tw_cons, 2)

                    result_cons_route_tw = {
                        "proposed_value": proposed_cons_route_value,
                        "consolidated_routes_tw": proposed_route_val_tw_cons,
                        "percentage_savings": savings_route_val_tw_cons
                    }

                    # Consolidated_Total_summary_tw
                    total_savings_tw_cons.append(result_cons_route_tw)

                    for origin_destination, propose_result_comp_tw, propose_result_comp in itertools.izip(origin_result_company, propose_result_postal_tw, propose_result_company):

                        # Get the distance
                        proposed_tw_value = sorting_prep.result_distance_latlng(propose_result_comp_tw, origin_destination, num_post_code)
                        proposed_value = sorting_prep.result_distance_latlng(propose_result_comp, origin_destination, num_post_code)

                        # Converting the total percentage saving of distance
                        difference_total = proposed_value - proposed_tw_value
                        percentage_savings_tw = (difference_total / proposed_value) * 100

                        proposed_route_val_tw = round(proposed_tw_value, 2)
                        proposed_route_val = round(proposed_value, 2)
                        savings_route_val_tw = round(percentage_savings_tw, 2)

                        result_route_tw_value = {
                            "proposed_value": proposed_route_val,
                            "proposed_value_with_tw": proposed_route_val_tw,
                            "percentage_savings": savings_route_val_tw
                        }

                        # Total_summary_saving
                        total_savings_tw.append(result_route_tw_value)

                # # For Google MAP
                # result_list_arr = []
                # for propose_result_company_1 in propose_result_company:
                #     for propose_result_company_2 in propose_result_company_1:
                #         result_list_arr.append(propose_result_company_2)

                # Converting to string of this Proposed data
                proposed_postal = sorting.convert_to_string(propose_result_company)

                # proposed_cons_array = []
                # current_cons_array = []
                #
                # # Proposed
                # for consolidated_proposed in propose_result_sequence:
                #     for proposed_comp in consolidated_proposed:
                #         proposed_cons_array.append(proposed_comp)
                #
                # # Current
                # for consolidated_current in current_result_sequence:
                #     for proposed_comp in consolidated_current:
                #         current_cons_array.append(proposed_comp)

                # Create a Dictionary

                # postal_list_sequence = {
                #     "proposed_postal_list_seq": proposed_cons_array,
                #     "current_postal_list_seq": current_cons_array,
                # }
                #
                # # starting_postal_list
                # starting_list_seqeunce = {
                #     "starting_address": starting_postal_list
                # }
                #
                # # propose_result_company
                # propose_result_seqeunce = {
                #     "proposed_postal": propose_result_company
                # }
                # # grp_truck
                # grp_truck_sequence_1 = {
                #     "grp_truck_name": grp_truck_sequence
                # }
                #
                # # truck_sequence_list
                # truck_sequence_sequence = {
                #     "num_of_vehicle": truck_sequence_list
                # }
                #
                # # Compressing data
                # postal_list_compress = pickle.dumps(postal_list_sequence)
                # starting_address_compress = pickle.dumps(starting_list_seqeunce)
                # proposed_postal_compress = pickle.dumps(propose_result_seqeunce)
                # grp_truck_compress = pickle.dumps(grp_truck_sequence_1)
                # truck_sequence_compress = pickle.dumps(truck_sequence_sequence)
                #
                # # taskqueue.add(url='/sorting-proposed-api',
                # #               params=({
                # #                   # 'compare_id': compare_id,
                # #                   'starting_address': starting_address_compress,
                # #                   'postal_list_compress': postal_list_compress,
                # #                   'proposed_postal': proposed_postal_compress,
                # #                   'grp_truck_name': grp_truck_compress,
                # #
                # #                   'num_of_vehicle': truck_sequence_compress,
                # #
                # #                   'sort_company': sort_company,
                # #                   'options_truck': options_truck,
                # #                   'priority_capacity': priority_capacity,
                # #
                # #                   'has_return': has_return,
                # #                   'email': email,
                # #                   'num_user_load': num_user_load,
                # #
                # #               })
                # #               )

                # - - - - - - - - - - - - - - - - - #
                # Send API JSON Response Update

                if time_windows == "true":

                    response['status'] = 'ok'
                    response['sort_company'] = 'true'
                    response['data_result'] = [
                        {
                            "required_fields": {
                                "companies_hq": starting_postal_list,
                                "has_return": has_return,
                                "trucks_details": truck_sequence_list,
                                "truck_name": grp_truck_name_seq
                            },
                            "order_details_results": {
                                "postal_sequence_results": {
                                    "propose_routes": propose_result_sequence_tw,
                                    "propose_routes_total_summary_savings": result_route_value,
                                    "propose_routes_postal_latlng": latlng_array_list
                                },
                                "consolidated_postal_results": {
                                    "consolidated_routes_postal": proposed_cons_list,
                                    "consolidated_routes_total_summary_savings": result_route_value_cons,
                                    "consolidated_routes_latlng_postal": latlng_cons_array
                                },
                            },
                            "time_windows_results": {
                                "time_windows_total_savings": total_savings_tw,
                                "time_windows_consolidated_summary_routes": total_savings_tw_cons
                            }
                        }
                    ]

                else:

                    response['status'] = 'ok'
                    response['sort_company'] = 'true'
                    response['data_result'] = [
                        {
                            "required_fields": {
                                "companies_hq": starting_postal_list,
                                "has_return": has_return,
                                "trucks_details": truck_sequence_list,
                                "truck_name": vehicle_list_grp
                            },
                            "order_details_results": {
                            "postal_sequence_results": {
                                "propose_routes": propose_result_sequence,
                                "propose_routes_total_summary_savings": result_route_value,
                                "propose_routes_postal_latlng": latlng_array_list
                            },
                            "consolidated_postal_results": {
                                "consolidated_routes_postal": proposed_cons_list,
                                "consolidated_routes_total_summary_savings": result_route_value_cons,
                                "consolidated_routes_latlng_postal": latlng_cons_array
                                },
                            }
                        }
                    ]

            else:
                errors.extend(['Error in process'])
        else:
            errors.extend(['Error in JSON-Data'])

        if len(errors) > 0:
            response['status'] = 'error'
            response['errors'] = errors

        logging.info(response)
        self.response.out.write(json.dumps(response, indent=3))


def RepresentsInt(num):

    try:
        int(num)
        return True

    except ValueError:

        return False

def is_time_format(input):

    try:
        time.strptime(input, '%H:%M:%S')
        return True
    except ValueError:
        return False

# GeoCode Latlng MAP - single company
def map_visible(propose_result):
    latlng_array = []

    for vehicle_postal in propose_result:
        lat_long_Source = []

        for current_post in vehicle_postal:
            # Convert to Lat-Long the postal code
            destinations = postalcode_latlong(current_post)

            # For Geo-Code MAP
            lat_long_value_map = str(destinations)
            lat_long_value_map = lat_long_value_map.split(",")
            lat_long_Source.append(lat_long_value_map)

        # - - -  for lat & long value with vehicle number- - - #
        latlng_array.append(lat_long_Source)

    return latlng_array

def postalcode_latlong(postal):

        # Validation for Task Q
        compare_postal = postalRecordDB.check_if_exists(postal)

        if compare_postal == None:

            if postal[0] == "0":
                current_post = postal.lstrip("0")
                compare_postal = postalRecordDB.check_if_exists(current_post)
            else:
                print('load')
                nearestPostalCode = postalRecordDB.query().filter(postalRecordDB.postal_code >= postal).get(keys_only=True)
                compare_postal = nearestPostalCode.id()

        latlong = postalRecordDB.get_by_id(compare_postal)

        laglongSource = []
        laglongSource.append(latlong.lat)
        laglongSource.append(',')
        laglongSource.append(latlong.long)
        destinations = ''.join(laglongSource)

        return destinations

app = webapp2.WSGIApplication([
    ('/api/multi_truck/v1', Multi_truck_API),
    ('/api/truck_capacity/v1', Truck_capacity_API),
    ('/api/multi_companies/v1', Multi_companies_API)
], debug=True)