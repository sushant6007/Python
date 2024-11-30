#This code implements a simple word-guessing game where a random word is selected from a predefined list. 
#The player guesses letters, and correctly guessed letters are revealed in their corresponding positions in the word, while the rest remain hidden.

word_list = ["test", "ganesh", "sushant"]

import random
chosen_word = random.choice(word_list)

print(f'Shhhh, the solution is {chosen_word}')

display = []

for _ in range(len(chosen_word)):
    display += "_"
print(display)

guess = input("Guess a letter :").lower()

for position in range(len(chosen_word)):
    letter = chosen_word[position ]
    if letter == guess:
        display[position] = letter

print(display)