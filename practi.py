from collections import defaultdict

def countLetters(word):
    counter = defaultdict(int)
    for letter in word:
        if letter == 'c':
            counter[letter] += 2
            continue
        counter[letter] += 1
    return counter

a = countLetters('abcbaabca')
print(a)