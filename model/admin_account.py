from google.appengine.ext import ndb
from google.appengine.api import search


class RouteDistance(ndb.Model):
    compare_id = ndb.StringProperty(required=True)
    user_id = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    starting_point = ndb.StringProperty()
    origin_destination = ndb.StringProperty()
    latVal = ndb.StringProperty()  # FloatProperty()
    longVal = ndb.StringProperty()
    no_vehicle = ndb.IntegerProperty()
    current_total_dist = ndb.FloatProperty()
    proposed_total_dist = ndb.FloatProperty()
    percentage_savings = ndb.FloatProperty()
    postal_count = ndb.IntegerProperty()
    return_vehicle = ndb.StringProperty()
    vehicle_capacity = ndb.StringProperty()
    user_count = ndb.IntegerProperty(default=0)
    type_optimise = ndb.StringProperty()
    optimise_id = ndb.IntegerProperty()

    @classmethod
    def add_new_route(cls, compare_id, user_id, starting_point, origin_destination, longVal, latVal, no_vehicle, vehicle_capacity,
                      current_total_dist, proposed_total_dist, percentage_savings, postal_count, return_vehicle,
                      user_count, type_optimise, optimise_id):

        route = RouteDistance()

        route.compare_id = compare_id
        route.user_id = user_id
        route.starting_point = starting_point
        route.origin_destination = origin_destination
        route.longVal = longVal
        route.latVal = latVal
        route.no_vehicle = no_vehicle
        route.vehicle_capacity = vehicle_capacity
        route.current_total_dist = current_total_dist
        route.proposed_total_dist = proposed_total_dist
        route.percentage_savings = percentage_savings
        route.postal_count = postal_count
        route.return_vehicle = return_vehicle
        route.user_count = user_count
        route.type_optimise = type_optimise
        route.optimise_id = optimise_id

        route.put()

        return route.key

    @classmethod
    def get_by_email(cls, email):
        user = cls.query(cls.user_id == email).get()
        return user.key.id()


class CurrentRoute(ndb.Model):
    compare_id = ndb.StringProperty(required=True)
    origin_code = ndb.StringProperty()
    postal_code = ndb.StringProperty()
    vehicle_id = ndb.IntegerProperty()
    latVal = ndb.StringProperty()   #FloatProperty()
    longVal = ndb.StringProperty()
    distance = ndb.FloatProperty()
    rank_id = ndb.IntegerProperty()
    url_id = ndb.StringProperty()
    order_id = ndb.StringProperty()
    cargo_unit = ndb.IntegerProperty()
    company_id = ndb.StringProperty()

    @classmethod
    def add_new_current_route(cls, compare_id, origin_code, postal_code, vehicle_id, latVal, longVal, url_id, distance, rank_id, order_id, cargo_unit, company_id):

        current = CurrentRoute()

        current.compare_id = compare_id
        current.origin_code = origin_code
        current.postal_code = postal_code
        current.vehicle_id = vehicle_id
        current.latVal = latVal
        current.longVal = longVal
        current.url_id = url_id
        current.distance = distance
        current.rank_id = rank_id
        current.order_id = order_id
        current.cargo_unit = cargo_unit
        current.company_id = company_id

        current.put()

        return current.key

class ProposedRoute(ndb.Model):
    compare_id = ndb.StringProperty(required=True)
    origin_code = ndb.StringProperty()
    postal_code = ndb.StringProperty()
    vehicle_id = ndb.IntegerProperty()
    latVal = ndb.StringProperty()   #FloatProperty()
    longVal = ndb.StringProperty()
    distance = ndb.FloatProperty()
    rank_id = ndb.IntegerProperty()
    url_id = ndb.StringProperty()
    order_id = ndb.StringProperty()
    cargo_unit = ndb.IntegerProperty()
    company_id = ndb.StringProperty()

    @classmethod
    def add_new_proposed_route(cls, compare_id, origin_code, postal_code, vehicle_id, latVal, longVal, url_id, distance, rank_id, order_id, cargo_unit, company_id):

        proposed = ProposedRoute()

        proposed.compare_id = compare_id
        proposed.origin_code = origin_code
        proposed.postal_code = postal_code
        proposed.vehicle_id = vehicle_id
        proposed.latVal = latVal
        proposed.longVal = longVal
        proposed.url_id = url_id
        proposed.distance = distance
        proposed.rank_id = rank_id
        proposed.order_id = order_id
        proposed.cargo_unit = cargo_unit
        proposed.company_id = company_id

        proposed.put()

        return proposed.key


