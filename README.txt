.txt files must be put in the directory of the program.

available modes explained:
1. Word suggestion based on frequency.
Asks for a word and the number of suggestions you want and then prints the 
suggested words. Words are suggested based on how many times they are 
found to follow the given word. If two or more words have the same frequency
one of them is chosen randomly.
2. Sentence suggestion based on frequency.
Asks for a word and the number words you want your sentence to have and then
for every word the procedure mentioned in the previous mode is executed and the
word with the biggest frequency is chosen. Then the sentence gets printed.
If two or more words have the same frequency one of them is chosen randomly.
3. Word suggestion based on possibility.
Asks for a word and the number of suggestions you want and then prints the 
suggested words. Words are suggested based on a random choise selection that
uses their possibility ratio. Possibility ratio is calculated based on how many times
that word is found to follow the given word. For example if the word "evening" follows 
the word "good" 4 out of 20 times the word "good" is found then the possibility ratio 
of the word evening given the word good is 20 %.
4. Sentence suggestion based on possibility.
Asks for a word and the number words you want your sentence to have and then
for every word the procedure mentioned in the previous mode is executed with the number 
of suggestions being 1. Then the sentence gets printed. 