'''
Functions to generate random texts on the basis of trigrams
TODO: many functions could (and should) be more efficient.
'''
import random


'''
reads a text and returns a string containing this text
'''
def read_text(filename):
    with open(filename) as f:
        text = f.read()
        f.close()
    return text


"""
Preprocesses a string of text.
Removes all undesired characters.
TODO: make more efficient
"""
def pre_process(inputText):
    processed = ""
    for char in inputText:
        if char.isalnum():                  #is character alphanumerical
            processed = processed + char
        elif char == " " or char == "\n":
            processed = processed + char
        elif char == "." or char == "," or char == "?" or char == "!" or char == "'" or char == "-" or char == ":" or char == ";" : #chars I like to keep despite they are not alphanumerical
            processed = processed + char

    processed = processed.replace('\t', ' ')
    return processed

'''
This function takes the (cleaned) input text
The function makes a dictionary from all the trigrams in the inputText
Trigrams are stored as follows
{ ( word1, word2) : {word3 : [number of occurances of word3 after the bigram word1, word2] }
'''
def build_dictionary(inputText):
    n_grams = {}

    inputWords = inputText.split()
    N_minus_one = ""        # <-- This variable is word2 (see description above)
    N_minus_two = ""        # <-- This variable is word1

    for words in inputWords:
        key = (N_minus_two, N_minus_one)
        if n_grams.get(key) == None:
            n_grams[key] = {words : 1 }
        else:
            if n_grams[key].get(words) == None:
                n_grams[key][words] = 1
            else:
                n_grams[key][words] += 1
        N_minus_two = N_minus_one           # <-- perform a shift to store the next trigram
        N_minus_one = words

    return n_grams

'''
This function selects a random bigram from all the bigrams so that the first word of the bigram starts with a capital.
It returns this 'random' bigram
the variable: n_grams, contains the n_gram model
'''
def get_random_start_bigram(n_grams):
    keylist = list(n_grams.keys())

    while True:
        random_number = random.randint(0, len(keylist) - 1)
        start_bigram = keylist[random_number]
        if len(start_bigram[0]) == 0:           # <-- some items in the dictionary are empty (""). This prevents the program from crashing
            continue
        if start_bigram[0][0] >= "A" and start_bigram[0][0] <= "Z":
            break

    return start_bigram

'''
This function gets the preceding bigram as context.
It selects a semi-random word that follows that bigram according to the dictionary.
The chance that a word is chosen is determined by the number of occurances in the text.
Strategie: create a list that contains every possible follow-up word. Every possible follow-up word is as many times in this list as it occurs in the inputText.
From this list a random position is selected. The word at this position is returned as the follow-up word.
Assumption: the more a word occurs in the list. The higher the chance that it will be randomly selected.
'''
def get_next_word (context, n_grams):

    possible_words = n_grams.get(context)

    possible_list = []      # <-- will contain all possible follow-up words as many times as they occur in the inputText
    for items in possible_words:
        i = 0
        while i < possible_words[items]:
            possible_list.append(items)
            i += 1

    random_int = random.randint(0, len(possible_list) - 1)      # <-- select a random position in the list
    next_word = possible_list[random_int]

    return next_word

'''
This function creates a line of text.
The line is initiated by a random chosen bigram.
Until the last character of the line is a period, exclamation mark or question mark, new words are being selected randomly.
The completed line is returned
'''
def generate_line (n_grams):
    start = get_random_start_bigram(n_grams)
    line = start[0] + " " + start[1] + " "

    while True:
        line_list = line.split()
        context = (line_list[-2], line_list[-1])        # <-- the last two words of the line are the context-bigram
        next_word = get_next_word (context, n_grams)
        if next_word[-1] == "." or next_word[-1] == "!" or next_word [-1] == "?":
            break

        line = line + next_word + " "

    line = line + next_word + '\n'

    return line


'''
This function takes as input the n-gram dictionary and the desired number of lines in the output.
The function generates a tekst of the desired length.
This text is returned
'''
def generate_text (n_grams, lines_in_output):
    i = 0
    text = ""
    while i < lines_in_output:
        line = generate_line (n_grams)
        text = text + line
        i += 1

    return text


'''
Generates a tweet.
takes as input:
- the ngram model (ngram_dict)
- hashtags that the tweed should have. Default is no hashtags:
- The maximum number of tries to get a proper tweet. Default is 10.000 tries
- The minimum length of a tweet in nr of characters. Default is 100
'''
def generate_tweet(ngram_dict ,hashtags = '', max_tries = 10000, min_length = 100):
    i = 0
    while True:
        line = generate_line(ngram_dict)
        line = line.replace('- ', '')
        line = line.strip()
        tweet = line + ' ' + hashtags
        if len(tweet) < 140 and len(tweet) > min_length:   # <-- if tweet satisfies conditions
            return tweet

        i+=1
        if i == max_tries:
            return None

