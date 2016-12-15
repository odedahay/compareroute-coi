import itertools
import operator

# Variable for validation:
error_Num_of_truck = "Add more Truck! <br />The minimum balance number of delivery truck  "


response = {}


def cargo_unit_checker_for_comp(num_comp_val, postal_sequence_company, **truck_capacity_dict):

    errors = []
    error_cargo_unit_companies_priority = " has been exceeding to maximum Truck Capacity <br />"

    # count the company entered:
    # if two companies
    if int(num_comp_val) == 2:

        truck_capacity_c1 = truck_capacity_dict['truck_capacity_c1']
        truck_capacity_c2 = truck_capacity_dict['truck_capacity_c2']

        # separate each company
        company1 = postal_sequence_company[0]
        company2 = postal_sequence_company[1]

        # Iterate each cargo unit
        # check if there is more than minimum value of cargo unit
        for company_grp_1, company_grp_2 in itertools.izip(company1, company2):

            # iterate for company 1
            postal_code1 = company_grp_1[0]
            cargo_unit1 = int(company_grp_1[2])
            company_id1 = company_grp_1[3]

            # iterate for company 2
            postal_code2 = company_grp_2[0]
            cargo_unit2 = int(company_grp_2[2])
            company_id2 = company_grp_2[3]

            # if there is more the minimum value throw an error:
            # print "error_cargo1", cargo_unit1 > int(truck_capacity_c1)

            if cargo_unit1 > int(truck_capacity_c1):
                errors.extend([company_id1, ", ", postal_code1, error_cargo_unit_companies_priority])

            if cargo_unit2 > int(truck_capacity_c2):
                errors.extend([company_id2, ", ", postal_code2, error_cargo_unit_companies_priority])

        return errors

    # if three companies
    elif int(num_comp_val) == 3:

        truck_capacity_c1 = truck_capacity_dict['truck_capacity_c1']
        truck_capacity_c2 = truck_capacity_dict['truck_capacity_c2']
        truck_capacity_c3 = truck_capacity_dict['truck_capacity_c3']

        # separate each company
        company1 = postal_sequence_company[0]
        company2 = postal_sequence_company[1]
        company3 = postal_sequence_company[2]

        # Iterate each cargo unit
        # check if there is more than minimum value of cargo unit
        for company_grp_1, company_grp_2, company_grp_3 in itertools.izip(company1, company2, company3):

            # iterate for company 1
            postal_code1 = company_grp_1[0]
            cargo_unit1 = int(company_grp_1[2])
            company_id1 = company_grp_1[3]

            # iterate for company 2
            postal_code2 = company_grp_2[0]
            cargo_unit2 = int(company_grp_2[2])
            company_id2 = company_grp_2[3]

            # iterate for company 3
            postal_code3 = company_grp_2[0]
            cargo_unit3 = int(company_grp_2[2])
            company_id3 = company_grp_2[3]

            # if there is more the minimum value throw an error:
            if cargo_unit1 > int(truck_capacity_c1):
                errors.extend([company_id1, " ", postal_code1, error_cargo_unit_companies_priority])

            if cargo_unit2 > int(truck_capacity_c2):
                errors.extend([company_id2, " ", postal_code2, error_cargo_unit_companies_priority])

            if cargo_unit3 > int(truck_capacity_c3):
                errors.extend([company_id3, " ", postal_code3, error_cargo_unit_companies_priority])

        return errors

    # if three companies
    elif int(num_comp_val) == 4:

        truck_capacity_c1 = truck_capacity_dict['truck_capacity_c1']
        truck_capacity_c2 = truck_capacity_dict['truck_capacity_c2']
        truck_capacity_c3 = truck_capacity_dict['truck_capacity_c3']
        truck_capacity_c4 = truck_capacity_dict['truck_capacity_c4']

        # separate each company
        company1 = postal_sequence_company[0]
        company2 = postal_sequence_company[1]
        company3 = postal_sequence_company[2]
        company4 = postal_sequence_company[3]

        # Iterate each cargo unit
        # check if there is more than minimum value of cargo unit
        for company_grp_1, company_grp_2, company_grp_3, company_grp_4 in itertools.izip(company1, company2, company3, company4):

            # iterate for company 1
            postal_code1 = company_grp_1[0]
            cargo_unit1 = int(company_grp_1[2])
            company_id1 = company_grp_1[3]

            # iterate for company 2
            postal_code2 = company_grp_2[0]
            cargo_unit2 = int(company_grp_2[2])
            company_id2 = company_grp_2[3]

            # iterate for company 3
            postal_code3 = company_grp_2[0]
            cargo_unit3 = int(company_grp_2[2])
            company_id3 = company_grp_2[3]

            # iterate for company 4
            postal_code4 = company_grp_2[0]
            cargo_unit4 = int(company_grp_2[2])
            company_id4 = company_grp_2[3]

            # if there is more the minimum value throw an error:
            if cargo_unit1 > int(truck_capacity_c1):
                errors.extend([company_id1, " ", postal_code1, error_cargo_unit_companies_priority])

            if cargo_unit2 > int(truck_capacity_c2):
                errors.extend([company_id2, " ", postal_code2, error_cargo_unit_companies_priority])

            if cargo_unit3 > int(truck_capacity_c3):
                errors.extend([company_id3, " ", postal_code3, error_cargo_unit_companies_priority])

            if cargo_unit4 > int(truck_capacity_c4):
                errors.extend([company_id4, " ", postal_code4, error_cargo_unit_companies_priority])

        return errors

    # if three companies
    elif int(num_comp_val) == 5:

        truck_capacity_c1 = truck_capacity_dict['truck_capacity_c1']
        truck_capacity_c2 = truck_capacity_dict['truck_capacity_c2']
        truck_capacity_c3 = truck_capacity_dict['truck_capacity_c3']
        truck_capacity_c4 = truck_capacity_dict['truck_capacity_c4']
        truck_capacity_c5 = truck_capacity_dict['truck_capacity_c5']

        # separate each company
        company1 = postal_sequence_company[0]
        company2 = postal_sequence_company[1]
        company3 = postal_sequence_company[2]
        company4 = postal_sequence_company[3]
        company5 = postal_sequence_company[4]

        # Iterate each cargo unit
        # check if there is more than minimum value of cargo unit
        for company_grp_1, company_grp_2, company_grp_3, company_grp_4, company_grp_5 in itertools.izip(company1, company2, company3, company4, company5):

            # iterate for company 1
            postal_code1 = company_grp_1[0]
            cargo_unit1 = int(company_grp_1[2])
            company_id1 = company_grp_1[3]

            # iterate for company 2
            postal_code2 = company_grp_2[0]
            cargo_unit2 = int(company_grp_2[2])
            company_id2 = company_grp_2[3]

            # iterate for company 3
            postal_code3 = company_grp_2[0]
            cargo_unit3 = int(company_grp_2[2])
            company_id3 = company_grp_2[3]

            # iterate for company 4
            postal_code4 = company_grp_2[0]
            cargo_unit4 = int(company_grp_2[2])
            company_id4 = company_grp_2[3]

            # iterate for company 5
            postal_code5 = company_grp_2[0]
            cargo_unit5 = int(company_grp_2[2])
            company_id5 = company_grp_2[3]

            # if there is more the minimum value throw an error:
            if cargo_unit1 > int(truck_capacity_c1):
                errors.extend([company_id1, " ", postal_code1, error_cargo_unit_companies_priority])

            if cargo_unit2 > int(truck_capacity_c2):
                errors.extend([company_id2, " ", postal_code2, error_cargo_unit_companies_priority])

            if cargo_unit3 > int(truck_capacity_c3):
                errors.extend([company_id3, " ", postal_code3, error_cargo_unit_companies_priority])

            if cargo_unit4 > int(truck_capacity_c4):
                errors.extend([company_id4, " ", postal_code4, error_cargo_unit_companies_priority])

            if cargo_unit5 > int(truck_capacity_c5):
                errors.extend([company_id5, " ", postal_code5, error_cargo_unit_companies_priority])

        return errors
    # else:
    #
    #
    #     return True


