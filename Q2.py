from fileController import fileController
from outPutController import outPutController
def minimization_handler(handler,new_set,former_set):
    # latter_set = []
    if(len(new_set)==1):
        return [new_set]
    elif(len(new_set)>1):
        chart = state_chart_creator(handler,new_set,former_set)
        groups = []
        for state in chart.keys():
            flag = False
            for i in range(len(groups)):
                if(chart[groups[i][0]] == chart[state]):
                    groups[i].append(state)
                    flag = True
                    break
            if(not flag):
                groups.append([state])
        return groups



def find_relevent_grammers(grammer,state):
    temp_grams=[]
    for gram in grammer:
        if(gram.find(state)==0):
            temp_grams.append(gram)
    return temp_grams

def state_chart_creator(handler,new_set,former_set):
    chart = {}
    for state in new_set:
        grammers = find_relevent_grammers(handler.grammer,state)
        chart_specifications = []
        for grammer in grammers:
            splited_grammer = grammer.split(',')
            chart_specifications.append(find_group(splited_grammer[2],former_set))
        chart[state] = tuple(chart_specifications)
    return chart

def find_group(state,former_set):
    for i in range(len(former_set)):
        if(state in former_set[i]):
            return i




handler = fileController("input.txt")
former_set = [handler.states,handler.final_states]
latter_set = []
while True:
    latter_set = []
    for new_set in former_set:
        latter_set+=minimization_handler(handler,new_set,former_set)
    if(len(latter_set) != len(former_set)):
        former_set = latter_set
    else:
        break
minimized_dfa = outPutController(latter_set,handler.grammer,handler.alphabet,handler.starting_states)

# print(minimized_dfa.states_count)
# print(minimized_dfa.alphabet)
# for i in minimized_dfa.grammer:
#     print(i)
