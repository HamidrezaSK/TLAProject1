# from Q2 import find_relevent_grammers,find_group
class outPutController:
    def __init__(self,sett,grammer,alphabet,starting_states):
        self.outputAddress = "output.txt"
        self.alphabet = alphabet
        self.states_count = len(sett)
        self.starting_states = []
        self.final_states = []
        self.states = []
        self.grammer = []
        self._state_generator(sett,starting_states)
        self._grammer_generator(grammer,sett)
        self._file_handler()
    def _state_generator(self,sett,starting_states):
        for i in range(len(starting_states)):
            starting_states[i] = starting_states[i][2:]
        for i in range(len(sett)):
            
            if('*' not in sett[i][0]):
                self.states.append('g'+str(i))
                for j in range(len(sett[i])):
                    flag = False
                    for j in starting_states:
                        if(j in sett[i]):
                            flag = True
                            break
                    if(flag):
                        self.starting_states.append('->g'+str(i))
                        break
                        
            else:
                self.final_states.append('*g'+str(i))
    def _grammer_generator(self,grammer,sett):
        for i in range(len(sett)):
            temp = sett[i][0]
            grams = self.find_relevent_grammers(grammer,temp)
            for gram in grams:
                gram = gram.split(',')
                source_index = self.find_group(gram[0],sett)
                sink_index = self.find_group(gram[2],sett)
                source_index = str(source_index)
                sink_index = str(sink_index)
                source = 'g'+source_index
                sink = 'g'+sink_index
                if("*"+source in self.final_states):
                    source = '*'+source
                if("*"+sink in self.final_states):
                    sink = '*'+sink
                self.grammer.append(source+','+gram[1]+','+sink)
        for initstate in self.starting_states:
            temp = initstate[2:]
            for i in range(len(self.grammer)):
                if(self.grammer[i].find(temp) == 0):
                    self.grammer[i] = "->"+ self.grammer[i]
                    break

    def find_relevent_grammers(self,grammer,state):
        temp_grams=[]
        for gram in grammer:
            if(gram.find(state)==0):
                temp_grams.append(gram)
        return temp_grams

    def find_group(self,state,former_set):
        for i in range(len(former_set)):
            if(state in former_set[i]):
                return i
    def _file_handler(self):
        file = open(self.outputAddress,'w')
        file_content = [self.states_count,' '.join(self.alphabet)]+self.grammer
        file_content[0] = str(file_content[0])
        file_content[1] = str(file_content[1])
        for i in range(len(file_content)):
            file_content[i] += '\n'
        file.writelines(file_content)
        file.close()