#PROGRAM 1: TRACING NTM BEHAVIOR

#HOW TO PROGRAM (E.G.)
# python traceTM_wsulli22.py check-equal_01s-wsulli22.csv

#REFERENCED SOURCES
#https://python-course.eu/applications-python/turing-machine.php                                               #FOR UNDERSTANDING TURING MACHINE CODE IMPLEMENTATION
#https://sandipanweb.wordpress.com/2020/08/08/simulating-a-turing-machine-with-python-and-executing-programs/  #FOR UNDERSTANDING TURING MACHINE CODE IMPLEMENTATION
#https://www.anthropic.com/news/claude-3-5-sonnet                                                              #FOR DEBUGGING CODE AND PYTHON SYNTAX REFERENCING
#https://www.geeksforgeeks.org/understanding-python-dataclasses                                                #FOR UNDERSTANDING DATACLASSES

#IMPORTS
import csv                                  #READING INPUT FILES
import sys                                  #READING INPUT FILES
from dataclasses import dataclass           #IMPORT DATACLASS FOR FUTURE USE

#STORE CURRENT CONFIGURATION OF MACHINE
@dataclass 
class CurrentConfiguration:
    left_side: str                #LEFT SIDE OF TAPE
    current_state: str            #CURRENT STATE OF TAPE
    head_char: str                #START CHARACTER OF TAPE
    right_side: str               #RIGHT SIDE OF TAPE

#LOAD TURING MACHINE
class TuringMachine:
    #LOAD INPUT FILE
    def load_in_input(self, filename):
        self.state_transitions = {}
        with open(filename, 'r') as input_file:
            csv_data = list(csv.reader(input_file))
            self.name = csv_data[0][0]                 #NAME OF MACHINE
            self.states = csv_data[1]                  #STATES OF MACHINE
            self.sigma = csv_data[2]                   #INPUT ALPHABET
            self.gamma = csv_data[3]                   #TAPE ALPHABET 
            self.start_state = csv_data[4][0]          #START STATE 
            self.accept_state = csv_data[5][0]         #ACCEPT STATE
            self.reject_state = csv_data[6][0]         #REJECT STATE
            
            #PARSE FILE
            for row in csv_data[7:]:                   #START AFTER HEADER LINES
                curr_state = row[0]                    #CURRENT STATE
                read_char = row[1]                     #READ CHARACTER
                next_state = row[2]                    #NEXT STATE
                current_char = row[3]                  #CURRENT CHARACTER
                direction = row[4]                     #TAPE DIRECTION
                
                #CREATE TRANSITION RULE TUPLE
                current_transition_rules = (curr_state, read_char)
                
                # INITIALIZE TRANSITION LIST IF DOESN'T EXIST
                if current_transition_rules not in self.state_transitions:
                    self.state_transitions[current_transition_rules] = []
                
                #ADD TRANSITIONS TO THE LIST
                self.state_transitions[current_transition_rules].append((next_state, current_char, direction))

    def __init__(self): self.number_transitions_count = 0  #ADDED AFTER I FINISHED BECAUSE NEEDED IT IN PRINTS LATER
    
    #RUN THE TURING MACHINE
    def run_turing_machine(self, input_string, max_depth):
        #IF NOT EMPTY, SET HEAD TO FIRST CHARACTER OF INPUT
        if (input_string):                             
            initial_head = input_string[0]
        else:                                       
            initial_head = "_"

        #IF 1+ CHAR, SET RIGHT TO REST OF INPUT
        if len(input_string) > 1:                     
            initial_right = input_string[1:]
        else:                                         
            initial_right = ""
            
        #INITIALIZE CURRENT STATE CONFIGURATION WITH INITIAL HEAD AND RIGHT SIDE
        initial_CurrentConfiguration = CurrentConfiguration(
            left_side="",
            current_state=self.start_state,
            head_char=initial_head,
            right_side=initial_right
        )
        
        #INITIALIZE CURRENT LEVEL AND TRANSITION COUNT
        current_level = [(initial_CurrentConfiguration, [initial_CurrentConfiguration])]   
        
        #LOOP THROUGH MAX DEPTH
        for depth in range(max_depth):
            next_level = []
            
            #LOOP THROUGH CURRENT LEVEL
            for config, current_path in current_level:
            
                #IF ACCEPT STATE IS REACHED
                if config.current_state == self.accept_state:
                    return True, depth, current_path 
                
                #GET POSSIBLE NEXT MOVES
                possible_moves = self.state_transitions.get((config.current_state, config.head_char), [])
                
                #COUNT TRANSITIONS
                if possible_moves:
                    self.number_transitions_count += len(possible_moves)   
                else: 
                    self.number_transitions_count += 1   

                #IF NO POSSIBLE MOVES, ADD REJECT STATE TO THE PATH
                if not possible_moves:next_level.append((CurrentConfiguration(config.left_side, self.reject_state, config.head_char, config.right_side), current_path + [config]))
                
                #LOOP THROUGH POSSIBLE MOVES
                for next_state, current_char, direction in possible_moves:
                    new_configuration = self.simulate_single_move_of_machine(config, next_state, current_char, direction)
                    next_level.append((new_configuration, current_path + [new_configuration]))
            
            #IF NO NEXT LEVEL, RETURN FALSE BECAUSE REJECT REACHED
            if not next_level: return False, depth, []
            
            #SET CURRENT LEVEL TO NEXT LEVEL BECAUSE ACCEPT REACHED
            current_level = next_level
            
            #CHECK IF ALL STATES ARE REJECTED BECAUSE REJECT REACHED
            all_rejected = True
            for config, _ in current_level:
                if config.current_state != self.reject_state:
                    all_rejected = False
                    break
            if all_rejected: return False, depth, []
                
        return None, max_depth, []
    
    #SIMULATE SINGLE MOVE OF TURING MACHINE
    def simulate_single_move_of_machine(self, configuration, next_state, current_char, direction):
        left = configuration.left_side
        right = configuration.right_side
        
        #IF DIRECTION IS RIGHT
        if direction == 'R':
            left = left + current_char
            head = right[0] if right else '_'
            right = right[1:] if right else ''

        #IF DIRECTION IS LEFT
        if direction == 'L':
            right = current_char + right
            head = left[-1] if left else '_'
            left = left[:-1] if left else ''
            
        #RETURN NEW CONFIGURATION
        return CurrentConfiguration(left, next_state, head, right)

