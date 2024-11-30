#This code implements a word-guessing game where a player attempts to guess a randomly chosen word one letter at a time. 
#The game continues until the player correctly guesses all the letters in the word, revealing the complete word.
import random
word_list = ["test", "ganesh", "sushant"]
chosen_word = random.choice(word_list)
word_length = len(chosen_word)

print(f'Shhhh, the solution is {chosen_word}')

display = []

for _ in range(word_length):
    display += "_"

end_of_game = False

while not end_of_game:
    guess = input("Guess a letter :").lower()

    for position in range(word_length):
        letter = chosen_word[position ]
        if letter == guess:
            display[position] = letter

    print(display)

    if "_" not in display:
        end_of_game = True
        print("You Win")