# def minimum_truck_checker_comp(num_comp_val, propose_result_company, starting_postal_list,
#                                                                            num_of_truck_c1, num_of_truck_cc1,
#                                                                            num_of_truck_c2, num_of_truck_cc21,
#                                                                            num_of_truck_c3, num_of_truck_cc31,
#                                                                            type_of_truck_c2,type_of_truck_cc1,type_of_truck_cc21,
#                                                                            type_of_truck_c1,
#                                                                            type_of_truck_c3,
#                                                                            add_truck_cc1, add_truck_cc2,add_truck_cc3):
#
#     # add_truck_dict = {
#                     #     "add_truck_cc1": add_truck_cc1,
#                     #     "add_truck_cc2": add_truck_cc2,
#                     #     "add_truck_cc3": add_truck_cc3,
#                     # }
#                     #
#                     # num_of_truck_dict = {
#                     #
#                     #     "num_of_truck_c1": num_of_truck_c1,
#                     #     "num_of_truck_cc1": num_of_truck_cc1,
#                     #     "num_of_truck_cc2": num_of_truck_cc2,
#                     #     "num_of_truck_cc3": num_of_truck_cc3,
#                     #
#                     #     "num_of_truck_c2": num_of_truck_c2,
#                     #     "num_of_truck_cc21": num_of_truck_cc21,
#                     #     "num_of_truck_cc22": num_of_truck_cc22,
#                     #     "num_of_truck_cc23": num_of_truck_cc23,
#                     #
#                     #     "num_of_truck_c3": num_of_truck_c3,
#                     #     "num_of_truck_cc31": num_of_truck_cc31,
#                     #     "num_of_truck_cc32": num_of_truck_cc32,
#                     #     "num_of_truck_cc33": num_of_truck_cc33,
#                     #
#                     # }
#
#                     # type_of_truck_dict = {
#                     #     "type_of_truck_cc1": type_of_truck_cc1,
#                     #     "type_of_truck_cc2": type_of_truck_cc2,
#                     #     "type_of_truck_cc3": type_of_truck_cc3,
#                     # }
#
#     if int(num_comp_val) == 2:
#
#         # type_of_truck_cc1 = type_of_truck_dict['type_of_truck_cc1']
#         #
#         # num_of_truck_c1 = num_of_truck_dict['num_of_truck_c1']
#         # num_of_truck_cc1 = num_of_truck_dict['num_of_truck_cc1']
#         # num_of_truck_c2 = num_of_truck_dict['num_of_truck_c2']
#
#         company_1 = int(len(propose_result_company[0]))
#         company_2 = int(len(propose_result_company[1]))
#
#         # HQ
#         hq_comp_1 = starting_postal_list[0]
#         hq_comp_2 = starting_postal_list[1]
#
#         if add_truck_cc1 == "true" and not add_truck_cc2 == "true":
#
#             if company_1 > int(num_of_truck_cc1) + int(num_of_truck_c1):
#                 errors.extend([error_Num_of_truck, type_of_truck_cc1, " : ", company_1, "<br />"])
#
#         if add_truck_cc1 == "true" and add_truck_cc2 == "true":
#
#             if company_1 > int(num_of_truck_cc1) + int(num_of_truck_c1):
#                 errors.extend([error_Num_of_truck, " for ", hq_comp_1, ", Type Truck: ", type_of_truck_cc1, " is ", company_1, "<br />"])
#
#             if company_2 > int(num_of_truck_cc21) + int(num_of_truck_c2):
#                 errors.extend([error_Num_of_truck, " for ", hq_comp_2, ", Type Truck: ", type_of_truck_cc21, " is ", company_2, "<br />"])
#
#         if not add_truck_cc1 == "true" and not add_truck_cc2 == "true":
#
#             if company_1 > int(num_of_truck_c1):
#                 errors.extend([error_Num_of_truck, " for ", hq_comp_1, ", Type Truck: ", type_of_truck_c1, " is ", company_1, "<br />"])
#
#             if company_2 > int(num_of_truck_c2):
#                     errors.extend([error_Num_of_truck, " for ", hq_comp_2, ", Type Truck: ", type_of_truck_c2, " is ", company_2, "<br />"])
#
#         return errors
#
#     if int(num_comp_val) == 3:
#
#         company_1 = int(len(propose_result_company[0]))
#         company_2 = int(len(propose_result_company[1]))
#         company_3 = int(len(propose_result_company[2]))
#
#         # HQ
#         hq_comp_1 = starting_postal_list[0]
#         hq_comp_2 = starting_postal_list[1]
#         hq_comp_3 = starting_postal_list[2]
#
#         if add_truck_cc1 == "true" and not add_truck_cc2 == "true":
#
#             if company_1 > int(num_of_truck_cc1) + int(num_of_truck_c1):
#                 errors.extend([error_Num_of_truck,
#                      type_of_truck_cc1, " : ", company_1, "<br />"])
#
#         if add_truck_cc1 == "true" and add_truck_cc2 == "true" and not add_truck_cc3 == "true":
#
#             if company_1 > int(num_of_truck_cc1) + int(num_of_truck_c1):
#                 errors.extend([error_Num_of_truck, " for ", hq_comp_1, ", Type Truck: ", type_of_truck_cc1, " is ", company_1, "<br />"])
#
#             if company_2 > int(num_of_truck_cc21) + int(num_of_truck_c2):
#                 errors.extend([error_Num_of_truck, " for ", hq_comp_2, ", Type Truck: ", type_of_truck_cc21, " is ", company_2, "<br />"])
#
#             if company_3 > int(num_of_truck_cc31) + int(num_of_truck_c2):
#                 errors.extend([error_Num_of_truck, " for ", hq_comp_3, ", Type Truck: ", num_of_truck_cc31, " is ", company_3, "<br />"])
#
#         if not add_truck_cc1 == "true" and not add_truck_cc2 == "true" and not add_truck_cc3 == "true":
#
#             if company_1 > int(num_of_truck_c1):
#                 errors.extend([error_Num_of_truck, " for ", hq_comp_1, ", Type Truck: ", type_of_truck_c1, " is ", company_1, "<br />"])
#
#             if company_2 > int(num_of_truck_c2):
#                 errors.extend([error_Num_of_truck, " for ", hq_comp_2, ", Type Truck: ", type_of_truck_c2, " is ", company_2, "<br />"])
#
#             if company_3 > int(num_of_truck_c3):
#                 errors.extend([error_Num_of_truck, " for ", hq_comp_3, ", Type Truck: ", type_of_truck_c3, " is ", company_3, "<br />"])
#
#         return errors