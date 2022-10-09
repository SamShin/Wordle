
from math import floor
from random import choice
from time import sleep
from tkinter import Canvas
from tkinter import Label
from tkinter import LabelFrame
from tkinter import font
from tkinter import Tk
from tkinter import CENTER

class Wordle(Tk):

    BLOCKPAD = 3
    BLOCKSIZE = 61
    font_name = "Helvetica Neue"


    def __init__(self, howManyWordsPerLine=5, howManyTries=6, fileName="bigdict.txt"):

        #Anything value bigger and the GUI will not fit in a 15.6in laptop screen
        if(howManyWordsPerLine > 20 or howManyTries > 10 or
           howManyWordsPerLine < 2 or howManyTries < 1):
            raise ValueError("First argument must be smaller than 21 and Second argument must be smaller than 10")

        super().__init__()

        self.HMWPL = howManyWordsPerLine #Stores what the length of the word is
        self.howManyTries = howManyTries #Stores how many guesses the player can make
        self.total = howManyWordsPerLine * howManyTries #Stores how many postions for letters there are in total
        self.word = "" #Stores the word to be guessed
        self.position = [0,0] #Stores the position of the current cursor, [column, row]
        self.word_dict = {} #Stores the possible words to be guessed
        self.board_dict = {} #Stores the tkinter objects

        self.title("Wordle")

        wSize = self.HMWPL * (Wordle.BLOCKSIZE + 2 * Wordle.BLOCKPAD)
        hSize = self.howManyTries * (Wordle.BLOCKSIZE + 2 * Wordle.BLOCKPAD) + 220

        if(wSize < 500):
            wSize = 500
        if(hSize < 700):
            hSize = 700

        geometry = str(wSize) + "x" + str(hSize)
        self.geometry(geometry)

        self.minsize(wSize, hSize)
        self.maxsize(wSize, hSize)
        self['background'] = '#121213'

        self.title_font = font.Font(family=Wordle.font_name, size=29, weight="bold")
        self.letter_font = font.Font(family=Wordle.font_name, size=20, weight="bold")

        self.title_label = Label(self, text="WORDLE", font=self.title_font, bg="#121213", fg="#ffffff")
        self.title_label.grid(column=0, row=0, padx=160)

        self.line = Canvas(self, width=(wSize-5), height=1, bg="#121213")
        self.line.grid(column=0, row=1)

        self.board_frame = LabelFrame(self, bg="#121213", borderwidth=0)
        self.board_frame.grid(column=0, row=2, columnspan=10, pady=110)

        #Building the board_dict, which is a dictionary of lists containing tkinter objects
        #(example): board_dict[i] = {i: [tkinter.LabelFrame, tkinter.Label]}
        #It is dynamically sized to fit the given word length and guess amount
        for i in range(self.total):

            c = i % self.HMWPL
            r = floor(i / self.HMWPL)

            self.board_dict[i] = []
            self.board_dict[i].append(LabelFrame(self.board_frame, width=Wordle.BLOCKSIZE, height=Wordle.BLOCKSIZE, highlightthickness=0, bg= "#121213"))
            self.board_dict[i][0].grid(column=c, row=r, padx=Wordle.BLOCKPAD, pady=Wordle.BLOCKPAD)
            self.board_dict[i][0].grid_propagate(0)

            self.board_dict[i].append(Label(self.board_dict[i][0], bg="#121213", text=" "))
            self.board_dict[i][1].place(x=Wordle.BLOCKSIZE/2, y=Wordle.BLOCKSIZE/2, anchor=CENTER)

        #Opens the given dictionary text file and adds all words that fit the given word length
        with open(fileName) as f:
            for i, line in enumerate(f):
                word = line.strip()
                if(len(word) == self.HMWPL):
                    self.word_dict[i] = word

        #Chooses a starting  word to start the game
        self._choose_word()

        #This binds the given keystrokes so that methods are called when these keys are pressed
        self.bind('<Key>', self._key_pressed)
        self.bind('<Return>', self._return_key)
        self.bind('<BackSpace>', self._back_space)



    #Action taken for when a key is pressed
    #If the key is alphabetical and the current row is not already filled with letters,
    #Advance the cursor forward by one and output the entered letter to GUI
    def _key_pressed(self, event):
        typed_letter = event.char
        if(typed_letter.isalpha() and self.position[0] < self.HMWPL):

            self.board_dict[self._get_pos()][1].configure(text=typed_letter.upper(), font=self.letter_font, fg="#ffffff")
            self.position[0] += 1



    #Action taken for when the enter key is pressed
    #If there are exactly as many letters entered as the possible word length and the player is not out of guesses and if the word is legal,
    #Update position and update color for the row
    def _return_key(self, event):
        if((self.position[0] == self.HMWPL) and self.position[1] < self.howManyTries) and self._check_word():
            self.position[0] = 0
            self.position[1] += 1

            self._check_color(((self.position[1]-1) * self.HMWPL), self.HMWPL)
            self._check_win()



    #Action taken for when the back space key is pressed
    #If the position is greater than 0,
    #Delete the letter at current cursor, move back cursor by one
    def _back_space(self, event):
        if(self.position[0] > 0):
            self.board_dict[self._get_pos()-1][1].configure(text=" ")
            self.position[0] -= 1



    #Helper method, Returns the current cursor position
    def _get_pos(self):
        return self.position[0] + self.position[1] * self.HMWPL



    #Helper method, Returns the current row
    #Phase greater than 0 gives the nth row back from the current
    def _get_row(self, phase):
        return (self.position[1] - phase) * self.HMWPL



    #Helper method, Returns the current word guessed in the most recent row
    def _get_word(self):
        current_word = ""
        current_row = self._get_row(0)
        for i in range(self.HMWPL):
            current_letter = self.board_dict[current_row+i][1].cget("text")
            current_word += current_letter

        return current_word



    #Choses a word for the player to guess
    def _choose_word(self):
        self.word = choice(list(self.word_dict.values()))



    #Checks wether the guessed word is a legal word
    #Returns <True is yes | False if no>
    def _check_word(self):
        if self._get_word().lower() in self.word_dict.values():
            return True
        return False



    #Checks if the game has ended, either by the player guessing the word correctly or out of possible position
    def _check_win(self):
        if(all(self.board_dict[self._get_row(1)+k][0].cget("bg") == "#218f47" for k in range(self.HMWPL))
           or self._get_pos() == self.total):

            sleep(1.5)
            self._choose_word()
            self._clear_board()



    #Helper method to reset the board
    def _clear_board(self):
        for i in range(self.total):
            self.board_dict[i][1].configure(text=" ")

        self._check_color(0, self.total)

        for i in range(2):
            self.position[i] = 0



    #Helper method to update the color of each position depending on the parameters given
    def _check_color(self, position, count):

        for i in range(count):
            letter = self.board_dict[position + i][1].cget("text").lower()

            if letter == self.word[i % self.HMWPL]:
                for j in range(2):
                    self.board_dict[position + i][j].configure(bg='#218f47')
            elif letter in self.word:
                for j in range(2):
                    self.board_dict[position + i][j].configure(bg='#b59f3b')
            elif letter.isalpha():
                for j in range(2):
                    self.board_dict[position + i][j].configure(bg='#3a3a3c')
            else:
                for j in range(2):
                    self.board_dict[position + i][j].configure(bg='#121213')

            #If the method was getting called to update a row, skip if it is called for board reset
            if(count == self.HMWPL):
                sleep(0.1)
                self.update()