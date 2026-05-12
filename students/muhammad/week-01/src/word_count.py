# Write a function word_count(text: str) -> dict[str, int] 
# that returns word frequencies, lowercase,
# ignoring punctuation.
# Test on a paragraph of Lorem Ipsum.


from collections import Counter


def word_count(text: str):
    words_list = text.split()
    dic = {}
    
    for word in words_list:
        dic[word.lower()] = dic.get(word.lower(), 0) + 1
    
    return dic


def word_count_2(s: str):
    w = [word.lower() for word in s.split()]
    return Counter(w)


if __name__ == "__main__":
    text = input("Enter your text please: ")
    print(f"Method one:\n{word_count(text)}")
    print(f"Method twp:\n{word_count_2(text)}")

