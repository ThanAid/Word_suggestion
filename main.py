import string
import os
import glob

# Creating an empty graph to "save" words as keys and the following words as values for example
# "Hi! My name is unknown.", in this case "My" is a word and "name" is the following one.
word_graph = {}


# Creating a function that will add keys, values and the weight of the values to the graph
# v1 is a vertices, v2 an edge and w the weight of that edge
def graph_add_node(v1, v2, w):
    # Check if v1 already exists
    if v1 in word_graph:
        # We add the v2 and the corresponding w in the already existing v1
        word_graph[v1].append(v2)
        word_graph[v1].append(w)
    else:
        # if v1 doesn't exist we add it and at the same time add v2 and w using a temporary dictionary
        temp_dict = {
            v1: [v2, w]
        }
        word_graph.update(temp_dict)


# Creating a function that will take a word as an argument and return the following word with
# the maximum likelihood
def graph_next_word(current_word):
    # Creating a list to store the weights of the corresponding vertices
    w_list = []
    for w in word_graph[current_word]:
        # Choosing only the integers so we choose the weights
        if isinstance(w, int):
            w_list.append(w)

    # find the max w
    max_w = max(w_list)

    # find the index of the max w and then subtract 1 to get the corresponding edge
    max_w_index = word_graph[current_word].index(max_w)

    # return the edge with the maximum weight
    return word_graph[current_word][max_w_index - 1]


# function to read the txt files and convert them to a list of words using the pre_process_txt function. returns a
# list containing all the words that are read in a form that can be used (lower case letters and no punctuations),
# also returns the number (int) of txt files read.
def read_txt():
    # Creating a variable to keep track of the number of text files the programme has read.
    txt_number = 0
    # Creating an empty list to add the separate lists of words from each txt.
    final_word_list = []

    for filename in glob.glob('*.txt'):
        txt_number += 1
        with open(os.path.join(os.getcwd(), filename), mode='r', encoding='utf-8') as f:
            text_string = f.read().lower()

        # Calling the pre-process function
        processed_word_list = pre_process_txt(text_string)

        # Extend the final word list by the list of words created by this txt etc.
        final_word_list.extend(processed_word_list)

    return txt_number, final_word_list


# function to pre-process the text taking a string as an argument,
# returns the processed text as a list of words.
def pre_process_txt(text_string):
    # split the string
    words_list = text_string.split()
    # Delete unnecessary characters like spaces etc.
    stripped_word_list = [word.strip(string.punctuation) for word in words_list]
    return stripped_word_list


# function that takes a list of words as an argument and returns a dictionary with words as keys and their frequency
# as values, "sorted" using the values as a key and a sorted list containing only the words(Because lists are sortable).
def word_count(w_list):
    # creating a temporary list to keep track of counted words.
    temp_list = []
    # creating a dictionary to track the frequency of each word.
    word_freq = {}

    for word in w_list:
        # check if word is already counted
        if word not in temp_list:
            # Calculate the frequency
            freq = w_list.count(word)

            # Add this word to the temp list
            temp_list.append(word)
            # Add the word and its frequency in the dictionary.
            word_freq[word] = freq

    # "Sort" the dictionary using values(frequency) as key.
    word_freq_sorted = dict(sorted(word_freq.items(), key=lambda item: item[1], reverse=True))
    # Creating a sorted list containing the words
    word_list_sorted = list(word_freq_sorted.keys())
    return word_freq_sorted, word_list_sorted


# starting messages, reading and preprocessing the files and printing some statistics.
# Only returns a dictionary containing words as keys and their frequenxy as values, its "sorted" by the values.
def starting_up():
    print('Welcome!')
    print('Scanning ".txt" files...\n')

    # call the read_txt function
    txt_n, word_list = read_txt()
    print(f'Scanning is complete! {txt_n} text files are read in total.')
    print(f'The total words read are {len(word_list)}.\n')

    print('Printing some statistics...\n')
    # call the word_count function
    sorted_dict, sorted_list = word_count(word_list)
    print(f'The total unique words read are {len(sorted_list)}.')
    print(f'The most used word is "{sorted_list[0]}" and is used {sorted_dict[sorted_list[0]]} times.')
    print(f'The most rare word is "{sorted_list[-1]}" and is used {sorted_dict[sorted_list[-1]]} times.')
    # TODO an oi lekseis exoun idio freq na vgainei kapoia tuxaia.
    return sorted_dict


#####################################################################################################
#####################################################################################################
#####################################################################################################

word_dict = starting_up()
