#So it begins

def main():
    with open("books/frankenstein.txt") as f: #Open the novel. 
        file_contents = f.read() #Access f which is the novel and read it.
    
    def get_nums_words(text):
        words = text.split() #Split the text into words by whitespace.
        return len(words) #Return the number of words.
    
    #Counting all characters inside the book
    def count_characters(lowered_string):
        count = {} #Create empty dictionary (can create key-value pairs).
        for char in lowered_string: #Loop through each character inside lowered_string
            if char in count:
                count[char] += 1 #Create a new entry where the key is char and set val to 1
            else:
                count[char] = 1 #If the key already exists increase val by 1.
        return count # Placed outside the loop so it can completely finish (was placed inside before test which meant the loop only complete one cycle).


    num_words = get_nums_words(file_contents) #Passing file_contents to get num words and storing inside num words.

    print(f"--- Begin report of {f.name} ---") #Extracting name of novel from file object.
    print(f"{num_words} words are found in the document")
    input("\nPress 'Enter' to view the character count:\n") #Prompt user to get direct character count

    lowered_string = file_contents.lower() #(Calling file_contents instead of file.contents) Convert to lowercase so char counting is case-insensitive
    char_counts = count_characters(lowered_string) #Send complete lowercase text to count_characters.
    #Want to show the most common characters in the book first.
    sorted_char_counts = sorted(char_counts.items(), key=lambda item: item[1], reverse=True) #Sort the characters by number not letter and from biggest to smallest.
    #Looping through the sorted character count pairs and printng
    for char, count in sorted_char_counts:
        print(f"The '{char}' character was found {count} times")

    print("--- End Report ---")
    


    




if __name__ == "__main__": # If this script is being run directly (not imported), execute the main function.
    main()
