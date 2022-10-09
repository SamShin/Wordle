import random 
from tkinter import *
import tkinter.font as font
from math import *
import linecache
import time

print("THIS IS WORDLEOBJ")

dict_name = "words.txt"
possible_word_name = "dict.txt"
column_count = 0
row_count = 0
word = []
position = [0,0] #[Column, Row]

word_dict = {} #Choose a new word from the file for the player to guess
possible_word_dict = {} #The guessable words

#The program chooses a word for word_dict
#The player can guess any words in possible_word_dict


with open(dict_name) as f: 
    for i, line in enumerate(f):
        word_dict[i] = line.strip()

with open(possible_word_name) as d:
    for i, line in enumerate(d):
        possible_word_dict[i] = line.strip()




def get_pos(): #Get the position between (0-29) of the current square selected
    return position[0] + position[1] * 5        

  

def get_word(): #Get word guessed in the row in game
    current_word = ""
    pos = (position[1]) * 5

    for i in range(5):
        current_letter = board_dict[pos+i][1].cget("text")
        current_word += current_letter
        
    return current_word


     
def choose_word(): #Choose a word to guess from the word_dict
    word.clear()
    spot = random.randint(0, len(word_dict))
    word.append(word_dict[spot])
    print(word) 
    
 
   
def check_word(): #Check if the word guessed is a possible word in the possible_word_dict
    print(get_word().lower()) #Prints the current word 
    if get_word().lower() in possible_word_dict.values():
        return True
    else:
        return False



def check_color():
    
    pos = (position[1]-1) * 5   
    
    for i in range(5):
  
        letter = board_dict[i][1].cget("text").lower()
            
        if letter == word[0][i]:
            for j in range(2):
                board_dict[pos + i][j].configure(bg='#218f47') 
        elif letter in word[0]:
            for j in range(2):
                board_dict[pos + i][j].configure(bg='#b59f3b')  
        elif letter.isalpha():
            for j in range(2):
                board_dict[pos + i][j].configure(bg='#3a3a3c')  
        else:
            for j in range(2):
                board_dict[pos + i][j].configure(bg='#121213')            

    root.update()
    
    

def key_pressed(event):
    letter = event.char
    if (letter.isalpha() and position[0] <5):
        letter = letter.upper()
        
        board_dict[get_pos()][1].configure(text=letter, font=letter_font, fg='#ffffff')

        position[0] += 1
        
        
        
def back_space(event):
    
    if(position[0] > 0):
        board_dict[get_pos()-1][1].configure(text= " ")
        position[0] -= 1 



def return_key(event):
    
    if((position[0] == 5) and position[1] < 6) and check_word():
        position[0] = 0
        position[1] += 1
        
        check_color()
        check_win()
        
        if (get_pos() == 30):
            end_game()  
    


def check_win():
    pos = (position[1]-1) * 5
    
    if(all(board_dict[pos + k][0].cget("bg") == "#218f47" for k in range(5))):
        end_game()  



def clear_board():   
    for i in range(30):
        board_dict[i][1].configure(text = " ")
    
    check_color() 
    
    for i in range(2):
        position[i] = 0
        
    



def end_game():
    time.sleep(1.5)
    choose_word()
    clear_board() 
    
 
    
      
choose_word()


#TKINTER GUI
#=================================================================================================
BLOCKPAD = 3
BLOCKSIZE = 61
  
board = [["" for i in range(5)] for j in range(6)]


root = Tk()
root.title("Wordle")
#TODO At a later point, accept a color mode | Light and Dark
root.geometry("500x700")
root['background'] = '#121213'
#root.attributes('-alpha',0.5)

font_name = "Helvetica Neue"   

title_font = font.Font(family=font_name, size=29, weight="bold")
letter_font = font.Font(family=font_name, size=20, weight="bold",)


title_label = Label(root, text="WORDLE", font=title_font, bg= '#121213', fg= '#ffffff')
title_label.grid(column=0,row=0, padx=160)

#Creates the white line under the word "Wordle"
line = Canvas(root, width=495, height=1, bg='#121213')
line.grid(column=0,row=1)   

board_frame = LabelFrame(root, bg= '#121213', borderwidth=0) #TODO Add background 
board_frame.grid(column=0,row=2, columnspan=10, pady= 110) #TODO Add padx pady



#board_dict[i] => [LabelFrame, Label]
board_dict = {}
keys = range(30)

for i in keys:
    c = i % 5
    r = floor(i / 5)
    
    board_dict[i] = []
    board_dict[i].append(LabelFrame(board_frame, width=BLOCKSIZE, height=BLOCKSIZE, highlightthickness=0, bg= '#121213'))
    board_dict[i][0].grid(column=c, row=r, padx=BLOCKPAD, pady=BLOCKPAD)
    board_dict[i][0].grid_propagate(0)
    
    board_dict[i].append(Label(board_dict[i][0], bg='#121213', text=" "))
    board_dict[i][1].place(x=BLOCKSIZE/2, y=BLOCKSIZE/2, anchor=CENTER)  


root.bind('<Key>' , key_pressed)
root.bind('<Return>', return_key)
root.bind('<BackSpace>', back_space) 

def check_new_color():
    
    pos = (position[1]-1) * 5  
    for k in range(5):
         
        for j in range(5):
            letter = board_dict[pos+j][1].cget("text").lower()
                
            if letter == word[0][j]:
                for k in range(2):
                    board_dict[pos+j][k].configure(bg='#218f47') 
            elif letter in word[0]:
                for k in range(2):
                    board_dict[pos+j][k].configure(bg='#b59f3b')  
            elif letter.isalpha():
                for k in range(2):
                    board_dict[pos+j][k].configure(bg='#3a3a3c')  
            else:
                for k in range(2):
                    board_dict[pos+j][k].configure(bg='#121213') 
                              

        root.update()   

if __name__ == "__main__":
    root.mainloop()
    


#Make this dynamic so you can choose any size you want 
#TODO As you keep guessing and gets to 2nd or later guesses, the yellow possible letters do not
#Take into account of the letters already guessed and used letters, 
#Player might think there are double letters when in reality, the correctly guessed letter might be the only
#Letter in the word, FIX THAT 



#TODO pos function sometimes doesn't work as sometimes I have to do pos[0]-1 and sometimes pos[0]
#Fix this 


#TODO 03/01/2022 The GUI interface for the color check is broken 