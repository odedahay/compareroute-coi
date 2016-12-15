
// Validate forms
// Route by Truck
function checkStarting_Point(starting_postal){

    var errorInput = $('.startingPoint');
    var errorMessage;

    // create regex to validate if numbers onlyåå
    var reg = /^[0-9]+$/;

    if(starting_postal === 'undefined'  || starting_postal === ''){

        errorMessage = "*Postal Code required!";
        errorInput.fadeIn();
        errorInput.html(errorMessage);

        return false;

    }else if( (starting_postal.length) < 5 || (starting_postal.length) > 6 ){

        //console.log(errorMessage);
        errorMessage = "*Postal Code should only be 6 digits";
        errorInput.fadeIn();
        errorInput.html(errorMessage);

        return false;

    }else if (!reg.test(starting_postal)){

        errorMessage = "*Postal Code should be numbers only";
        errorInput.fadeIn();
        errorInput.html(errorMessage);

        return false;

    }else{

        errorInput.hide();
        return true;

    }
} // end

// validation function for Postal Sequence
function postalSequence_area(postal_sequence){
    var errorInput = $(".postalSeq");
    var errorMessage;

    if(postal_sequence === ""){

        errorMessage = "*Please, Enter your Delivery Location Details!";
        errorInput.fadeIn();
        errorInput.html(errorMessage);

        return;

    }else{

        errorInput.hide();
        return true;
    }
}
// Function for sub 2 fields
function truck_capacity_limit_2(num_of_truck, num_of_truck_1){
     var errorNumTruck2 = $(".numTruck_1");
     var limitTruck = parseInt(num_of_truck) + parseInt(num_of_truck_1);


     return truck_capacity_limit_body(errorNumTruck2, limitTruck);
}

// Function for sub 3 fields
function truck_capacity_limit_3(num_of_truck, num_of_truck_1, num_of_truck_2){

     var errorNumTruck2 = $(".numTruck_2");
     var limitTruck = parseInt(num_of_truck) + parseInt(num_of_truck_1) + parseInt(num_of_truck_2);

     //console.log('limitTruck', limitTruck);

     return truck_capacity_limit_body(errorNumTruck2, limitTruck);
}

// Body function of truck_capacity_limit_*
function truck_capacity_limit_body(errorNumTruck2, limitTruck){
		var errorMessage;
    errorNumTruck2.hide();

    //check the fields if empty
    // parseInt(num_of_truck) > 15
    if(parseInt(limitTruck) > 15 ){

        errorMessage = "*Total maximum of 15 Truck valid only";
        errorNumTruck2.fadeIn();
        errorNumTruck2.html(errorMessage);

        return false;
    }
    else{
        errorNumTruck2.hide();
        return true;
    }
}

// validation for truck capacity
function truck_capacity_area(type_of_truck, truck_capacity, num_of_truck){

    var errorInput1 = $(".typeTruck");
    var errorInput2 = $(".truckCapacity");
    var errorInput3 = $(".numTruck");

    var errorMessage;
     // create regex to validate if numbers onlyåå
    var reg = /^[0-9]+$/;

    errorInput1.hide();
    errorInput2.hide();
    errorInput3.hide();

    //check the fields if empty
    if(type_of_truck === ""){

        errorMessage = "*Please Enter Type of Truck!";
        errorInput1.fadeIn();
        errorInput1.html(errorMessage);

        return false;
    }
    else if( truck_capacity === "" || parseInt(truck_capacity) <= 0 || !reg.test(truck_capacity) ){

        errorMessage = "*Please Enter Valid Truck Capacity";
        errorInput2.fadeIn();
        errorInput2.html(errorMessage);

        return false;
    }
    else if( num_of_truck === "" || parseInt(num_of_truck) <= 0  || !reg.test(num_of_truck) ){

        errorMessage = "*Please Enter Valid Number of Truck";
        errorInput3.fadeIn();
        errorInput3.html(errorMessage);

        return false;
    }
    else if(  parseInt(num_of_truck) > 15 ){

        errorMessage = "*Maximum of 15 Truck valid only";
        errorInput3.fadeIn();
        errorInput3.html(errorMessage);

        return false;

    }
    else{

        errorInput1.hide();
        errorInput2.hide();
        errorInput3.hide();
        return true;
    }

}

