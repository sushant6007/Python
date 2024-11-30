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