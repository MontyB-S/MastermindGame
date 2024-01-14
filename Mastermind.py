'''
TO DO:
    - DONE [check if all colours in guess are in the actual allowed colours]
    - make it so the program can overwrite the output file (doesn't need the file to be empty)
    - check there are enough guesses to cover the game (6 guesses)

'''



class Game:
    #Init variables for class, __ are private and should not be changed later 
    def __init__(self, available_colours = ['red', 'blue', 'yellow', 'green', 'orange']):
        self.code = None
        self.player = None
        self.guess = None
        self.game_over = False
        self.__input = open('inputexample3.txt', 'r')
        self.__output = open('outputexample3.txt', 'w')
        self.black = 0
        self.white = 0
        self.guess_count = 0
        self.colours = available_colours
    
    #function that reads the winning code, and whether player is human or computer 
    def read_code_player(self):
        self.code = self.__input.readline().split(' ')[1:4]
#        self.code = ' '.join(self.code)
        self.player = self.__input.readline().split(' ')[1]
        self.player = self.player.strip('\n')
    
    #function to write to terminal based on the guess, different outputs based on input x
    def write_to_output(self, x):
        if x == 1:
            print('being called')
            self.__output.write('Guess ' + str(self.guess_count) + ': ' + ('black ' * self.black) + ('white ' * self.white) + '\n')
            self.black = 0
            self.white = 0
        elif x == 2:
            self.__output.write('No or ill-formed code provided.')
        elif x == 3:
            self.__output.write('Guess ' + str(self.guess_count) + ': Ill-formed guess provided \n')
        elif x == 4:
            print('congrats')
            self.__output.write('You won in ' + str(self.guess_count) + ' guesses. Congratulations \n')
        elif x == 5:
            self.__output.write('The game was completed. Further lines were ignored.')
        elif x == 6:
            self.__output.write('You lost. Please try again.')
    
    def is_guess(self, guess):
        for colour in self.guess:
            if colour not in self.colours:
                return False
        return True

    #function to read guess from file and format correctly, also skipping turn if guess is not formatted correctly
    def read_guess(self):
        self.guess = self.__input.readline().split(' ')[:]
        #print(self.guess)
        self.guess = [colour.rstrip('\n') for colour in self.guess if colour.rstrip('\n')] #this line strips \n from the elements and removes empty elements from array so it can processed
        #print(self.guess)
        if len(self.guess) > 3:
            self.guess_count += 1
            self.write_to_output(3)
            self.guess = 'skip'
            #print(self.guess)
        if not self.is_guess(self.guess) and self.guess != 'skip':
            self.write_to_output(3)
            self.guess = 'skip'
        else:
            self.guess_count += 1


    
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
                for i in range(3):
                    if self.guess[i] == self.code[i]:
                        self.black += 1
                    elif self.guess[i] == most_common_element:
                        if self.code.count(self.guess[i]) >= 1:
                            self.white += 1
                    elif self.guess[i] in self.code:
                        self.white += 1
            self.write_to_output(1)



    #this function calls all other classes and runs the main game loop
    def Initliase(self):
        #below checks whether there is enough guesses in the file and if not calls the write function and exits the game loop
        with self.__input as file:
            line_count = sum(1 for line in file if line.strip())
        print('line count is:', line_count)
        if (line_count - 2) < 6:
            self.write_to_output(2)
            self.game_over = True
            return False
        

        self.read_code_player()
        count = 0
        while not self.game_over and count < 6:
            count += 1
        #Put this inside a while loop that checks if game is over
            if self.player == 'human':
                self.read_guess()
                self.check_guess()
            print(count)
        if count >= 6 and not self.game_over: #if taken 6 guesses and not won print losing message
            self.game_over = True
            self.write_to_output(6)

        print(line_count)
        if (line_count-2) > count: #if the game is over and there is more guesses then output ignore message
            self.write_to_output(5)



if __name__ == "__main__":
    x = Game()
    x.Initliase()
