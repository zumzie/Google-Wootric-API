from collections import defaultdict
from copy import copy



def sum_avg(surveys, firm_ls, survey_ls, leng_ls):
    # a dictionary whose value defaults to a list
    data = defaultdict(list)
    temp_surveys = surveys.copy()
    firm_names = firm_ls
    survey_scores = survey_ls
    length_scores = leng_ls
    for i, row in enumerate(surveys['values']):
        # skip the header line and any empty rows
        # we take advantage of the first roww being indexed at 0
        # i=0 which evalutes as false, as does an empty row
        if not i or not row:
            continue

        # unpack the columns into local variables
        # index vaues -> id:0, score:1, text:2, email:3, response:4, csm:5, firm_id:6, firm_name:7, blank_:8, all_firm:9, firm_avg:10, firm_len:11
        id, score, text, email, response, csm, firm_id, firm_name, blank_, all_firm, firm_avg, firm_len = row
        
        # for each firm_id, add the score to the list
        data[firm_name].append(float(score))
        
    
        
    for firm_name, score in dict.items(data):
        new_n = firm_name
        sum_scores = sum(score)
        len_scores = len(score)
        avg_score = float(1)
        if sum_scores <= 0:
            if len_scores > 0:
                avg_score = sum_scores / int(len_scores)
                #print(firm_name, sum_scores / len_scores)
                firm_names.append(firm_name)
                survey_scores.append(avg_score)
                length_scores.append(len_scores)
                

        else:
           # print(firm_name, sum_scores / len_scores)
            avg_score = sum_scores / int(len_scores)
            firm_names.append(firm_name)
            survey_scores.append(avg_score)
            length_scores.append(len_scores)
            
    return temp_surveys, firm_names, survey_scores, length_scores
                #avg_score = sum_scores / int(len_scores)
               # print(firm_name, sum_scores / len_scores)

            # iterate through firm id and its list of scores and calculate average



#def struct_survey_data(body, scores):
    #pass
    










"""
   if sum_scores <= 0:
                if len_scores > 0:
                    row[9] = new_n
                    row[10] = sum_scores / len_scores
                    avg_score = sum_scores / int(len_scores)
                    print(firm_name, sum_scores / len_scores)

            else:
                row[9] = new_n
"""






"""
    for firm_name, avg_score in dict.items(prac):
         print(firm_name, avg_score)

    for j in range(len(prac)):
        for firm_name, score in dict.items(prac):
            if not i or not row:
                continue
            row[9] = firm_name
"""         
    



            

    






    
        
            






        
    




            




