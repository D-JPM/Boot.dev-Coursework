#So it begins

def main():
    with open("books/frankenstein.txt") as f: #Open the novel. 
        file_contents = f.read() #Access f which is the novel and read it.
    
    def get_nums_words(text):
        words - text.split() #Split the text into words by whitespace.
        return len(words) #Return the number of words.

    num_words = get_num_words(file_contents) #Passing file_contents to get num words and storing inside num words.

    print(f"--- Begin report of {f.name} ---") #Extracting name of novel from file object.
     
