#!/usr/bin/python3

EPS = '_'
START = 'x'
END = 'y'
fin = None
fout = None

def write(s):
    if fout:
        fout.write(s)
    else:
        print(s),
    
def str_set(s):
    x = list(s)
    if x:
        y = []
        res = '{'
        c = []
        for i in x:
            if i.isdigit():
                y.append(int(i))
            else:
                c.append(i)
        y.sort()
        if START in c:
            res += START.upper() + ', '
        for i in y:
            res += '%d' % i + ', '
        if END in c:
            res += END.upper() + '}'
        else:
            res = res[:-2] + '}'
        return res
    return '{}'
    
def eps_closure(nfa, node_set):
    if node_set == set([]):
        return node_set
    res = node_set.copy()
    for node in node_set:
        next_list = nfa.get(node)
        if next_list:
            for next in next_list:
                if next[1] == EPS:
                    res.add(next[0])
                    if next[0] != node:
                        res |= eps_closure(nfa, set([next[0]]))
    return res
    
def next_set(nfa, now_set, c):
    res = set([])
    for node in now_set:
        next_list = nfa.get(node)
        if next_list:
            for next in next_list:
                if next[1] == c:
                    res.add(next[0])
    return res
    
def main():
    nfa = {}
    lit = set([])
    
    for s in fin:
        e = s.lower().split()
        if nfa.get(e[0]):
            nfa[e[0]].append((e[1], e[2]))
        else:
            nfa[e[0]] = [(e[1], e[2])]
        lit.add(e[2])
    lit.remove(EPS)
    liter = list(lit)
    liter.sort()
    q = [eps_closure(nfa, set([START]))]
    status = [q[0]]
    dfa_str = ''
    dfa = {}
    end_node = []
    end_nodes = []
    mid_node = []
    while q:
        now = q.pop(0)
        i = status.index(now)
        now_index = '%d' % i
        end_str = ''
        if END in now:
            end_str = '*'
            end_node.append(i)
            end_nodes.append("q"+str(i))
        else:
            mid_node.append(i)
        # write(str_set(now) + ' ')
        dfa_str += end_str +"q"+ now_index + ' '
        # print(dfa_str)
        next_dict = {}
        for c in liter:
            next = eps_closure(nfa, next_set(nfa, now, c))
            if not next in status and next:
                q.append(next)
                status.append(next)
            j = status.index(next) if next else -1
            next_index = '%d' % j
            # write(str_set(next) + ' ')
            dfa_str += "q"+next_index + ' '
            next_dict[c] = j
        # write('\n')
        dfa_str += '\n'
        dfa[i] = next_dict
    # write('\ns %s\n%s\n' % (' '.join(liter), dfa_str))

    print(end_nodes)



    answer = str(len(status)) + "\n" + '%s\n%s\n' % (','.join(liter), dfa_str)
    # print(dfa_str.splitlines(),liter)

    listOfDfaStr = dfa_str.splitlines()

    for i in range(len(listOfDfaStr)):
        x = listOfDfaStr[i].split(" ")[:len(listOfDfaStr[i].split(" "))-1]
        listOfDfaStr[i] = x
    # print(listOfDfaStr)
    
    ToPrint = ""
    
    for i in range(len(listOfDfaStr)):
        source = listOfDfaStr[i][0]
        for j in range(len(listOfDfaStr[i])):
            if j != 0:
                if j != len(listOfDfaStr[i]) -1:
                    if source == listOfDfaStr[0][0]:
                        ToPrint +="->" + source + "," +liter[j-1] + ","  + listOfDfaStr[i][j] + "\n"
                    else:
                        ToPrint += source + "," +liter[j-1] + ","  + listOfDfaStr[i][j] + "\n"
                else:
                    ToPrint += source + "," +liter[j-1] + ","  + listOfDfaStr[i][j] + "\n"
    # print(ToPrint,ToPrint.find("q0"))

    for final in end_nodes:
        print(final)
        prevoius_final = 0
        while ToPrint.find(final,prevoius_final) != -1:
            border = ToPrint.find(final,prevoius_final)
            if ToPrint[border-1] != "*":
                ToPrint = ToPrint[:border] + "*" + ToPrint[border:]
                prevoius_final = border + 3
            else:
                prevoius_final = border + 3
    print(ToPrint)

    write(ToPrint)
            
    # print('s %s\n%s\n' % (' '.join(liter), dfa_str))
    # print(liter,dfa_str )
    q = [[end_node, True], [mid_node, True]]
    fresh = True
    while fresh:
        now = q[0]
        for c in liter:
            next = {}
            for i in now[0]:
                if dfa[i][c] == -1:
                    if next.get(-1):
                        next[-1].append(i)
                    else:
                        next[-1] = [i]
                else:
                    j = 0
                    for x in q:
                        if dfa[i][c] in x[0]:
                            if next.get(j):
                                next[j].append(i)
                            else:
                                next[j] = [i]
                        j += 1
            splited = True
            now_split = next.values()
            if now[0] in now_split:
                splited = False
            else:
                for x in now_split:
                    q.append([x, True])
                break
        q.pop(0)
        if not splited:
            q.append([now[0], False])
        fresh = False
        for x in q:
            if x[1] == True:
                fresh = True
                break
    split = [x for x, y in q]
    split.sort()
    # write(str(split).replace('[', '{').replace(']', '}') + '\n')
    for x in split:
        if len(x) > 1:
            rep = x[0]
            for i in range(1, len(x)):
                for j in dfa:
                    for c in liter:
                        if dfa[j][c] == x[i]:
                            dfa[j][c] = rep
                del dfa[x[i]]
    # write('\ns %s\n' % (' '.join(liter)))
    # for i in dfa:
    #     write('%d%s ' % (i, '*' if i in end_node else ''))
    #     for c in liter:
            # write('%d ' % dfa[i][c])
        # write('\n')
    fin.close()
    fout.close()

if __name__ == '__main__':
    import os

    input = open("input.txt",'r')
    output = open("nfa_0.txt","w")

    input_file = input.readlines()

    initial_state = None

    final_state = None

    for line in range(len(input_file)):
        if line >=2:
            rule = input_file[line].replace("\n", "").split(",")
            rule_to_write=''
            if "->" in rule[0]:
                initial_state = rule[0][2:]
                # print(initial_state)
            # elif "*" in rule[0]:
            #     final_state = rule[0][1:]
            #     print(final_state)

            for part in range(len(rule)):
                if "->" in rule[part]:
                    rule[part] = rule[part].replace("->",'')
                if "*" in rule[part]:
                    rule[part] = rule[part].replace("*",'')
                    final_state = rule[part]
                if initial_state != None and initial_state in rule[part]:
                    rule[part] = rule[part].replace(initial_state,"x")
                elif final_state != None and final_state in rule[part]:
                    rule[part] = rule[part].replace(final_state,'y')
                
            rule_to_write = " ".join([rule[0],rule[2],rule[1]])
            # print(rule_to_write,"asasas")
            rule_to_write += "\n"
            output.write(rule_to_write)
    output.close()
    
            




    now_dir = os.path.dirname(os.path.realpath(__file__))
    files = [x for x in os.listdir(now_dir) if os.path.isfile(x) and x.endswith('txt') and x.startswith('nfa_')]
    for x in files:
        fin = open(x, 'r')
        fout = open(x.replace('nfa_', 'dfa_'), 'w')
main()
