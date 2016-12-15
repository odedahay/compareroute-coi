'''
Created on 17 Jun, 2015

@author: muhammad_nickman
'''
import webapp2
import json

class capacityHandler(webapp2.RequestHandler):
    def post(self):

        try:    
            jsonstring = self.request.body
            jsonobject = json.loads(jsonstring)
    
        
            
            # Initiate the json reply dictionary
            # And all the other replies
            json_vehicle_dict = {}
            error = False
            errorMsg = []
            
           
            #####    CATCH ERROR IF ARGUEMENTS NOT FOUND ###
            if "starting address" not in jsonobject:
                error = True
                errorMsg.append("Missing starting address")
            else :
                starting_address = jsonobject["starting address"]
                
            if "vehicle details" not in jsonobject:
                error = True
                errorMsg.append("Missing vehicle details")
            else:
                vehicle_details = jsonobject["vehicle details"]
                
                if "number of vehicles" not in vehicle_details:
                    error = True
                    errorMsg.append("Missing number of vehicles")
                else:
                    num_of_vehicle = vehicle_details["number of vehicles"]
                if "capacity" not in vehicle_details:
                    error = True
                    errorMsg.append("Missing capacity of vehicles")
                else:
                    vehicle_capacity = vehicle_details["capacity"]
                
            if "order details" not in jsonobject:
                error = True
                errorMsg.append("Missing order details")
            else:
                order_details = jsonobject["order details"]
                
            for order in order_details:
                if "address" not in order or "order id" not in order:
                    error =True
                    errorMsg.append("Missing order address or id")
                try: 
                    address = int(order["address"])
                except:
                    error =True
                    errorMsg.append("Invalid format for address")
            # END OF ERROR CHECKING           
                 
            # START OF LOGIC IF NO ERROR FOUND     
            if  not error:
        
            
                # Initialize all the objects needed
                # Capacity dict to store the capacity value of each order
                capacity_dict = {}
                # Postal dictionary for linking all orders with same postal codes tgt
                postal_dict = {}      
                # List of all unique postal codes
                postal_list = []
                # Order dict with all the relevant information of each specific order
                total_order_size = 0
                order_dict = {}
                
                # Order taken dict
                order_taken_dict = {}
                for order in order_details:
                    address = int(order["address"])
                    order_id = order["order id"]  
                    capacity = int(order["size"])  
                    total_order_size += capacity
                    order_taken_dict[order_id] = True
                    postal_list.append(address)
                    capacity_dict[order_id] = capacity
                    if address not in postal_dict.keys():
                        postal_dict[address] = []
                    postal_dict[address].append(order_id)
                    if order_id not in order_dict.keys():
                        order_dict[order_id] = []
                    # CAN ADD OTHER INFORMATION 
                    order_dict[order_id].append(address)
                    
                # Initialize the rankings    
                areaCodeRanking_dict = createPostalRanking()    
                # Rearrange the postal code with reference to the starting address
                areaCodeRanking_dict = arrangePostal(starting_address,areaCodeRanking_dict)
                # Obtain a list of sorted postal code
                custPostal_arr_sorted = sortPostalArray(areaCodeRanking_dict,postal_list)
                if custPostal_arr_sorted is None:
                    error = True
                    errorMsg.append("Invalid postal code")
                else:
                    # initialize the result array
                    results = []
                    # split postal codes into list for each vehicle
                    vehicle_postal_list = chunkIt(custPostal_arr_sorted,num_of_vehicle)
                
                    for vpostal_list in vehicle_postal_list:
                        
                        vehicle_order_list=[]
                        for postal in vpostal_list:
                            vehicle_order_list.extend(postal_dict[int(postal)])
                        results.append(vehicle_order_list)
                    
                    json_vehicle_dict["status"] = "success"
                    json_vehicle_dict["vehicles"] = []
                   
                
                    
                    for result in results:
                        json_order_dict = {}
                        json_order_dict["orders"] = []
                        temp_capacity =0
                        for each in result:
                            json_each_dict = {}
                            json_each_dict["order id"] = each
                            json_each_dict["address"] = order_dict[each][0]
                            json_order_dict["orders"].append(json_each_dict)
                            temp_capacity += capacity_dict[each]
                            #print temp_capacity
                        if temp_capacity > vehicle_capacity:
                            json_order_dict["capacity"] = False
                        else :
                            print temp_capacity
                            json_order_dict["capacity"] = True
                        json_vehicle_dict["vehicles"].append(json_order_dict)
                    
            if error: 
                json_vehicle_dict["status"] = "error"
                json_vehicle_dict["errMsg"] = errorMsg
            self.response.out.write(json.dumps(json_vehicle_dict,indent=4))
        except:
            out = {"status" : "error", "errMsg" : "Require json format input"}
            self.response.out.write(json.dumps(out,indent=1))
    
        
            
def sortPostalArray(areaCodeRanking_dict,postal_list):
        
        # Hash for the ranked but unsorted postal codes
        custPostal_dict_unsorted = {}
        
        # Array to store current sequence of postal codes
        currentSeq = []
        
        # For every postal codes, obtain and assign the respective rank
        for postal in postal_list:
        
            # Convert into string and remove white spaces
            postal_str = str(postal)
            postal_str = postal_str.strip()
    
            # Check if postal code is a valid value i.e. Contains only five or six digits
            if not str.isdigit(postal_str) or len(postal_str) != 5 and len(postal_str) != 6:
                return None
            # Add "0" in front of five digit postal codes
            if len(postal_str) == 5:
                postal_str = "0" + postal_str
            
        
            # Record current sequence of postal codes
            currentSeq.append(postal_str)
         
            # Obtain rank for postal code
            rank = areaCodeRanking_dict[postal_str[0:2]]
             
            # Store postal code and rank into hash
            custPostal_dict_unsorted[postal_str] = rank    
                 
        # Sort the hash by rank then postal
        custPostal_arr_sorted = sorted(custPostal_dict_unsorted, key = lambda key: (int(custPostal_dict_unsorted[key]), key))
    
        
        # Send email with current and sorted sequence of postal codes
        # sendEmail(currentSeq, custPostal_arr_sorted)    
        # Return result
        return custPostal_arr_sorted
        
    # method used to break down a list into equal parts    
