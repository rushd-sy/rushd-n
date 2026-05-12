# Write a function word_count(text: str) -> dict[str, int] 
# that returns word frequencies, lowercase,
# ignoring punctuation.
# Test on a paragraph of Lorem Ipsum.



def word_count(text: str):
    words_list = text.split()
    dic = {}
    
    for word in words_list:
        dic[word.lower()] = dic.get(word.lower(), 0) + 1
    
    return dic




if __name__ == "__main__":
    text = input("Enter your text please: ")
    print(word_count(text))
