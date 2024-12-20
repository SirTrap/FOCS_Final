import ast

class MachineConverter:
    def __init__(self, string):
        
        string = string.replace("'", "\"")
        self.diction = ast.literal_eval(string)  # Safely convert to a dictionary

        self.states = self.diction["states"]
        self.alphabet = self.diction["alphabet"]
        self.tape_alphabet = self.diction["tape_alphabet"]
        self.start = self.diction["start"]
        self.accept = self.diction["accept"]
        self.reject = self.diction["reject"]
        self.delta = self.diction["delta"]
        
    def convert2string(self,w,cs):
        states_dict = {}
        letters_dict = {}

        states_dict[self.start] = 1
        states_dict[self.accept] = 2
        states_dict[self.reject] = 3
        indexs = 4
        indexa = 1

        for state in self.states:
            if state not in states_dict:
                states_dict[state] = indexs
                print(state)
                indexs += 1
        
        ustates = ""
        for i in range(len(self.states)):
            ustates += "1"*(i+1)
            ustates += "0"
        ustates = ustates[:-1]

        for letter in self.alphabet:
            if letter not in letters_dict:
                letters_dict[letter] = indexa
                indexa += 1
        
        ualphabet = ""
        for i in range(len(self.alphabet)):
            ualphabet += "1"*(i+1)
            ualphabet += "0"
        ualphabet = ualphabet[:-1]

        for letter in self.tape_alphabet:
            if letter not in letters_dict:
                letters_dict[letter] = indexa
                indexa += 1
        
        utapealphabet = ualphabet + "0"
        for i in range(len(self.alphabet),len(self.tape_alphabet)):
            utapealphabet += "1"*(i+1)
            utapealphabet += "0"
        utapealphabet = utapealphabet[:-1]

        mod_delta = []
        for (starts, letter, ends, tletter, add) in self.delta:
            mod_delta.append((states_dict[starts], letters_dict[letter], states_dict[ends],letters_dict[tletter], 1 if add == 1 else 2))
        
        udelta = ""
        for (starts, letter, ends, tletter, add) in mod_delta:
            udelta += "1"*starts + "0" + "1"*letter + "0" + "1"*ends + "0" + "1"*tletter + "0" + "1"*add
            udelta += "00"
        udelta = udelta[:-2]

        ustring = ""
        for i in w:
            ustring += "1"*letters_dict[i]
            ustring += "0"
        ustring = ustring[:-1]

        ucs = states_dict[cs] * "1" + (len(self.states) - states_dict[cs]) * "0"

        return ucs + "0000" + ustates + "00" + ualphabet + "00" + utapealphabet + "000" + udelta + "000" + "1001100111" + "0000" + ustring

    def __repr__(self):
        return str(self.diction)


#M = {'states': [1, 2, 4, 6, 7, 777, 666], 'alphabet': ['a','b'], 'tape_alphabet': ['a','b','X','Y','_'], 'start': 1, 'accept': 777, 'reject': 666, 'delta': [(1, 'a', 2, 'X', 1), (1, '_', 777, '_', 1), (2, 'a', 2, 'a', 1), (2, 'Y', 2, 'Y', 1), (2, 'b', 4, 'Y', -1), (4, 'Y', 4, 'Y', -1), (4, 'a', 7, 'a', -1), (4, 'X', 6, 'X', 1),  (6, 'Y', 6, 'Y', 1), (6, '_', 777, '_', 1), (7, 'a', 7, 'a', -1), (7, 'X', 1, 'X', 1)]}
#w = aba
#cs = 1
M = input("Enter the Machine:")
w = input("Enter the String:")
cs = int(input("Enter the Starting State:"))




tm = MachineConverter(M)

# Print the parsed dictionary
print(tm.convert2string(w,cs))
