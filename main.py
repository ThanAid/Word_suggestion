import string
import os
import glob
import random
import sys

# Creating an empty graph to "save" words as keys and the following words as values for example
# "Hi! My name is unknown.", in this case "My" is a word and "name" is the following one.
# The "weight" of the following word (meaning the times that it has been detected) is also "saved" in the graph.
# ex. word_graph = {'good': ['morning', 2, 'evening', 4]} where 2 are the times morning is used after good.
word_graph = {}


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
# as values, "sorted" using the values as a key and also returns
# a sorted list containing only the words(Because lists are sortable).
def word_count(w_list):
    # creating a dictionary to track the frequency of each word.
    word_freq = {}

    for word in w_list:
        # check if word is already counted
        if word not in word_freq:
            # if not then the current frequency is 1
            word_freq[word] = 1

        else:
            # if yes then the current frequency is the old + 1
            word_freq[word] += 1

    # "Sort" the dictionary using values(frequency) as key.
    word_freq_sorted = dict(sorted(word_freq.items(), key=lambda item: item[1], reverse=True))
    # Creating a sorted list containing the words
    word_list_sorted = list(word_freq_sorted.keys())
    return word_freq_sorted, word_list_sorted


# function that takes a list of words as an argument and returns a graph with words as vertices and their following
# words as edges with their corresponding frequency as weight.
def list_to_graph(txt_list):
    for i in range(0, len(txt_list) - 1):
        v1 = txt_list[i]
        v2 = txt_list[i + 1]
        w = 1

        # now we call the function graph_add_node to add those words to the graph
        graph_add_node(v1, v2, w)


# Creating a function that will add keys, values and the weight of the values to the graph
# v1 is vertices, v2 edge and w the weight of that edge
def graph_add_node(v1, v2, w):
    # Check if v1 already exists
    if v1 in word_graph:
        # check if v2 doesn't exist for that v1
        if v2 not in word_graph[v1]:
            # We add the v2 and the corresponding w in the already existing v1
            word_graph[v1].append(v2)
            word_graph[v1].append(w)

        else:
            # if v2 does exist again under the same key, then we need to find its index.
            index_v2 = word_graph[v1].index(v2)
            # now we just add 1 to the corresponding weight which has index, index_v2 + 1
            word_graph[v1][index_v2 + 1] += 1

    else:
        # if v1 doesn't exist we add it and at the same time add v2 and w using a temporary dictionary
        temp_dict = {
            v1: [v2, w]
        }
        word_graph.update(temp_dict)


# Creating a function that will take a word and the number of the suggestions you want
# as an argument and return the following words with the maximum likelihood
# randomness is a boolean, if its true words are picked if they have the max frequency,
# if false, words are picked using their frequency as a probability ratio.
# For example,
# if a word is found 6 times out of 10 after the current word then that word has 60 % chance of being suggested.
def graph_next_word(current_word, number_suggestions, randomness=False):
    # Creating a list to store the weights of the corresponding vertices.
    w_list = []
    # Creating a list to store the vertices of the corresponding weights.
    v_list = []
    # Creating a list to store suggestions and keep duplicates out.
    suggestions = []

    for w in word_graph[current_word]:
        # Choosing only the integers so we choose the weights
        if isinstance(w, int):
            w_list.append(w)
        else:
            v_list.append(w)

    # Check if the asked number of suggestions exists and provide a message if not (also adjust the number).
    if int(number_suggestions) > int(len(w_list)):
        # adjust the number
        number_suggestions = int(len(w_list))
        print(f'The number of suggestions you asked for doesn\'t exist for that word. Here are {number_suggestions} '
              f'suggestions:')

        # loop for each suggestion.
    for k in range(0, number_suggestions):

        # if we want the suggestions to be the most frequent following word (randomness = False)
        if not randomness:
            # find the max weight
            chosen_w = max(w_list)

            # Use the line below to get it randomized in case of a draw(for
            # example if two words have the same weight).
            chosen_w_index = random.choice([i for i in range(len(w_list))
                                            if w_list[i] == chosen_w])

        # if we want the suggestions to be the calculated via possibility (randomness = True)
        else:
            # Calculating total weight
            total_weight = sum(w_list)
            # Creating a list to store probability of each word
            p_list = []
            for w in w_list:
                # Calculate the probability and add it to the p_list
                p_list.append(w / total_weight)

            chosen_w_index = v_list.index(random.choices(v_list, weights=p_list, k=1)[0])

        # put the suggested word in the list suggestions
        suggestions.append(v_list[chosen_w_index])

        # remove that value from the list of the weights and vertices, using index.
        del v_list[chosen_w_index]
        del w_list[chosen_w_index]

    # return the edge with the maximum weight
    return suggestions


