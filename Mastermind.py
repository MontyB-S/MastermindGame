class Game:

    def __init__(self):
        self.code = None
        self.player = None
        self.guess = None
        self.game_over = False
        self.__input = open('inputexample1.txt', 'r')
        self.__output = open('outputexample1.txt', 'w')
        self.black = 0
        self.white = 0
        self.guess_count = 0
        
    def read_code_player(self):
        self.code = self.__input.readline().split(' ')[1:4]
#        self.code = ' '.join(self.code)
        self.player = self.__input.readline().split(' ')[1]
        self.player = self.player.strip('\n')
    
    def write_to_output(self, x):
        if x == 1:
            black_string = 'black ' * self.black
            white_string = 'white ' * self.white
            print(black_string)
            print(white_string)
            self.__output.write('Guess ' + str(self.guess_count) + ': ' + ('black ' * self.black) + ('white ' * self.white) + '\n')
            self.black = 0
            self.white = 0
        elif x == 3:
            self.__output.write('Guess ' + str(self.guess_count) + ': Ill-formed guess provided \n')
        elif x == 4:
            self.__output.write('You won in ' + str(self.guess_count) + ' guesses. Congratulations \n')


    def read_guess(self):
        self.guess = self.__input.readline().split(' ')[:]
        if len(self.guess) > 3:
            self.guess_count += 1
            self.write_to_output(3)
            self.guess = 'skip'
        else:
            self.guess[2] = self.guess[2].strip('\n')
            self.guess_count += 1
#        print(self.guess)
    
    def check_guess(self):
        if self.guess == 'skip':
            x = 0
        elif self.guess == self.code:
            self.game_over = True
            self.black = 3
            self.write_to_output(1)
            self.write_to_output(4)
        else:
            for i in range(3):
                if self.guess[i] == self.code[i]:
                    self.black += 1
                elif self.guess[i] in self.code:
                    self.white += 1
        self.write_to_output(1)
            
            

    
    def Initliase(self):
        self.read_code_player()
        while not self.game_over:
        #Put this inside a while loop that checks if game is over
            if self.player == 'human':
                self.read_guess()
                self.check_guess()



if __name__ == "__main__":
    x = Game()
    x.Initliase()