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



def unzip_problems(problems):
    result = []
    # Searches for sets like '1.3.2,3,4,5-7,9,13-17', '1.4.2' and so on
    list_of_sets = re.findall('(?:[0-9]+\.)+[0-9-,]*[0-9](?!\.)',problems)
    # Problems without dots
    if list_of_sets == []:
        list_of_sets = [problems]
    for problem_set in list_of_sets:
        unzipped_set = unzip_set(problem_set)
        result += unzipped_set
    return result

# Unzip string as '1.3.2,4-6,9' to be ['1.3.2', '1.3.4', '1.3.5', '1.3.6', '1.3.9']
def unzip_set(problem_set):
    # Check whether it is simple problem like '1.4.2'
    check = re.search('\.[0-9]+[,-]', problem_set)
    if check == None:
        return [problem_set]
    #If not then it finds base ('1.3') and main part ('2,4-6,9')
    index = check.start()
    base = problem_set[0:index]
    main = problem_set[index + 1:]
    
    #List of unzip main part
    sub_problems = []
    
    #Consequent part is '4-6' = 4,5,6 (without last number, it is included below in leftover)
    consequent = re.findall('[0-9]+-[0-9]+', main)
    for problems in consequent:
        start = int(problems.split('-')[0])
        end = int(problems.split('-')[1])
        for problem in range(start, end):
            sub_problems.append(problem)
    
    #Leftovers are all numbers that are in main part: '2,4,6,9'. They are added without repeatings to sub_problems
    leftover = re.findall('[0-9]+', main)
    for problem in leftover:
        if int(problem) not in sub_problems:
            sub_problems.append(int(problem))
    
    sub_problems.sort()
    
    unzipped_problems = []
    
    for number in sub_problems:
        unzipped_problems.append(f'{base}.{number}')
    
    return unzipped_problems