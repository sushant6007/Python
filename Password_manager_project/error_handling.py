import pandas

data = pandas.read_csv("nato_phonetic_alphabet.csv")

phonetic_dict = {row.letter: row.code for (index, row) in data.iterrows()}
print(phonetic_dict)



def generate_phonetic():
    try:
        word = input("input letter: ").upper()
        output_dict = [phonetic_dict[letter] for letter in word]
    except KeyError:
        print("word should be valid value with alphabets only.")
        generate_phonetic()
    else:
        print(output_dict)
        
generate_phonetic()

