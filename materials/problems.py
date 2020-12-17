import re

def problems_list_zip(start_list):
    #this function converts sorted list of problems into zip one using "-"
    #example: from ["1.1","1.2","1.3","1.5","1.6","1.7","2.1","2.2"]
    #         to   ["1.1-3,5-7","2.1,2"]

    #this function is divide in two parts. First zip all ranges and second join problems with same "id"
    #example for the first part:
    #from ["1.1","1.2","1.3","1.5","1.6","1.7","2.1","2.2"]
    #to   ["1.1-3","1.5-7","2.1,2"]

    #example for the second part:
    #from ["1.1-3","1.5-7","2.1,2"]
    #to   ["1.1-3,5-7","2.1,2"]
    if start_list == []:
        return []

    middle_list = []
    if not (re.match("^((\d+\.)*)(\d+)$",start_list[0])):
        raise TypeError("Wrong problems format")#maybe here should be specification exactly what problem have wrong format
        
    reg_exp = re.search("^((\d+\.)*)(\d+)$",start_list[0])
    range_id, first_num = reg_exp.group(1), int(reg_exp.group(3)) #if element="1.2.3.4", range_id ="1.2.3." and first_num=4
    prev_num = first_num
    count = 1 #quantity of problems in range
    
    for element in start_list[1:]:
        if not (re.match("^((\d+\.)*)(\d+)$",element)):
            raise TypeError("Wrong problems format")#maybe here should be specification exactly what problem have wrong format
        
        reg_exp = re.search("^((\d+\.)*)(\d+)$",element)
        element_id, element_num = reg_exp.group(1), int(reg_exp.group(3))
        if (element_id != range_id) or (prev_num + 1 != element_num): #range ended
            if count > 2:
                middle_list.append(f"{range_id}{first_num}-{prev_num}")
            elif count == 2: middle_list.append(f"{range_id}{first_num},{prev_num}")
            else:middle_list.append(f"{range_id}{first_num}")
                
            range_id, first_num = element_id, element_num
            prev_num = first_num
            count = 1 
        else:
            prev_num += 1
            count += 1
    if count > 2:
        middle_list.append(f"{range_id}{first_num}-{prev_num}")
    elif count == 2: middle_list.append(f"{range_id}{first_num},{prev_num}")
    else:middle_list.append(f"{range_id}{first_num}")


    #here second part begins
    final_list = []
    reg_exp = re.search("^((\d+\.)*)([\d,-]+)$",middle_list[0])
    section_id, num_string = reg_exp.group(1), reg_exp.group(3) #if element="1.2.3.4-10", section_id ="1.2.3.", num_string = "4-10"
    
    for element in middle_list[1:]:
        reg_exp = re.search("^((\d+\.)*)([\d,-]+)$",element)
        element_id, el_string = reg_exp.group(1), reg_exp.group(3)
        if (element_id != section_id): #range ended
            final_list.append(section_id + num_string)
                
            section_id, num_string = element_id, el_string
        else:
            num_string = num_string + "," + el_string
    final_list.append(section_id + num_string)


    
    return final_list