# starting messages, reading and preprocessing the files and printing some statistics.
# Only returns a dictionary containing words as keys and their frequency as values, its "sorted" by the values.
def starting_up():
    print('Welcome!')
    print('Scanning ".txt" files...\n')

    # call the read_txt function
    txt_n, word_list = read_txt()
    print(f'Scanning is complete! {txt_n} text files are read in total.')

    # if there are no .txt files the program will be terminated.
    if txt_n == 0:
        print('Please put at least one .txt file in the directory of the program.')
        print('\nProgram will now end...')
        sys.exit()
    print(f'The total words read are {len(word_list)}.\n')

    print('Printing some statistics...\n')
    # call the word_count function
    sorted_dict, sorted_list = word_count(word_list)
    print(f'The total unique words read are {len(sorted_list)}.')
    print(f'The most used word is "{sorted_list[0]}" and is used {sorted_dict[sorted_list[0]]} times.')
    print(f'One of the most rare words is "{sorted_list[-1]}" and is used {sorted_dict[sorted_list[-1]]} time(s).')
    return word_list


def main_menu():
    # printing available modes.
    print('\nThe available modes are: ')
    print('Frequency based:')
    print('   1--Word suggestion')
    print('   2--Sentence suggestion')
    print('Possibility based:')
    print('   3--Word suggestion')
    print('   4--Sentence suggestion')
    print('5--Exit')
    ans = input('\nPlease provide the corresponding number: ')

    # Check the answer
    while True:
        # if answer is 1 then mode A is entered.
        if ans == '1':
            print('\nHow many suggestions do you want to be provided for each word?')
            ans_ = input('Please type a number: ')
            while not ans_.isnumeric() or ans_ == '0':
                ans_ = input('Please type a valid number: ')

            # convert string to int
            ans_ = int(ans_)
            # call mode_a function that makes the suggestions.
            mode_a(ans_)

        # if answer is 2 then mode B is entered.
        elif ans == '2':
            print('\nHow many words do you want your sentence to have?')
            ans_b = input('Please type a number: ')
            while not ans_b.isnumeric() or ans_b == '0':
                ans_b = input('Please type a valid number: ')

            # convert string to int
            ans_b = int(ans_b)
            # call mode_a function that makes the suggestions.
            mode_b(ans_b)

        # if answer is 3 then mode C is entered.
        elif ans == '3':
            print('\nHow many suggestions do you want to be provided for each word?')
            ans_c = input('Please type a number: ')
            while not ans_c.isnumeric() or ans_c == '0':
                ans_c = input('Please type a valid number: ')

            # convert string to int
            ans_c = int(ans_c)
            # call mode_a function that makes the suggestions.
            mode_a(ans_c, posib=True)
            # if answer is 2 then mode B is entered.

        # if answer is 3 then mode D is entered.
        elif ans == '4':
            print('\nHow many words do you want your sentence to have?')
            ans_d = input('Please type a number: ')
            while not ans_d.isnumeric() or ans_d == '0':
                ans_d = input('Please type a valid number: ')

            # convert string to int
            ans_d = int(ans_d)
            # call mode_a function that makes the suggestions.
            mode_b(ans_d, posib=True)

        # if answer is 5 then the program will exit.
        elif ans == '5':
            print('\nExiting...')
            sys.exit()

        # if the answer is neither 1, 2, 3 nor 4 then the program will ask again.
        else:
            print('Wrong input.')
            main_menu()


# function that asks for a word and makes suggestions for following words based on frequency.
# takes an int as an argument that tells the number of suggestions the user wants.
def mode_a(n_sug, posib=False):
    while True:
        word = input('\nProvide a word or "q" to exit to the main menu: ').lower()
        if word in word_graph:
            suggestion = graph_next_word(word, n_sug, posib)
            print(", ".join(suggestion))

        # Check if user wants to exit
        elif word == 'q':
            main_menu()

        # if the provided word doesn't exist print a message.
        else:
            print('Word not found.')


# function that asks for a word and creates a sentence using the most frequent following words.
# Takes an int as an argument that will be the size (number of words) of the sentence.
# n_sug is and must be by default 1.
def mode_b(sentence_size, n_sug=1, posib=False):
    while True:
        word = input('\nProvide a word or "q" to exit to the main menu: ').lower()
        # Create a variable (list) to store the suggested words.
        words = []

        if word in word_graph:
            # put the typed word to the words list.
            words.append(word)
            for k in range(1, sentence_size):
                if word in word_graph:
                    suggestion = graph_next_word(word, n_sug, posib)
                    # put the suggested word to the words list
                    # (index '0' is used to pick the first and only word in the list of suggestions)
                    words.append(suggestion[0])
                    # make the suggestion the next word to be provided to the function graph_next_word.
                    word = suggestion[0]

                else:
                    print(f"There are not enough words in the programmes' dictionary to create "
                          f"a sentence with {sentence_size} words. A sentence with {k} words is created instead: ")
                    break

            # print the sentence created as a string.
            print(' '.join(words).capitalize() + '.')

        # Check if user wants to exit
        elif word == 'q':
            main_menu()

        # if the provided word doesn't exist print a message.
        else:
            print('Word not found.')


#####################################################################################################
#####################################################################################################
#####################################################################################################
###################################### main program #################################################
#####################################################################################################


# get all the texts as a list of words.
final_list = starting_up()

print('\nAnalysing the data...')
# we need to convert the list to a graph
list_to_graph(final_list)
print('Model created.')

# Calling the menu
main_menu()