// validation for truck capacity second field
function truck_capacity_area_1(type_of_truck_1, truck_capacity_1, num_of_truck_1){

    var errorInput1 = $(".typeTruck_1");
    var errorInput2 = $(".truckCapacity_1");
    var errorInput3 = $(".numTruck_1");

    var errorMessage;
    var reg = /^[0-9]+$/;

     errorInput1.hide();
     errorInput2.hide();
     errorInput3.hide();

    //check the fields if empty
    if(type_of_truck_1 === ""){

        errorMessage = "*Please Enter Types of Truck!";
        errorInput1.fadeIn();
        errorInput1.html(errorMessage);

        return false;

    }
    else if( truck_capacity_1 === "" || parseInt(truck_capacity_1) <= 0 || !reg.test(truck_capacity_1) ){

        errorMessage = "*Please Enter Valid Truck Capacity ";
        errorInput2.fadeIn();
        errorInput2.html(errorMessage);

        return false;
    }
    else if( num_of_truck_1 === "" || parseInt(num_of_truck_1) <= 0 || !reg.test(num_of_truck_1) ){

        errorMessage = "*Please Enter valid Number of Truck";
        errorInput3.fadeIn();
        errorInput3.html(errorMessage);

        return false;
    }
    else{
        errorInput1.hide();
        errorInput2.hide();
        errorInput3.hide();
        return true;
    }
}

// validation for truck capacity third field
function truck_capacity_area_2(type_of_truck_2, truck_capacity_2, num_of_truck_2){

    var errorInput1 = $(".typeTruck_2");
    var errorInput2 = $(".truckCapacity_2");
    var errorInput3 = $(".numTruck_2");

    var errorMessage;
    var reg = /^[0-9]+$/;

     errorInput1.hide();
     errorInput2.hide();
     errorInput3.hide();

    //check the fields if empty
    if(type_of_truck_2 === ""){

        errorMessage = "*Please Enter Types of Truck!";
        errorInput1.fadeIn();
        errorInput1.html(errorMessage);

        return false;

    }
    else if( truck_capacity_2 === "" || parseInt(truck_capacity_2) <= 0 || !reg.test(truck_capacity_2) ){

        errorMessage = "*Please Enter Valid Truck Capacity ";
        errorInput2.fadeIn();
        errorInput2.html(errorMessage);

        return false;
    }
    else if( num_of_truck_2 === ""|| parseInt(num_of_truck_2) <= 0 || !reg.test(num_of_truck_2) ){

        errorMessage = "*Please Enter valid Number of Truck";
        errorInput3.fadeIn();
        errorInput3.html(errorMessage);

        return false;
    }
    else{
        errorInput1.hide();
        errorInput2.hide();
        errorInput3.hide();
        return true;
    }
}

// Route by Companies:
// Starting Point Validation 1
function checkStarting_Point_comp_selector_1(starting_postal){
    var errorInput = $(".startingPostal_1");
    return checkStarting_Point_comp_body(errorInput, starting_postal);
}
// Starting Point Validation 2
function checkStarting_Point_comp_selector_2(starting_postal){
    var errorInput = $(".startingPostal_2");
    return checkStarting_Point_comp_body(errorInput, starting_postal);
}
// Starting Point Validation 3
function checkStarting_Point_comp_selector_3(starting_postal){
    var errorInput = $(".startingPostal_3");
    return checkStarting_Point_comp_body(errorInput, starting_postal);
}
// main body of checkStarting_Point_comp_selector
function checkStarting_Point_comp_body(errorInput, starting_postal){

    var errorMessage;

    // create regex to validate if numbers onlyåå
    var reg = /^[0-9]+$/;

    if(starting_postal === "undefined"  || starting_postal === ""){

        errorMessage = "*Postal Code required!";
        errorInput.fadeIn();
        errorInput.html(errorMessage);

        return false;

    }else if( (starting_postal.length) < 5 || (starting_postal.length) > 6 ){

        //console.log(errorMessage);
        errorMessage = "*Postal Code should only be 6 digits";
        errorInput.fadeIn();
        errorInput.html(errorMessage);

        return false;

    }else if (!reg.test(starting_postal)){

        errorMessage = "*Postal Code should be numbers only";
        errorInput.fadeIn();
        errorInput.html(errorMessage);

        return false;

    }else{

        errorInput.hide();
        return true;

    }
} // end

