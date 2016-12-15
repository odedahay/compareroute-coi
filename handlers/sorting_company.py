import sorting

def setLists_company(lists):

    # Create a dictionary of postal codes with values of order id
    # One postal code can have more than 1 order Id || 2 order
    postal_dictionary = {}

    # Postal list will contain all unique postal codes
    postal_list = []
    # capacity list will contain all capacity of postal codes
    capacity_list = []
    company_list = []

    # Create Order dictionary to store all the values that relate to the specific order
    order_dict = {}

    # Create Capacity dictionary to store all the values that relate to the specific order
    capacity_dic = {}
    company_dic = {}

    for i in range(0, len(lists)):

        order = lists[i]

        postal_list.append(order[0])
        capacity_list.append([order[0], int(order[2])])
        company_list.append([order[0], order[3]])

        if order[1] and order[2] not in postal_dictionary.keys():
            postal_dictionary[order[0]] = []

        postal_dictionary[order[0]].append(str(order[1]))
        postal_dictionary[order[0]].append(order[2])

        if order[0] not in order_dict.keys():
            order_dict[order[1]] = []

        for j in range(0, len(order)):
            order_dict[order[1]].append(str(order[j]))

        if order[0] and order[1] not in capacity_dic.keys():
            capacity_dic[order[2]] = []

        for k in range(0, len(order)):
            capacity_dic[order[2]].append(str(order[k]))
        # - - - - - - company - - - - - - #

        if order[0] and order[1] and order[2] not in company_dic.keys():
            company_dic[order[3]] = []

        for m in range(0, len(order)):
            company_dic[order[3]].append(str(order[m]))

    return postal_dictionary, postal_list, order_dict, capacity_dic, capacity_list, company_list


def setLists_company_cons(lists):

    # Create a dictionary of postal codes with values of order id
    # Postal list will contain all unique postal codes
    postal_list = []

    for i in range(0, len(lists)):

        order = lists[i]

        postal_list.append(order[0])

    return postal_list

