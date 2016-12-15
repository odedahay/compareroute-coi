from handlers import base
from datetime import datetime
from model.admin_account_api import ProposedRoute_api, CurrentRoute_api, RouteDistance_api
from handlers.postalchecker import postalRecordDB
import urllib
import json
import itertools
import pickle
import sorting, sorting_task



class TaskRouteHandlerProposed_api(base.BaseHandler):
    def post(self):

        if not 'X-AppEngine-TaskName' in self.request.headers:
            self.error(403)

        # Important Data
        proposed_postal = self.request.get('proposed_postal')
        postal_list_compress = self.request.get('postal_list_compress')

        # Basic Data
        # compare_id = self.request.get('compare_id')
        starting_address = self.request.get('starting_address')
        num_user_load = self.request.get('num_user_load')

        # Optimization
        sort_company = self.request.get('sort_company')
        options_truck = self.request.get('options_truck')
        priority_capacity = self.request.get('priority_capacity')

        num_of_vehicle = self.request.get('num_of_vehicle')
        email = self.request.get('email')
        has_return = self.request.get('has_return')
        grp_truck_name = self.request.get('grp_truck_name')

        vehicle_capacity = self.request.get('vehicle_capacity')

        compare_id = datetime.now().strftime('%Y%m%d%H%m%f')

        # Id for type of optimization use by user
        optimise_id = ""

        if options_truck == "true":
            optimise_id = 1

        elif priority_capacity == "true":
            optimise_id = 2

        elif sort_company == "true":
            optimise_id = 3

        # Return vehicle
        if has_return == "true":
            return_vehicle = "Yes"
        else:
            return_vehicle = "No"

        user_count = 0
        # Counter Sign
        if num_user_load == "true":
            user_count += 1

        if sort_company == "true":

            # Counting the number of postal code:
            actual_vehicle_postal = proposed_postal.split("_")
            postal_count_arr = []

            for vehicle_postal in actual_vehicle_postal:
                vehicle_postal = vehicle_postal.split(", ")

                for current_post in vehicle_postal:
                    postal_count_arr.append(current_post)

            postal_count = len(postal_count_arr)

            # Decompress the data
            sorting_data = pickle.loads(str(postal_list_compress))

            # GeoCode
            origin_destination, lat, long = sorting.startingpoint_latlong(starting_address)

            # Define the function
            proposed_total_dist = self.task_proposed_Route(compare_id, email, starting_address, origin_destination, sort_company, priority_capacity, **sorting_data)
            current_total_dist = self.task_current_Route(compare_id, email, starting_address, origin_destination, sort_company, priority_capacity, **sorting_data)

            # Total Percentage Saving
            difference_total = current_total_dist - proposed_total_dist
            percentage_savings = (difference_total / current_total_dist) * 100

            # Vehicle
            for truck_num in truck_sequence_sequence["num_of_vehicle"]:
                print "num_of_vehicle", truck_num

            RouteDistance_api.add_new_route_api(compare_id, email, starting_address, origin_destination, 1, vehicle_capacity, float(current_total_dist),
                                                float(proposed_total_dist), round(percentage_savings, 2), int(postal_count), return_vehicle, int(user_count), optimise_id)
        else:
            # Counting the number of postal code:
            actual_vehicle_postal = proposed_postal.split("_")
            postal_count_arr = []

            for vehicle_postal in actual_vehicle_postal:
                vehicle_postal = vehicle_postal.split(", ")

                for current_post in vehicle_postal:
                    postal_count_arr.append(current_post)

            postal_count = len(postal_count_arr)

            # GeoCode
            origin_destination, lat, long = sorting.startingpoint_latlong(starting_address)

            # Decompress the data
            sorting_data = pickle.loads(str(postal_list_compress))

            # Define the function
            proposed_total_dist = self.task_proposed_Route(compare_id, email, starting_address, origin_destination, sort_company, priority_capacity, **sorting_data)
            current_total_dist = self.task_current_Route(compare_id, email, starting_address, origin_destination, sort_company, priority_capacity, **sorting_data)

            # Total Percentage Saving
            difference_total = current_total_dist - proposed_total_dist
            percentage_savings = (difference_total / current_total_dist) * 100

            RouteDistance_api.add_new_route_api(compare_id, email,
                                                starting_address,
                                                origin_destination,
                                                int(num_of_vehicle),
                                                vehicle_capacity,
                                                float(current_total_dist),
                                                float(proposed_total_dist),
                                                round(percentage_savings, 2), int(postal_count), return_vehicle,
                                                int(user_count), optimise_id)

    def task_proposed_Route(self, compare_id, email, starting_address, origin_destination, sort_company, priority_capacity, **sorting_data):

        origin_postcode = starting_address
        origin_destination = origin_destination

        vehicle_count = 0
        proposed_total_dist = 0

        for truck_count in sorting_data["proposed_postal_list_seq"]:

            vehicle_count += 1
            postal_rank = 0

            for postal_count in truck_count:
                postal_rank += 1

                proposed_post = postal_count[0]
                order_id = postal_count[1]
                cargo_unit = 0

                if priority_capacity == "true":
                    cargo_unit = postal_count[2]

                company_id = "None"
                if sort_company == "true":
                    company_id = postal_count[3]

                destinations, latval, longval = postalcode_latlong(proposed_post, compare_id, email)

                distance1 = "http://dev.logistics.lol:5000/viaroute?loc=" + origin_destination + "&loc=" + destinations

                # Url Link each postal code
                url_id = distance1

                dist_val = urllib.urlopen(distance1)
                wjson = dist_val.read()
                distance2 = json.loads(wjson)
                distance3 = distance2['route_summary']['total_distance']
                distance_km = float(distance3) / 1000

                proposed_total_dist = proposed_total_dist + distance_km

                origin_destination = destinations

                # # Storing the data in Proposed Route
                # if (postal_rank == 1):
                #
                #     ProposedRoute_api.add_new_proposed_route_api(compare_id, starting_address, proposed_post, int(vehicle_count), longval, latval, url_id, round(float(distance_km), 2), int(postal_rank), order_id, cargo_unit, company_id)
                # else:
                #     ProposedRoute_api.add_new_proposed_route_api(compare_id, origin_postcode, proposed_post, int(vehicle_count), longval, latval, url_id, round(float(distance_km), 2), int(postal_rank), order_id, cargo_unit, company_id)
                #
                # origin_postcode = proposed_post

        return proposed_total_dist

    def task_current_Route(self, compare_id, email, starting_address, origin_destination, sort_company, priority_capacity, **sorting_data):

        origin_postcode = starting_address
        origin_destination = origin_destination

        vehicle_count = 0
        current_total_dist = 0

        for truck_count in sorting_data["current_postal_list_seq"]:

            vehicle_count += 1
            postal_rank = 0

            for postal_count in truck_count:
                postal_rank += 1

                current_post = postal_count[0]
                order_id = postal_count[1]

                cargo_unit = 0

                if priority_capacity == "true":
                    cargo_unit = postal_count[2]

                company_id = "None"

                if sort_company == "true":
                    company_id = postal_count[3]

                destinations, latval, longval = postalcode_latlong(current_post, compare_id, email)

                distance1 = "http://dev.logistics.lol:5000/viaroute?loc=" + origin_destination + "&loc=" + destinations

                # Url Link each postal code
                url_id = distance1

                dist_val = urllib.urlopen(distance1)
                wjson = dist_val.read()
                distance2 = json.loads(wjson)
                distance3 = distance2['route_summary']['total_distance']
                distance_km = float(distance3) / 1000

                current_total_dist = current_total_dist + distance_km

                origin_destination = destinations

                # # Storing the data in Proposed Route
                # if (postal_rank == 1):
                #     CurrentRoute_api.add_new_current_route_api(compare_id, starting_address, current_post, int(vehicle_count), longval, latval, url_id, round(float(distance_km), 2), int(postal_rank), order_id, cargo_unit, company_id)
                #
                # else:
                #     CurrentRoute_api.add_new_current_route_api(compare_id, origin_postcode, current_post, int(vehicle_count), longval, latval, url_id, round(float(distance_km), 2), int(postal_rank), order_id, cargo_unit, company_id)
                #
                # origin_postcode = current_post

        return current_total_dist


# To check weather the Postal Code is exits:
def postalcode_latlong(current_post, compare_id, email):

    # Time recording only
    currentDateTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    counter_no = 0

    # Validation for Task Q
    compare_postal = postalRecordDB.check_if_exists(current_post)

    if compare_postal == None:

        counter_no += 1

        if current_post[0] == "0":
            current_post = current_post.lstrip("0")
            compare_postal = postalRecordDB.check_if_exists(current_post)

        else:
            print('No Postal Code Record- API')

            PostalRecordDB_alert.add_new_postal_records(compare_id, current_post, email, currentDateTime, int(counter_no))

            nearestPostalCode = postalRecordDB.query().filter(postalRecordDB.postal_code >= current_post).get(keys_only=True)
            compare_postal = nearestPostalCode.id()

    latlong = postalRecordDB.get_by_id(compare_postal)

    laglongSource = []
    laglongSource.append(latlong.lat)
    laglongSource.append(',')
    laglongSource.append(latlong.long)
    destinations = ''.join(laglongSource)

    latval = latlong.lat
    longval = latlong.long

    return destinations, latval, longval