//////////////////////////////
// Vehicle Count Validation 1
function checkVehicle_comp_selector_1(vehicle_quantity){
    var errorInput = $(".vehicleQuantity_1");
    return vehicleCount_comp_body(errorInput, vehicle_quantity);
}
// Vehicle Count Validation 2
function checkVehicle_comp_selector_2(vehicle_quantity){
    var errorInput = $(".vehicleQuantity_2");
    return vehicleCount_comp_body(errorInput, vehicle_quantity);
}
// Vehicle Count Validation 3
function checkVehicle_comp_selector_3(vehicle_quantity){
    var errorInput = $(".vehicleQuantity_3");
    return vehicleCount_comp_body(errorInput, vehicle_quantity);
}
// main body of checkStarting_Point_comp_selector
function vehicleCount_comp_body(errorInput, vehicle_quantity){

    var errorMessage;

    // create regex to validate if numbers onlyåå
    var reg = /^[0-9]+$/;

    if(vehicle_quantity === "undefined"  || vehicle_quantity === ""){

        errorMessage = "*Please Enter Number of Truck!";
        errorInput.fadeIn();
        errorInput.html(errorMessage);

        return false;

    //(vehicle_quantity.length) <= 0 || (vehicle_quantity.length) > 15
    }else if(vehicle_quantity === "" || parseInt(vehicle_quantity) <= 0 || !reg.test(vehicle_quantity) ){

        errorMessage = "*Please Enter Valid Number of Truck!";
        errorInput.fadeIn();
        errorInput.html(errorMessage);

        return false;

    }else if(  parseInt(vehicle_quantity) > 15 ){

        errorMessage = "*Maximum of 15 Truck valid only";
        errorInput.fadeIn();
        errorInput.html(errorMessage);

        return false;

    }
    else{

        errorInput.hide();
        return true;

    }
} // end

//////////////////////////////
// Company Capacity Truck Validation 1
function truck_capacity_area_comp_1(type_of_truck, truck_capacity, num_of_truck){

    var errorInput1 = $(".typeTruck_c1");
    var errorInput2 = $(".truckCapacity_c1");
    var errorInput3 = $(".numTruck_c1");
    // call function to validate fields
    return truck_capacity_area_body_comp(errorInput1, errorInput2, errorInput3, type_of_truck, truck_capacity, num_of_truck);
}
// Company Capacity Truck Validation 1 - sub-additional page 1 sub 2
function truck_capacity_area_comp_1a(type_of_truck, truck_capacity, num_of_truck){

    var errorInput1 = $(".typeTruck_cc1");
    var errorInput2 = $(".truckCapacity_cc1");
    var errorInput3 = $(".numTruck_cc1");
    // call function to validate fields
    return truck_capacity_area_body_comp(errorInput1, errorInput2, errorInput3, type_of_truck, truck_capacity, num_of_truck);
}
// Company Capacity Truck Validation 1 - sub-additional page 1 sub 2
function truck_capacity_area_comp_1b(type_of_truck, truck_capacity, num_of_truck){

    var errorInput1 = $(".typeTruck_cc2");
    var errorInput2 = $(".truckCapacity_cc2");
    var errorInput3 = $(".numTruck_cc2");
    // call function to validate fields
    return truck_capacity_area_body_comp(errorInput1, errorInput2, errorInput3, type_of_truck, truck_capacity, num_of_truck);
}

