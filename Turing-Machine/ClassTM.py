"""Class that contains the Turing Machine program

By Jan Nogué Gómez

Master in Quantum Science and Technology UB"""


class TuringMachine:
    def __init__(self, program, input_tape, N=4, state='q0'):
        """
        Preprocessing of the Input tape
        """
        self.iter = 0
        self.i_tape = input_tape
        bin_list = [bin(decimal)[2:] for decimal in self.i_tape]
        str_arr = [str(decimal) for decimal in bin_list]
        max_len = max(len(number) for number in str_arr)

        self.i_tape = 'S' + '_'.join(number.zfill(max_len) for number in str_arr) + 'E'
        """"""

        self.lenght = len(self.i_tape)-2
        self.trf = {}  #transition function
        self.state = state
        self.tape = ''.join(['_']*N)
        self.tape_lenght = ''.join(['_']*self.lenght)
        

        self.w_tape = f"S{self.tape_lenght}"
        self.t_tape = f"S{self.tape_lenght}E"
        self.o_tape = f"S{self.tape_lenght}H"
        self.head_i = N // 2 
        self.head_w = N // 2
        self.head_t = N // 2
        self.head_o = N // 2  
        
        self.i_tape = self.tape[:self.head_i] + self.i_tape + self.tape[self.head_i:]
        self.w_tape = self.tape[:self.head_w] + self.w_tape + self.tape[self.head_w:]
        self.t_tape = self.tape[:self.head_t] + self.t_tape + self.tape[self.head_t:]
        self.o_tape = self.tape[:self.head_o] + self.o_tape + self.tape[self.head_o:]


        for line in program.splitlines():
            q0, RI, WI, HI, RW, WW, HW, RT, WT, HT, RO, WO, HO, q1 = line.split(' ') 
            self.trf[q0, RI, RW, RT, RO] = (WI, HI, WW, HW, WT, HT, WO, HO, q1)

    def step(self):
        if (self.state != 'H'):
            #print(self.state)
            #print("entering step")
        # assert self.head >= 0 and self.head < len(self.tape) here
            RI = self.i_tape[self.head_i] # we set a to were the head is (we read)
            RW = self.w_tape[self.head_w]
            RT = self.t_tape[self.head_t]
            RO = self.o_tape[self.head_o]
            action = self.trf.get((self.state, RI, RW, RT, RO)) # from the transition function dictionari, we get the heads
            if action: # if there is a component (self.state, a) in the dictionari of transitions then:
                WI, HI, WW, HW, WT, _, WO, HO, q1 = action
                self.i_tape = self.i_tape[:self.head_i] + WI + self.i_tape[self.head_i+1:]
                self.w_tape = self.w_tape[:self.head_w] + WW + self.w_tape[self.head_w+1:]
                self.t_tape = self.t_tape[:self.head_t] + WT + self.t_tape[self.head_t+1:]
                self.o_tape = self.o_tape[:self.head_o] + WO + self.o_tape[self.head_o+1:]
                if HI != '*': # * means that the head does not move. 
                    self.head_i = self.head_i + (1 if HI == 'R' else -1)
                    self.head_t = self.head_i 

                if HW != '*': # * means that the head does not move. 
                    self.head_w = self.head_w + (1 if HW == 'R' else -1) # movem el head R o L depenent del valor de d
                
                if HO != '*': # * means that the head does not move. 
                    self.head_o = self.head_o + (1 if HO == 'R' else -1) # movem el head R o L depenent del valor de d
                self.state = q1 # we change the state

    def run(self, max_iter=999999999999999):
        while (self.state != 'H') and self.iter < max_iter: # prevent infinite loop
            self.step()
            self.iter += 1
        print(self.o_tape)
        return self.iter


    
    def initial_state(self):
        print(f"Initial Input Tape in binary: {self.i_tape}")
        return self.i_tape


    def print_solution(self):
    # Remove 'S' and 'E' from the string
        self.o_tape = self.o_tape[3:-2]
    # Split the string into a list of binary numbers
        self.o_tape = self.o_tape.split('_')
        self.o_tape = [int(binary, 2) for binary in self.o_tape if binary]
        print(f"Ouput Tape: {self.o_tape}")
        print(f"State: {self.state}, Iterations: {self.iter}")
        return self.iter

