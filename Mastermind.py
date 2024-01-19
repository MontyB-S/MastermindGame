import sys
import random

class Game:
    def __init__(self, input_file, output_file, code, no_of_guesses, colours):
        '''Init variables for class, __ are private and cannot not be changed during program'''
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
        self.code_line = code
    
    def read_code_player(self):
        '''function that reads the winning code, and whether player is human or computer'''
        self.code = self.open_input.readline().split(' ')[1:]
        self.code = [i.rstrip('\n') for i in self.code if i.rstrip('\n')]
        self.player = self.open_input.readline().split(' ')[1]
        self.player = self.player.strip('\n')
    
    def write_to_output(self, x):
        '''function to write to terminal based on the guess, different outputs based on input x'''
        #below stays as elif statements instead of match to support older versions of python
        if x == 1:
            self.__output.write('Guess ' + str(self.guess_count) + ': ' + ('black ' * self.black) + ('white ' * self.white) + '\n')
            self.black = 0
            self.white = 0
        elif x == 2:
            self.__output.write('No or ill-formed code provided.')
            sys.exit('No or ill-formed code provided.')
        elif x == 3:
            self.__output.write('Guess ' + str(self.guess_count) + ': Ill-formed guess provided \n')
        elif x == 4:
            self.__output.write('You won in ' + str(self.guess_count) + ' guesses. Congratulations! \n')
        elif x == 5:
            self.__output.write('The game was completed. Further lines were ignored. \n')
        elif x == 6:
            self.__output.write('You lost. Please try again. \n')
        elif x == 7:
            self.__output.write('No or ill-formed player provided. \n')
            sys.exit('No or ill-formed player provided.')
    
    def is_guess_in_colour(self): 
        '''checks if each colour in guess is in allowed list of colours'''
        for colour in self.guess:
            if colour not in self.colours:
                return False
        return True

    def read_guess(self):
        '''function to read guess from file and format correctly, also skipping turn if guess is not formatted correctly'''
        self.guess = self.open_input.readline().split(' ')[:]
        self.guess = [colour.rstrip('\n') for colour in self.guess if colour.rstrip('\n')] #this line strips \n from the elements and removes empty elements from array so it can processed

        if len(self.guess) != len(self.code):
            self.guess_count += 1
            self.write_to_output(3)
            self.guess = 'skip'

        if not self.is_guess_in_colour() and self.guess != 'skip': #if guess not in avaialbe colours
            self.write_to_output(3)
            self.guess = 'skip'
        elif self.guess != 'skip':
            self.guess_count += 1

    def find_most_common_elements(self):
        '''for each guess return the element(s) which occur the most'''
        most_common_element = []
        counts = {}
        for guess in self.guess:
            counts[guess] = counts.get(guess, 0) + 1
        
        for guess, count in counts.items():
            if count > 1:
                most_common_element.append(guess)
        return most_common_element
            
    def check_guess(self):
        '''function to check whether guess is same as code, and if not displays the relevant black and white counters. '''
        if self.guess == 'skip':
            x = 0
        elif self.guess == self.code:
            self.game_over = True
            self.black = len(self.code)
            self.write_to_output(1)
            self.write_to_output(4)
        else:
            most_common_element = self.find_most_common_elements()
            if self.guess.count(self.guess[0]) == len(self.code): #if the guess is all the same colour then check in the code how much of the colour appears and add it to the self.black variable
                self.black = self.black + self.code.count(self.guess[0])
            else:
                flag = False
                for i in range(len(self.code)): 
                    if self.guess[i] == self.code[i]:
                        self.black += 1
                    elif self.guess[i] in most_common_element and flag == False: 
                        if self.guess[i] in self.code: #covers case where same colour appears more than once in code
                            count = self.code.count(self.guess[i])
                            self.white += count - 1
                            flag = True
                    elif self.guess[i] in self.code:
                        self.white += 1
            self.write_to_output(1)

    def Initliase(self):
        '''this function calls all other classes and runs the main game loop'''
        #below checks whether there is enough guesses in the file and if not calls the write function and exits the game loop
        with open(self.__input, 'r') as file:
            line_count = sum(1 for line in file if line.strip())
        guesses_in_file = line_count - 2 #how many guesses contained in file
    
        self.read_code_player()
        count = 0

        if self.player == 'human':
            if (line_count - 2) < int(self.code_line):
                self.write_to_output(2)
                self.game_over = True
                sys.exit()
            while not self.game_over and count < self.no_of_guesses and count < guesses_in_file:
                count += 1
                self.read_guess()
                self.check_guess()

            if count >= guesses_in_file and not self.game_over: 
                self.game_over = True
                self.write_to_output(6)
            
            if count >= self.no_of_guesses and not self.game_over: #if taken max guesses and not won print losing message
                self.game_over = True
                self.write_to_output(6)

            if (line_count-2) > count: #if the game is over and there is more guesses then output ignore message
                self.write_to_output(5)
        elif self.player == 'computer':
            with open('ComputerGame.txt', 'w') as file:
                code_str = ' '.join(str(code) for code in self.code)
                file.write(f'code {code_str}\n')
                file.write('player human\n')
                count = 0
                while not self.game_over and count < self.no_of_guesses:
                    count += 1
                    self.comp_guess()
                    self.write_guess_to_file(file)
                    self.check_guess()
                if count >= self.no_of_guesses:
                    self.game_over = True
                    self.write_to_output(6)
        else:
            self.write_to_output(7)


    #below is the code for the computer
    def comp_guess(self):
        self.guess = []
        for _ in range(len(self.code)):
            self.guess.append(random.choice(self.colours))
        self.guess_count += 1

    def write_guess_to_file(self, file):
        guess_str = ' '.join(str(guess) for guess in self.guess)
        file.write(f'{guess_str}\n')


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
