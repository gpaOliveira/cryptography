from constants import *
from math import fabs
from operator import itemgetter

def break_message_in_columns(message, columns_to_break):
    """Separate message in N columns (N = columns_to_break)"""
    #initialize the columns structure
    column_text = {i: [] for i in range(0, columns_to_break)}
    
    #lets iterate trough our message
    index = 0
    for m in message:        
        #add the letter to the right column
        column_text[index].append(m)
        index += 1
        
        #end the loop and make sure the next m-char analyzed goes to the next column or goes back to the start (0)        
        if index == columns_to_break:            
            index = 0
    
    return column_text

def assemble_message_from_columns(columns_to_build_from):
    """Reacrete message from N columns (N = columns_to_build_from)"""
    #initialize the text structure
    max_column_len = max([len(c) for c in columns_to_build_from])
    text = ""
    for i in range(0, max_column_len):
        for c in columns_to_build_from:
            try:
                text += c[i]
            except:
                text += ""
    
    return text
    
def count_occurences(column):
    """Part of the coincidence index of a message`s columns: the letters count process"""
    letters_count = {c: 0 for c in column}
    for c in column:
        letters_count[c] += 1
    return letters_count
    
def sum_of_counts(letters_count):
    """Part of the coincidence index of a message`s columns: the sum of letters count"""
    return sum([(fi*(fi-1)) for f,fi in letters_count.iteritems()])
    
def calculate_coincidence_index(message, column, debug=False):
    """Calculate the coincidence index of a message`s columns"""
    letters_count = count_occurences(column)
    n = float(len(column))
    n = (n*(n-1))
    
    if n > 0.0:#avoiding a division by 0
        sum = sum_of_counts(letters_count)
        ic = float(sum)/n
        if debug: 
            print "calculate_coincidence_index",letters_count,sum,n
        return ic
    else:
        if debug: 
            print "calculate_coincidence_index - 0.0",letters_count,float(len(column)),n
        return 0.0    

def calculate_column_wise_coincidence_index(message, proposed_key_len, debug=False):
    """Calculate the coincidence index of a message in a column wise way"""
    #break message in columns 
    columns = break_message_in_columns(message, proposed_key_len)

    #compute the ic on each column
    ics = {}
    sum = 0.0
    for c in range(0, proposed_key_len):
        coincidence_index = calculate_coincidence_index(message, columns[c], debug)
        ics[c] = coincidence_index
        sum += ics[c]
    avg = round(float(sum)/proposed_key_len,2)
    if debug:
        print "+++calculate_column_wise_coincidence_index",proposed_key_len,avg,ics,"\n"
    return avg

def find_best_key_len(message,debug=False):
    """Calculate the most probable key len of a given ciphered message"""
    english_ic = 0.067
    best_len = 0
    avg_ics = []
    for i in range(1,20):#the key is not often bigger than that...
        #grab the column wise coincidence index for a key with len = i
        avg_ic = calculate_column_wise_coincidence_index(message, i, debug)
        #store the difference between each one and the english_ic
        avg_ics.append(fabs(avg_ic - english_ic))
    
    #grab the min-difference position (0..n-1) and adjust it to the range (1..n)
    best_len = avg_ics.index(min(avg_ics)) + 1 
    if debug:
        print "==>" ,best_len,avg_ics,"\n"
    return best_len
    
def move_letters_according_to_key_len(message, key_len, debug=False):
    """Move letters according to frequency analysis of each column"""
    columns = break_message_in_columns(message, key_len)
    
    #move letters on each column
    decrypted_columns = []
    movements = []
    for c in range(0, key_len):
        move,decrypted = move_letters_based_on_frequency_analysis(columns[c])
        movements.append(move)
        decrypted_columns.append(decrypted)
    text = assemble_message_from_columns(decrypted_columns)
    key = "".join(map(lambda x: LETTERS[x], movements))
    if debug:
        print "!!!!move_letters_according_to_key_len",text,movements,key,"\n"
    return key,text
    
    
def friedman(message,debug=False):
    """Calculate the estimated key len trough Friedman`s method. Taken from http://crypto.stackexchange.com/questions/333/how-does-the-index-of-coincidence-work-in-the-kasiki-test"""
    global_ic = calculate_coincidence_index(message, message, debug)
    english_ic = 0.067
    english_letters_division = 0.0385 #1/26
    n = float(len(message))
    result = float((english_ic-english_letters_division)*n)
    if debug:
        print result
    divisor = float(( (n * global_ic) - ( n * english_letters_division) + (english_ic - global_ic)))
    if debug:
        print divisor
    result = float(result/divisor)
    return result

def move_letters(message, movement, debug = False):
    moved = ""
    for m in message:
        if debug:
            print m
            print LETTERS[((LETTERS.find(m) + movement)%len(LETTERS))]
        moved += LETTERS[((LETTERS.find(m) + movement)%len(LETTERS))]
    return moved

def move_letters_based_on_frequency_analysis(message):
    #print message
    occurences = count_occurences(message)#{A:1,B:2,C:3, ...}
    iteractions = len(occurences.keys())
    occurences = occurences.items()#((A,1),(B,2),(C,3), ...}    
    #print occurences
    local_frequency_english = FREQUENCY_IN_ENGLISH[:]#shallow copy
    local_letters = LETTERS[:]#shallow copy
    
    #find the max occurence to deduce the movement
    english_max_percent = max(local_frequency_english)
    english_char_index = local_frequency_english.index(english_max_percent)
    max_tuple = max(occurences, key=itemgetter(1))
    movement = (ord(max_tuple[0]) - ord(LETTERS[english_char_index]))%len(LETTERS)
    #print movement
    #print chr(ord('A') + movement)
    
    return movement,move_letters(message, -movement)        
        
if __name__ == "__main__":
    print "Run tests with 'python test_friedman_find_key_len.py'"
    print "If you're the teacher, a better way to check this program is to use 'python test_friedman_find_key_len.py TestBreakHelperMethods.test_mooodle_class'"