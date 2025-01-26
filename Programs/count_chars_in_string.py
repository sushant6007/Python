from collections import Counter

def find_duplicates(input_string):
    char_count = Counter(input_string)
    
    duplicates = {char: count for char, count in char_count.items() if count > 1}
    
    
    return duplicates

print(find_duplicates(input_string='input_string'))