def chunkIt(seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0
    
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
    
        return out
      
                
def arrangePostal(starting_address,areaCodeRanking_dict) :
        # Add a 0 in front of the address if it has 5digit
        starting_address = str(starting_address)
        if len(starting_address) == 5 :
            starting_address = "0"+ starting_address
        # Get the first 2 digit of the postal code
        current_location = starting_address[0:2]
        # Get the current ranking of starting address
        current_ranking = areaCodeRanking_dict[current_location]
        
        # Get the number of postal ranking in the dictionary
        total_ranking = len(areaCodeRanking_dict)
        
        # Get the number to adjust
        adjustment  = total_ranking - current_ranking
        
        for key in areaCodeRanking_dict.keys() :
            areaCodeRanking_dict[key] = ((areaCodeRanking_dict[key] + adjustment) % total_ranking )+ 1
        return areaCodeRanking_dict
        
            
def createPostalRanking():
        
        
        # Hash for area codes and rank
        areaCodeRanking_dict = {}
     
    
        # Fix the dict
        areaCodeRanking_dict['63'] = 1
        areaCodeRanking_dict['70'] = 2
        areaCodeRanking_dict['71'] = 3
        areaCodeRanking_dict['69'] = 4
        areaCodeRanking_dict['68'] = 5
        areaCodeRanking_dict['72'] = 6
        areaCodeRanking_dict['73'] = 7
        areaCodeRanking_dict['76'] = 8
        areaCodeRanking_dict['75'] = 9
        areaCodeRanking_dict['77'] = 10
        areaCodeRanking_dict['78'] = 11
        areaCodeRanking_dict['79'] = 12
        areaCodeRanking_dict['80'] = 13
        areaCodeRanking_dict['56'] = 14
        areaCodeRanking_dict['55'] = 15
        areaCodeRanking_dict['36'] = 16
        areaCodeRanking_dict['37'] = 17
        areaCodeRanking_dict['53'] = 18
        areaCodeRanking_dict['54'] = 19
        areaCodeRanking_dict['82'] = 20
        areaCodeRanking_dict['50'] = 21
        areaCodeRanking_dict['51'] = 22
        areaCodeRanking_dict['49'] = 23
        areaCodeRanking_dict['81'] = 24
        areaCodeRanking_dict['48'] = 25
        areaCodeRanking_dict['52'] = 26
        areaCodeRanking_dict['46'] = 27
        areaCodeRanking_dict['47'] = 28
        areaCodeRanking_dict['41'] = 29
        areaCodeRanking_dict['40'] = 30
        areaCodeRanking_dict['42'] = 31
        areaCodeRanking_dict['44'] = 32
        areaCodeRanking_dict['45'] = 33
        areaCodeRanking_dict['43'] = 34
        areaCodeRanking_dict['04'] = 35
        areaCodeRanking_dict['01'] = 36
        areaCodeRanking_dict['07'] = 37
        areaCodeRanking_dict['08'] = 38
        areaCodeRanking_dict['09'] = 39
        areaCodeRanking_dict['15'] = 40
        areaCodeRanking_dict['10'] = 41
        areaCodeRanking_dict['11'] = 42
        areaCodeRanking_dict['14'] = 43
        areaCodeRanking_dict['25'] = 44
        areaCodeRanking_dict['24'] = 45
        areaCodeRanking_dict['23'] = 46
        areaCodeRanking_dict['05'] = 47
        areaCodeRanking_dict['06'] = 48
        areaCodeRanking_dict['16'] = 49
        areaCodeRanking_dict['17'] = 50
        areaCodeRanking_dict['03'] = 51
        areaCodeRanking_dict['18'] = 52
        areaCodeRanking_dict['22'] = 53
        areaCodeRanking_dict['30'] = 54
        areaCodeRanking_dict['21'] = 55
        areaCodeRanking_dict['33'] = 56
        areaCodeRanking_dict['20'] = 57
        areaCodeRanking_dict['19'] = 58
        areaCodeRanking_dict['39'] = 59
        areaCodeRanking_dict['38'] = 60
        areaCodeRanking_dict['34'] = 61
        areaCodeRanking_dict['35'] = 62
        areaCodeRanking_dict['32'] = 63
        areaCodeRanking_dict['31'] = 64
        areaCodeRanking_dict['57'] = 65
        areaCodeRanking_dict['29'] = 66
        areaCodeRanking_dict['28'] = 67
        areaCodeRanking_dict['26'] = 68
        areaCodeRanking_dict['27'] = 69
        areaCodeRanking_dict['58'] = 70
        areaCodeRanking_dict['67'] = 71
        areaCodeRanking_dict['66'] = 72
        areaCodeRanking_dict['59'] = 73
        areaCodeRanking_dict['60'] = 74
        areaCodeRanking_dict['65'] = 75
        areaCodeRanking_dict['64'] = 76
        areaCodeRanking_dict['61'] = 77
        areaCodeRanking_dict['12'] = 78
        areaCodeRanking_dict['13'] = 79
        areaCodeRanking_dict['62'] = 80
        return areaCodeRanking_dict
            
            
        
        
app = webapp2.WSGIApplication([
    ('/json/capacity',capacityHandler)
], debug=True)
