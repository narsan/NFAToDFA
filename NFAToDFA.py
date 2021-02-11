# main
nfa_transition_functions = []
dfa_transition_functions = []
dfa_states = []
new_states = []
dfa_finalStates = []
num_dfa_final_states = 0
nfa_transition_dict = {}
dfa_transition_dict = {}
try:
    f = open("NFA_Input_2.txt", "r")
except FileNotFoundError:
    print("Wrong file or file path")

alphabet = str(f.readline()).split()
states = str(f.readline()).split()
tmp = str(f.readline()).split()
firstState = tmp[0]
dfa_states.append((firstState,))
finalStates = str(f.readline()).split()
line = f.readlines()
n = line.__len__()

for i in range(n):
    temp = str(line[i]).split()
    from_state = temp[0]
    with_alphabet = temp[1]
    to_state = temp[2]
    transition_function = (from_state, with_alphabet, to_state)
    nfa_transition_functions.append(transition_function)
f.close()

# until here we read inputs from file and store them in variables
# handling "landa" operator
for i in nfa_transition_functions:
    if i[1] == 'Î»':
        nfa_transition_functions.remove((i[0], i[1], i[2]))
        for a in alphabet:
            if (i[0], a, i[2]) not in nfa_transition_functions:
                nfa_transition_functions.append((i[0], a, i[2]))

# combine the states that have same transition

for transition in nfa_transition_functions:
    starting_state = transition[0]
    transition_symbol = transition[1]
    ending_state = transition[2]

    if (starting_state, transition_symbol) in nfa_transition_dict:
        nfa_transition_dict[(starting_state, transition_symbol)].append(ending_state)
    else:
        nfa_transition_dict[(starting_state, transition_symbol)] = [ending_state]

# creating dfa states which are our new states
for dfa_state in dfa_states:
    for symbol in alphabet:
        if len(dfa_state) == 2 and (dfa_state, symbol) in nfa_transition_dict:
            dfa_transition_dict[(dfa_state, symbol)] = nfa_transition_dict[(dfa_state, symbol)]

            if tuple(dfa_transition_dict[(dfa_state, symbol)]) not in dfa_states:
                dfa_states.append(tuple(dfa_transition_dict[(dfa_state, symbol)]))

        else:
            destinations = []
            final_destination = []

            for nfa_state in dfa_state:
                if (nfa_state, symbol) in nfa_transition_dict and nfa_transition_dict[
                    (nfa_state, symbol)] not in destinations:
                    destinations.append(nfa_transition_dict[(nfa_state, symbol)])

            if not destinations:
                final_destination.append(None)
            else:
                for destination in destinations:
                    for value in destination:
                        if value not in final_destination:
                            final_destination.append(value)

            dfa_transition_dict[(dfa_state, symbol)] = final_destination

            if tuple(final_destination) not in dfa_states:
                dfa_states.append(tuple(final_destination))

for key in dfa_transition_dict:
    dfa_transition_functions.append(
        ("q" + str(dfa_states.index(tuple(key[0]))), key[1],
         "q" + str(dfa_states.index(tuple(dfa_transition_dict[key])))))

for q_state in dfa_states:
    for nfa_accepting_state in finalStates:
        if nfa_accepting_state in q_state:
            dfa_finalStates.append("q" + str(dfa_states.index(q_state)))
            num_dfa_final_states += 1

for i in dfa_states:
    new_states.append("q" + str(dfa_states.index(i)))

# write on the output file
f1 = open("DFA_Output_2.txt", "w")
for a in alphabet:
    f1.write(a + " ")
f1.write("\n")

for a in new_states:
    f1.write(a + " ")

f1.write("\n")
f1.write(firstState)
f1.write("\n")

for a in dfa_finalStates:
    f1.write(a + " ")
f1.write("\n")

for a in dfa_transition_functions:
    f1.write(a[0] + " " + a[1] + " " + a[2] + "\n")
f1.close()
