import sys

'''
TO DO:
    - DONE [check if all colours in guess are in the actual allowed colours]
    - DONE [make it so the program can overwrite the output file (doesn't need the file to be empty)]
    - DONE [check there are enough guesses to cover the game (6 guesses)]
    - DONE [make the code able to take codes that are not 3 long e.g. accept codes that are 4 colours]
    - DONE [make it so that it can be run from terminal]
    - DONE [if code contains colours not in the variable add them as allowed colours]
    - make the code work for codes longer than 3 for the black and white outputs 

'''

class Game:
    #Init variables for class, __ are private and should not be changed later 
    def __init__(self, input_file, output_file, code, no_of_guesses, colours):
        self.code = None
        self.player = None
        self.guess = None
        self.game_over = False
        self.__input = input_file
        self.open_input = open(input_file, 'r')
        self.__output = open(output_file, 'w')
        self.line_of_codes = code
        self.no_of_guesses = no_of_guesses
        self.black = 0
        self.white = 0
        self.guess_count = 0
        self.colours = colours
    
    #function that reads the winning code, and whether player is human or computer 
    def read_code_player(self):
        self.code = self.open_input.readline().split(' ')[1:]
        self.code = [i.rstrip('\n') for i in self.code if i.rstrip('\n')]
        print(self.code)
        #self.code = ' '.join(self.code)
        self.player = self.open_input.readline().split(' ')[1]
        self.player = self.player.strip('\n')
    
    #function to write to terminal based on the guess, different outputs based on input x
    def write_to_output(self, x):
        if x == 1:
            self.__output.write('Guess ' + str(self.guess_count) + ': ' + ('black ' * self.black) + ('white ' * self.white) + '\n')
            self.black = 0
            self.white = 0
        elif x == 2:
            self.__output.write('No or ill-formed code provided.')
        elif x == 3:
            self.__output.write('Guess ' + str(self.guess_count) + ': Ill-formed guess provided \n')
        elif x == 4:
            self.__output.write('You won in ' + str(self.guess_count) + ' guesses. Congratulations \n')
        elif x == 5:
            self.__output.write('The game was completed. Further lines were ignored. \n')
        elif x == 6:
            self.__output.write('You lost. Please try again. \n')
    
    def is_guess_in_colour(self): #if the colour isn't in availabe colours
        for colour in self.guess:
            if colour not in self.colours:
                return False
        return True

    #function to read guess from file and format correctly, also skipping turn if guess is not formatted correctly
    def read_guess(self):

        self.guess = self.open_input.readline().split(' ')[:]
        self.guess = [colour.rstrip('\n') for colour in self.guess if colour.rstrip('\n')] #this line strips \n from the elements and removes empty elements from array so it can processed
        print('guess', self.guess)
        if len(self.guess) != len(self.code):
            self.guess_count += 1
            self.write_to_output(3)
            self.guess = 'skip'
            print('3', self.guess_count)
        if not self.is_guess_in_colour() and self.guess != 'skip': #if guess not in avaialbe colours
            self.write_to_output(3)
            self.guess = 'skip'
        elif self.guess != 'skip':
            self.guess_count += 1
            print('else', self.guess_count)

    #function to check whether guess is same as code, and if not displays the relevant black and white counters. 
    def check_guess(self):
        if self.guess == 'skip':
            x = 0
        elif self.guess == self.code:
            self.game_over = True
            self.black = 3
            self.write_to_output(1)
            self.write_to_output(4)
        #need to rewrite the below
        else:
            most_common_element = max(set(self.guess), key = self.guess.count)
            if self.guess.count(self.guess[0]) == 3: #if the guess is all the same colour then check in the code how much of the colour appears and add it to the self.black variable
                self.black = self.black + self.code.count(self.guess[0])
            else:
                for i in range(len(self.code)): #change this from 3 to the length of the code
                    if self.guess[i] == self.code[i]:
                        self.black += 1
                    elif self.guess[i] == most_common_element:
                        if self.code.count(self.guess[i]) >= 1:
                            self.white += 1
                    elif self.guess[i] in self.code:
                        self.white += 1
            self.write_to_output(1)
    
    def add_colour_from_code(self):#this adds the colour from the code if not already in colours list
        for colour in self.code:
            if colour not in self.colours:
                self.colours.append(colour)



    #this function calls all other classes and runs the main game loop
    def Initliase(self):
        #below checks whether there is enough guesses in the file and if not calls the write function and exits the game loop
        with open(self.__input, 'r') as file:
            line_count = sum(1 for line in file if line.strip())
    
        self.read_code_player()
        self.add_colour_from_code()
        count = 0
        while not self.game_over and count < self.no_of_guesses:
            count += 1
            if self.player == 'human':
                self.read_guess()
                self.check_guess()

        if count >= self.no_of_guesses and not self.game_over: #if taken max guesses and not won print losing message
            self.game_over = True
            self.write_to_output(6)


        if (line_count-2) > count: #if the game is over and there is more guesses then output ignore message
            self.write_to_output(5)



if __name__ == "__main__":

    number_guess = 6
    colours = ['red', 'blue', 'yellow', 'green', 'orange']
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:    
        output_file = sys.argv[2]
    if len(sys.argv) > 3:
        code_line = sys.argv[3]
    if len(sys.argv) > 4:
        number_guess = int(sys.argv[4])
    if len(sys.argv) > 5:
        colours = sys.argv[5:]

    x = Game(input_file, output_file, code_line, number_guess, colours)
    x.Initliase()

'''


        if (line_count - 2) < self.no_of_guesses: #this function is not needed i think
            self.write_to_output(2)
            self.game_over = True
            return False

'''