def main():
    #LOAD INPUT FILE
    input_file  = sys.argv[1]
    turing_machine = TuringMachine()
    turing_machine.load_in_input(input_file)
    
    #GET INPUT STRING
    input_string = input("\nENTER INPUT STRING (CLICK ENTER FOR ϵ): ")
    max_depth = 200 
    
    #RUN TURING MACHINE
    accepted, depth, path = turing_machine.run_turing_machine(input_string, max_depth)
    
    #PRINT OUTPUT
    print("\n--------------------------------------------------\n")
    print(f"{'    MACHINE NAME:':<20} {turing_machine.name}")
    print(f"{'  INITIAL STRING:':<20} {'ε' if input_string == '' else input_string}")
    print(f"{'   DEPTH OF TREE:':<20} {depth}")
    print(f"{'TOTAL TRANSITION:':<20} {len(path) if path else 0}")
    print(f"{'          STATUS:':<20} {'ACCEPTED' if accepted else 'REJECTED'}")
    print(f"{'\n STEPS TO REJECT:':<20}  {depth}\n" if not accepted else "", end="")
    print(f"{'CONFIGS EXPLORED:':<20} {turing_machine.number_transitions_count}")

    print(f"{' AVG. NON-DETERM:':<20} {'N/A' if depth == 0 else f'{turing_machine.number_transitions_count / depth:.2f}'}")

    if accepted is None:
        print(f"Execution stopped after {max_depth} steps")
    elif accepted:
        print(f"\n STEPS TO ACCEPT:    {depth}")
        print("\n EXECUTION PATH: ", end="")
        for i, configuration in enumerate(path):
            if i == 0:
                print(f"    ({configuration.left_side}, {configuration.current_state}, {configuration.head_char}, {configuration.right_side})")
            else:
                print(f"                     ({configuration.left_side}, {configuration.current_state}, {configuration.head_char}, {configuration.right_side})")
    print("\n--------------------------------------------------")
    print()

#RUN MAIN FUNCTION
if __name__ == "__main__":
    main()