import datetime

# this actually shall be the input design

words = [ 
    ["Word1-V1", "Word1-V2","Word1-V3", ""],
    ["Word2-V1", "Word2-V2","Word2-V3", ""],
    ["Word3-V1", "Word3-V2","Word3-V3", ""],
    ["Word4-V1", "Word4-V2","Word4-V3", ""],
    ["Word5-V1", "Word5-V2","Word5-V3", ""]
    ]
    
# function to actually generate the wordlist based on words as input

def gen_wordlist(wordlist):
    
    wordlist_it = wordlist
    
    if (len(wordlist_it)>1):
        wordlist_it[0] = join_words(wordlist[0],wordlist[1])
        wordlist_it.remove(wordlist[1])
        
        return gen_wordlist(wordlist_it)
    else:
        return wordlist_it

# functions to merge two lists, used as subfunction within gen_wordlist
         
def join_words(list1, list2):
    
    joined_list = []
    word = []
    for x in list1:
        for y in list2:
            word = [x,y]
            word = ''.join(word)
            joined_list.append(word)
            
    return (joined_list)

# function that generates the filename for the wordlist. The purpose is to clean the wordlist names up by default

def gen_filename(list1):
    print("generating filepath for storing wordlist ...")
    filename = "wordlist_" + str(datetime.datetime.now())
    filename = filename.replace(' ','_')
    filename = filename.replace(':','-')
    filename = filename.replace('.','_')
    filename = filename + "_config"
    for element in list1:
        filename = filename + "-" + str(len(element)) 
    
    return (filename + ".txt")

# function to generate a config name, matching the concept of above. Sorry, I was lazy and just copied the thing.

def gen_configname(list1):
    print("generating filepath for storing config file ...")
    filename = "config_" + str(datetime.datetime.now())
    filename = filename.replace(' ','_')
    filename = filename.replace(':','-')
    filename = filename.replace('.','_')
    filename = filename + "_config"
    for element in list1:
        filename = filename + "-" + str(len(element)) 
    
    return (filename + ".txt")    

# function to flatten nested lists before writing to disc

def flatten_list(_2d_list):
    print("flattening input list for storage ...")
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

# simple write file function

def write_file(filename, list1):
    textfile = open(filename, "w")
    print("writing "+ filename+" to disc ...")
    if (any(isinstance(i, list) for i in list1)):
        write_file(filename, flatten_list(list1))
    else:
        for element in list1:
            textfile.write(element + "\n")
        textfile.close()
        print("file sucessfully written ...")
        print("open "+ filename + " to see results ...")

filename_config = gen_configname(words)
filename_wordlist = gen_filename(words)

write_file(filename_config, words)
print("generating wordlist ...")
wordlist = gen_wordlist(words)
print ('variants generated: ', len(wordlist[0]))

print ('appending config filename to wordlist for traceback ...')
wordlist[0].append(filename_config)

# if you want to see the generated wordlist, you can uncomment this one
# please consider the size of the list before uncommenting
# print ('Words found: ', wordlist[0])

write_file(filename_wordlist, wordlist[0])