class postalRecordDB(ndb.Model):
    postal_code = ndb.StringProperty()
    long = ndb.StringProperty()
    lat = ndb.StringProperty()

    @classmethod
    def add_new_records(cls, postal_code, long, lat):

        entry = postalRecordDB()

        entry.postal_code = postal_code
        entry.long = long
        entry.lat = lat

        entry.put()

        return entry.key

    @classmethod
    def delete_postal_records(cls, postal_code):

        deleterow = cls.query(cls.postal_code == postal_code).get()

        return deleterow

    @classmethod
    def search_records(cls, postal_code, long, lat):

        postal_key = cls(
            postal_code=postal_code,
            long=long,
            lat=lat,

        ).put()

        index = search.Index('postal')

        doc = search.Document(
            doc_id=str(postal_key.id()),
            fields=[
                search.TextField(postal_code='postal_code', value=postal_code),
                search.NumberField(name='longtitude', value=int(long)),
                search.NumberField(name='latitude', value=int(lat)),
            ]
        )
        index.put(doc)

    @classmethod
    def get_all_postalcode(cls, postal):

        index = search.Index('postal')

        query = 'postal_code:(%s)' % postal
        results = index.search(query)

        return results

    @classmethod
    def check_if_exists(cls, postal_code):
        check_postal = cls.query(cls.postal_code == postal_code).get(keys_only=True)

        if check_postal == None:
            return None
        else:
            postal_id = check_postal.id()
            return postal_id

    @classmethod
    def provideLatLong(cls, lat, long):
        return cls.query(cls.lat == lat, cls.long == long).fetch()

class PostalRecordDB_alert(ndb.Model):
    compare_id = ndb.StringProperty()
    created_date = ndb.StringProperty()
    postal_code = ndb.StringProperty(required=True)
    user_email = ndb.StringProperty(required=True)
    counter_no = ndb.IntegerProperty(default=0)

    @classmethod
    def add_new_postal_records(cls, compare_id, postal_code, user_email, created_date, counter_no):
        postal = cls.check_the_postal(postal_code)

        if not postal:
            # If postal is new
            new_entry = PostalRecordDB_alert()

            new_entry.compare_id = compare_id
            new_entry.postal_code = postal_code
            new_entry.user_email = user_email
            new_entry.created_date = created_date
            new_entry.counter_no = counter_no

            new_entry.put()

            # return new_entry.key
        else:

            current_num = postal.counter_no + counter_no

            postal.created_date = created_date
            postal.counter_no = current_num
            postal.put()

    @classmethod
    def get_compare_id(cls, postal):
        postal_id = cls.query(cls.postal_code == postal).get()

        if postal_id:
            compare_record = postal_id.compare_id
            return compare_record
        else:
            return None


    @classmethod
    def delete_postal_records(cls, compare_id):

        deleterow = cls.query(cls.compare_id == compare_id).get()

        return deleterow

    @classmethod
    def check_the_postal(cls, postal):
        return cls.query(cls.postal_code == postal).get()

class PostalRecordDB_history(ndb.Model):

    compare_id = ndb.StringProperty()
    created_date = ndb.StringProperty()
    postal_code = ndb.StringProperty(required=True)
    user_email = ndb.StringProperty(required=True)

    @classmethod
    def add_new_postal_records(cls, compare_id, postal_code, user_email, created_date):

        postal_entry = PostalRecordDB_history()

        postal_entry.compare_id = compare_id
        postal_entry.postal_code = postal_code
        postal_entry.user_email = user_email
        postal_entry.created_date = created_date

        postal_entry.put()

        return postal_entry.key

class Truck_capacity_details(ndb.Model):

    compare_id = ndb.StringProperty(required=True)
    no_vehicle = ndb.IntegerProperty()
    truck_details = ndb.StringProperty()
    cargo_loads = ndb.IntegerProperty()

    @classmethod
    def add_truck_details(cls, compare_id, no_vehicle, truck_details, cargo_loads):

        truck_entry = Truck_capacity_details()

        truck_entry.compare_id = compare_id
        truck_entry.no_vehicle = no_vehicle
        truck_entry.truck_details = truck_details
        truck_entry.cargo_loads = cargo_loads

        truck_entry.put()

        return truck_entry.key
