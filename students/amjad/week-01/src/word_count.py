from collections import Counter
def word_count(st : str) -> dict[str, int] :
    di = Counter(st.split())
    return di

st = input()
freq = word_count(st)
for key, value in freq.items():
    print(key, value)