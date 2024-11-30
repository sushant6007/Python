#This code implements a simple Hangman game. The player attempts to guess a randomly chosen word by guessing one letter at a time. 
#Incorrect guesses reduce the player's lives, and each stage of the Hangman graphic is displayed as lives decrease. 
#The game ends either when the player correctly guesses the entire word or when they run out of lives.
import random
stages = ['''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', '''
  +---+
  |   |
      |
      |
      |
      |
=========
''']
word_list = ["test", "ganesh", "sushant"]
chosen_word = random.choice(word_list)
word_length = len(chosen_word)
end_of_game = False
lives = 6

print(f'Shhhh, the solution is {chosen_word}')

display = []

for _ in range(word_length):
    display += "_"



while not end_of_game:
    guess = input("Guess a letter :").lower()

    if guess in display:
        print(f'You have already guessed letter {guess}')

    for position in range(word_length):
        letter = chosen_word[position ]
        if letter == guess:
            display[position] = letter
    
    if guess not in chosen_word:
        print(f"You guessed {guess}, that's not in the word. You lose a life.")
        lives -= 1
        if lives == 0:
            end_of_game = True
            print("You lose.")

    print(f"{' '.join(display)}")

    if "_" not in display:
        end_of_game = True
        print("You Win")

    print(stages[lives])