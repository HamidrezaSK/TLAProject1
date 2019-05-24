class fileController:
    def __init__(self,inputAddress):
        self.inputAddress = inputAddress
        self.alphabet = []
        self.states_count = 0
        self.starting_states = []
        self.final_states = []
        self.states = []
        self.grammer = []
        self._fileHandler()
    
    def _fileHandler(self):
        file = open(self.inputAddress,'r')
        lines = file.readlines()
        self.states_count = int(lines[0])
        self.grammer = lines[2:]
        lines[1] = lines[1].strip()
        self.alphabet = lines[1].split(',')
        self._stateHandler(self.grammer)
        self.states.sort()
        self._grammer_corrector()        
        return [self.states_count,self.alphabet,self.states,self.starting_states,self.final_states,self.grammer]

    def _stateHandler(self,unknown_grammer):
        for gram in unknown_grammer:
            gram = gram.strip()
            splited_gram = gram.split(',')
            temp = splited_gram[0]
            if("->" in temp):
                if(temp not in self.starting_states):
                    self.starting_states.append(temp)
            elif("*" in temp):
                if(temp not in self.final_states):
                    self.final_states.append(temp)
            else:
                if(temp not in self.states):
                    self.states.append(temp)
            temp = splited_gram[2]
            if("->" in temp):
                if(temp not in self.starting_states):
                    self.starting_states.append(temp)
                    temp = temp[2:]
                    if temp not in self.states:
                        self.states.append(temp)
            elif("*" in temp):
                if(temp not in self.final_states):
                    self.final_states.append(temp)
            else:
                if(temp not in self.states):
                    self.states.append(temp)

    def _grammer_corrector(self):
        self.grammer = [i.replace("->",'') for i in self.grammer]
        for i in range(len(self.grammer)):
            self.grammer[i] = self.grammer[i].strip()
        self.grammer.sort()
            
                