// Company Capacity Truck Validation 2
function truck_capacity_area_comp_2(type_of_truck, truck_capacity, num_of_truck){

    var errorInput1 = $(".typeTruck_c2");
    var errorInput2 = $(".truckCapacity_c2");
    var errorInput3 = $(".numTruck_c2");
    // call function to validate fields
    return truck_capacity_area_body_comp(errorInput1, errorInput2, errorInput3, type_of_truck, truck_capacity, num_of_truck);
}
// Company Capacity Truck Validation 2 - sub-additional page 1 x2
function truck_capacity_area_comp_2a(type_of_truck, truck_capacity, num_of_truck){

    var errorInput1 = $(".typeTruck_cc21");
    var errorInput2 = $(".truckCapacity_cc21");
    var errorInput3 = $(".numTruck_cc211");
    // call function to validate fields
    return truck_capacity_area_body_comp(errorInput1, errorInput2, errorInput3, type_of_truck, truck_capacity, num_of_truck);
}
// Company Capacity Truck Validation 2 - sub-additional page 1 x2
function truck_capacity_area_comp_2b(type_of_truck, truck_capacity, num_of_truck){

    var errorInput1 = $(".typeTruck_cc22");
    var errorInput2 = $(".truckCapacity_cc22");
    var errorInput3 = $(".numTruck_cc22");
    // call function to validate fields
    return truck_capacity_area_body_comp(errorInput1, errorInput2, errorInput3, type_of_truck, truck_capacity, num_of_truck);
}
/////////
// Company Capacity Truck Validation 3
function truck_capacity_area_comp_3(type_of_truck, truck_capacity, num_of_truck){

    var errorInput1 = $(".typeTruck_c3");
    var errorInput2 = $(".truckCapacity_c3");
    var errorInput3 = $(".numTruck_c3");
    // call function to validate fields
    return truck_capacity_area_body_comp(errorInput1, errorInput2, errorInput3, type_of_truck, truck_capacity, num_of_truck);
}

// Company Capacity Truck Validation 3 - sub-additional page 1 x2
function truck_capacity_area_comp_3a(type_of_truck, truck_capacity, num_of_truck){

    var errorInput1 = $(".typeTruck_cc31");
    var errorInput2 = $(".truckCapacity_cc31");
    var errorInput3 = $(".numTruck_cc31");
    // call function to validate fields
    return truck_capacity_area_body_comp(errorInput1, errorInput2, errorInput3, type_of_truck, truck_capacity, num_of_truck);
}
// Company Capacity Truck Validation 3 - sub-additional page 2 x 2
function truck_capacity_area_comp_3b(type_of_truck, truck_capacity, num_of_truck){

    var errorInput1 = $(".typeTruck_cc32");
    var errorInput2 = $(".truckCapacity_cc32");
    var errorInput3 = $(".numTruck_cc32");
    // call function to validate fields
    return truck_capacity_area_body_comp(errorInput1, errorInput2, errorInput3, type_of_truck, truck_capacity, num_of_truck);
}
/////////
// Company Capacity Truck Body
function truck_capacity_area_body_comp(errorInput1, errorInput2, errorInput3, type_of_truck, truck_capacity, num_of_truck){

    var errorMessage;
     // create regex to validate if numbers onlyåå
    var reg = /^[0-9]+$/;

    errorInput1.hide();
    errorInput2.hide();
    errorInput3.hide();

    //check the fields if empty
    if(type_of_truck === ""){

        errorMessage = "*Please Enter Type of Truck!";
        errorInput1.fadeIn();
        errorInput1.html(errorMessage);

        return false;

    }
    else if( truck_capacity === "" || parseInt(truck_capacity) <= 0 || !reg.test(truck_capacity) ){

        errorMessage = "*Please Enter Valid Truck Capacity";
        errorInput2.fadeIn();
        errorInput2.html(errorMessage);

        return false;
    }
    else if( num_of_truck === "" || parseInt(num_of_truck) <= 0  || !reg.test(num_of_truck) ){

        errorMessage = "*Please Enter Valid Number of Truck";
        errorInput3.fadeIn();
        errorInput3.html(errorMessage);

        return false;
    }
    else if(  parseInt(num_of_truck) > 15 ){

        errorMessage = "*Maximum of 15 Truck valid only";
        errorInput3.fadeIn();
        errorInput3.html(errorMessage);

        return false;

    }
    else{

        errorInput1.hide();
        errorInput2.hide();
        errorInput3.hide();
        return true;
    }

}
