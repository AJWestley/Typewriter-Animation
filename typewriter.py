from sys import argv
from time import sleep
from random import uniform, randint, choice
from letters import ALPHABET, KEYBOARD_NEIGHBOURS

def animate(
    text: str, *,
    delay: float = 0.1, 
    lengthen_space: float = 0.1, 
    temperature: float = 0,
    misspell_prob: float = 0
    ) -> None:
    '''
    Params
    ---------
    text: str
    The text to animate.
    
    delay: float
    The base delay between keystrokes.
    0.1 by default.
    
    lengthen_space: float 
    How much longer to make a space.
    0.1 by default.
    
    temperature: float 
    The level of variation in the keystroke delay.
    0 by default.
    
    misspell_prob: float 
    The probability of each word being misspelled.
    0 by default.
    '''
    
    # Fixing parameters if they aren't in the right ranges
    delay = max(0, delay)
    temperature = max(0, min(delay, temperature))
    lengthen_space = max(lengthen_space, -delay)
    misspell_prob = min(1, max(0, misspell_prob))
    space_delay = delay + lengthen_space
    
    text_list = text.split(' ')
    
    for word in text_list:
        if bernoulli_tf(misspell_prob) and len(word) > 1:
            misspell_word(word, delay, temperature)
        else:
            animate_word(word, delay, temperature)
        print(end=' ')
        fuzzy_delay(space_delay, temperature)

def animate_word(word: str, delay: float = 0.1, temperature: float = 0.05) -> None:
    for char in word:
        print(char, end='')
        fuzzy_delay(delay, temperature)

def misspell_word(word: str, delay: float = 0.1, temperature: float = 0.05) -> None:
    index = randint(0, len(word) - 2)
    for i in range(index):
        print(word[i], end='')
        fuzzy_delay(delay, temperature)
    if word[index] in KEYBOARD_NEIGHBOURS:
        print(choice(KEYBOARD_NEIGHBOURS[word[index]]), end='')
    else:
        print(choice(ALPHABET), end='')
    fuzzy_delay(delay, temperature)
    for i in range(index+1, len(word)):
        print(word[i], end='')
        fuzzy_delay(delay, temperature)
    for i in range(index, len(word)):
        print('\b', end=' \b')
        fuzzy_delay(delay, temperature)
    for i in range(index, len(word)):
        print(word[i], end='')
        fuzzy_delay(delay, temperature)

def fuzzy_delay(delay: float, temperature: float) -> None:
    sleep(delay + uniform(-temperature, temperature))

def bernoulli_tf(p: float):
    if uniform(0, 1) < p:
        return True
    return False

if __name__ == '__main__':
    text = 'Hello, how are you?' if len(argv) == 1 else argv[1]
    animate(text, delay=0.1, temperature=0.05, misspell_prob=0.2, lengthen_space=0.15)